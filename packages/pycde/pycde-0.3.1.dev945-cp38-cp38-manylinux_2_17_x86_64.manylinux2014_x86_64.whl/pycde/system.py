#  Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
#  See https://llvm.org/LICENSE.txt for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from __future__ import annotations

from pycde.devicedb import (EntityExtern, PlacementDB, PrimitiveDB,
                            PhysicalRegion)

from .common import _PyProxy
from .instance import Instance, InstanceHierarchyRoot
from .module import Module, ModuleLikeType, ModuleLikeBuilderBase
from .types import TypeAlias

from . import circt
from .circt import ir, passmanager
from .circt.dialects import esi, hw, msft

from contextvars import ContextVar
from collections.abc import Iterable
import weakref
import gc
import os
import pathlib
import sys
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

_current_system = ContextVar("current_pycde_system")


class System:
  """The 'System' contains the user's design and some private bookkeeping. On
  construction, specify a list of 'root' modules which you wish to generate.
  Upon generation, the design will be fleshed out and all the dependent modules
  will be created.

  'System' also has methods to run through the CIRCT lowering, output tcl, and
  output SystemVerilog."""

  __slots__ = [
      "mod", "top_modules", "name", "passed", "_old_system_token", "_op_cache",
      "_generate_queue", "output_directory", "files", "mod_files",
      "packaging_funcs", "sw_api_langs", "_instance_roots", "_placedb",
      "_appid_index", "platform"
  ]

  def __init__(self,
               top_modules: Union[list, Module],
               name: str = None,
               output_directory: str = None,
               sw_api_langs: List[str] = None):
    from .module import Module
    self.passed = False
    self.mod = ir.Module.create()
    if isinstance(top_modules, Iterable):
      self.top_modules = list(top_modules)
    else:
      self.top_modules = [top_modules]
    if name is None:
      self.name = self.top_modules[0].__name__
    else:
      self.name = name
    self._op_cache: _OpCache = _OpCache(self.mod)

    self._generate_queue = []
    # _instance_roots indexed by (module, instance_name).
    self._instance_roots: dict[(Module, str), InstanceHierarchyRoot] = {}

    self._placedb: PlacementDB = None
    self._appid_index: esi.AppIDIndex = None

    # To be set by a BSP. Gets passed through to CIRCT to direct lowerings.
    # Should be replaced by a more general mechanism (a target triple type
    # thing).
    self.platform = ""

    # The set of all files generated by PyCDE.
    self.files: Set[os.PathLike] = set()
    # The set of module SV files generated by PyCDE.
    self.mod_files: Set[os.PathLike] = set()
    self.packaging_funcs: List[Callable] = []
    self.sw_api_langs = sw_api_langs

    if output_directory is None:
      output_directory = os.path.join(os.getcwd(), self.name)
    self.output_directory = pathlib.Path(output_directory)
    self.output_directory.mkdir(exist_ok=True)
    self.hw_output_dir.mkdir(exist_ok=True)

    with self:
      [m._builder.circt_mod for m in self.top_modules]

  def add_packaging_step(self, func: Callable):
    self.packaging_funcs.append(func)

  def _return_create_if_necessary(self, dir: pathlib.Path):
    """Return the director given by 'dir' but create it if it doesn't exist."""
    if not dir.exists():
      dir.mkdir()
    return dir

  @property
  def hw_output_dir(self):
    return self._return_create_if_necessary(self.output_directory / "hw")

  @property
  def runtime_output_dir(self):
    return self._return_create_if_necessary(self.output_directory / "runtime")

  def _get_ip(self):
    return ir.InsertionPoint(self.mod.body)

  @staticmethod
  def set_debug():
    ir._GlobalDebug.flag = True

  # TODO: Ideally, we'd be able to run the cf-to-handshake lowering passes in
  # pycde.  As of now, however, the cf/memref/arith dialects are not registered
  # so the assembly can't be loaded. The right way to do this is to have pycde
  # load those dialects, though there isn't a python hook to selectively load
  # them.  Really, it's time for pycde to have a pybind11 module so we have more
  # flexibility to do this sort of thing. Until we get around to that, this'll
  # be commented out.
  # HANDSHAKE = [
  #     "flatten-memref",
  #     "flatten-memref-calls",
  #     "func.func(handshake-legalize-memrefs)",
  #     "lower-cf-to-handshake",
  #     "canonicalize",
  #     "handshake-lower-extmem-to-hw{wrap-esi}",
  #     "canonicalize",
  #     "handshake.func(handshake-insert-buffers)",
  #     "canonicalize",
  #     "handshake.func(handshake-remove-block-structure)",
  #     "handshake.func(handshake-materialize-forks-sinks)",
  #     "lower-handshake-to-hw",
  #     "canonicalize",
  # ]

  def import_mlir(self, module, lowering=None) -> Dict[str, Any]:
    """Import mlir asm created elsewhere into our space."""

    compat_mod = ir.Module.parse(str(module))
    if lowering is not None:
      pm = passmanager.PassManager.parse(",".join(lowering))
      pm.run(compat_mod.operation)
    ret: Dict[str, Any] = {}
    for op in compat_mod.body:
      # TODO: handle symbolrefs pointing to potentially renamed symbols.
      if isinstance(op, hw.HWModuleOp):
        from .module import import_hw_module
        im = import_hw_module(op)
        self._create_circt_mod(im._builder)
        ret[ir.StringAttr(op.name).value] = im
      elif isinstance(op, esi.RandomAccessMemoryDeclOp):
        from .esi import _import_ram_decl
        ram = _import_ram_decl(self, op)
        ret[ir.StringAttr(op.sym_name).value] = ram
        self.body.append(op)
      else:
        # TODO: do symbol renaming.
        self.body.append(op)
    return ret

  def create_physical_region(self, name: str = None):
    with self._get_ip():
      physical_region = PhysicalRegion(name)
    return physical_region

  def create_entity_extern(self, tag: str, metadata=""):
    with self._get_ip():
      entity_extern = EntityExtern(tag, metadata)
    return entity_extern

  def _create_circt_mod(self, builder: ModuleLikeBuilderBase):
    """Wrapper for a callback (which actually builds the CIRCT op) which
    controls all the bookkeeping around CIRCT module ops."""

    (symbol, install_func) = self._op_cache.create_symbol(builder)
    if symbol is None:
      return

    # Build the correct op.
    op = builder.create_op(self, symbol)
    # Install the op in the cache.
    install_func(op)
    # Add to the generation queue if the module has a generator callback.
    if len(builder.generators) > 0:
      self._generate_queue.append(builder)
      file_name = builder.modcls.__name__ + ".sv"
      outfn = self.hw_output_dir / file_name
      self.files.add(outfn)
      self.mod_files.add(outfn)
      op.fileName = ir.StringAttr.get(str(file_name))
    return op

  @staticmethod
  def current() -> System:
    """Get the top-most system in the stack created by `with System()`."""
    bb = _current_system.get(None)
    if bb is None:
      raise RuntimeError("No PyCDE system currently active!")
    return bb

  def __enter__(self):
    self._old_system_token = _current_system.set(self)

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_value is not None:
      return
    _current_system.reset(self._old_system_token)

  @property
  def body(self):
    return self.mod.body

  def print(self, *argv, **kwargs):
    self.mod.operation.print(*argv, **kwargs)

  def cleanup(self):
    pm = passmanager.PassManager.parse("builtin.module(canonicalize)")
    pm.run(self.mod.operation)

  def generate(self, generator_names=[], iters=None, skip_appid_index=False):
    """Fully generate the system unless iters is specified. Iters specifies the
    number of generators to run. Useful for debugging. Maybe."""
    i = 0
    with self:
      while len(self._generate_queue) > 0 and (iters is None or i < iters):
        m = self._generate_queue.pop()
        m.generate()
        i += 1

    if len(self._generate_queue) == 0:
      self.mod.operation.verify()
      if not skip_appid_index:
        self._appid_index = esi.AppIDIndex(self.mod.operation)

  def get_instance(self,
                   mod_cls: object,
                   instance_name: str = None) -> InstanceHierarchyRoot:
    assert len(self._generate_queue) == 0, "Ungenerated modules left"
    mod = mod_cls._builder
    key = (mod, instance_name)
    if key not in self._instance_roots:
      self._instance_roots[key] = InstanceHierarchyRoot(mod, instance_name,
                                                        self)
    return self._instance_roots[key]

  PASS_PHASES = [
      # First, run all the passes with callbacks into pycde.
      "builtin.module(esi-connect-services)",
      lambda sys: sys.generate(),
      # After all of the pycde code has been executed, we have all the types
      # defined so we can go through and output the typedefs delcarations.
      lambda sys: TypeAlias.declare_aliases(sys.mod),
      "builtin.module(esi-appid-hier{{top={tops} }}, esi-build-manifest{{top={tops} }})",
      "builtin.module(msft-lower-constructs, msft-lower-instances)",
      "builtin.module(esi-clean-metadata)",
      "builtin.module(hw.module(lower-seq-hlmem))",
      "builtin.module(lower-esi-to-physical)",
      # TODO: support more than just cosim.
      "builtin.module(lower-esi-bundles, lower-esi-ports)",
      "builtin.module(lower-esi-to-hw{{platform={platform}}})",
      "builtin.module(convert-fsm-to-sv)",
      "builtin.module(lower-hwarith-to-hw)",
      "builtin.module(lower-seq-to-sv)",
      "builtin.module(lower-comb)",
      "builtin.module(cse, canonicalize, cse)",
      "builtin.module(hw.module(prettify-verilog), hw.module(hw-cleanup))",
      "builtin.module(msft-export-tcl{{tops={tops} tcl-file={tcl_file}}})"
  ]

  def run_passes(self, debug=False):
    if self.passed:
      return
    self.generate()

    tops = ",".join(
        [self._op_cache.get_pyproxy_symbol(m) for m in self.top_modules])
    verilog_file = self.name + ".sv"
    tcl_file = self.name + ".tcl"
    self.files.add(self.output_directory / verilog_file)
    self.files.add(self.output_directory / tcl_file)

    self._op_cache.release_ops()
    if debug:
      open("after_generate.mlir", "w").write(str(self.mod))
    for idx, phase in enumerate(self.PASS_PHASES):
      aplog = None
      if debug:
        aplog = open(f"after_phase_{idx}.mlir", "w")
      try:
        if isinstance(phase, str):
          passes = phase.format(tops=tops,
                                verilog_file=verilog_file,
                                tcl_file=tcl_file,
                                platform=self.platform).strip()
          if aplog is not None:
            aplog.write(f"// passes ran: {passes}\n")
            aplog.flush()
          pm = passmanager.PassManager.parse(passes)
          pm.run(self.mod.operation)
        else:
          phase(self)
          if aplog is not None:
            aplog.write(f"// <python code>\n")
            aplog.flush()
      except RuntimeError as err:
        sys.stderr.write(f"Exception while executing phase {phase}.\n")
        raise err
      finally:
        if aplog is not None:
          aplog.write(str(self.mod))
          aplog.close()
      self._op_cache.release_ops()

    self.passed = True

  def emit_outputs(self):
    assert self.passed, "Must call 'run_passes' first"
    circt.export_split_verilog(self.mod, str(self.hw_output_dir))

  def compile(self):
    self.generate()
    self.run_passes()
    self.emit_outputs()

  @property
  def placedb(self):
    if self._placedb is None:
      raise Exception("Must `createdb` first")
    return self._placedb

  def createdb(self, primdb: PrimitiveDB = None):
    if self._placedb is None:
      self._placedb = PlacementDB(self, self.mod, primdb)

  def package(self):
    """Package up the system."""
    assert self.passed, "Must call compile before package"
    for func in self.packaging_funcs:
      func(self)


class _OpCache:
  """Used to cache CIRCT operations and handle symbols."""

  import pycde.instance as pi

  __slots__ = [
      "_module", "_symbols", "_pyproxy_symbols", "_symbol_pyproxy",
      "_instance_hier_cache", "_instance_hier_obj_cache", "_instance_cache",
      "_module_inside_sym_cache", "_dyn_insts_in_inst", "_pyproxies"
  ]

  def __init__(self, module: ir.Module):
    self._module = module
    self._symbols: Dict[str, ir.OpView] = None
    self._pyproxy_symbols: dict[_PyProxy, str] = {}
    self._symbol_pyproxy: dict[str, _PyProxy] = {}
    self._pyproxies: Set[weakref.ref[_PyProxy]] = set()

    # InstanceHier caches are indexes are (module_sym, instance_name)
    self._instance_hier_cache: dict[(ir.FlatSymbolRefAttr, ir.StringAttr),
                                    msft.InstanceHierarchyOp] = None
    self._instance_hier_obj_cache: dict[(ir.FlatSymbolRefAttr, ir.StringAttr),
                                        InstanceHierarchyRoot] = {}
    self._instance_cache: dict[Instance, msft.DynamicInstanceOp] = {}

    self._module_inside_sym_cache: Dict[ir.Operation, Dict[ir.Attribute,
                                                           ir.Operation]] = {}
    self._dyn_insts_in_inst: Dict[ir.Operation,
                                  Dict[ir.Attribute,
                                       msft.DynamicInstanceOp]] = {}

  def release_ops(self):
    """Clear all of the MLIR ops we store. Call this before each transition to
    MLIR C++."""
    self._symbols = None
    self._instance_hier_cache = None
    self._instance_cache.clear()
    self._module_inside_sym_cache.clear()
    self._dyn_insts_in_inst.clear()
    for proxy_ref in self._pyproxies:
      proxy = proxy_ref()
      if proxy is not None:
        proxy.clear_op_refs()

    gc.collect()
    # Pending https://github.com/llvm/llvm-project/pull/78663
    # live_ops = ir.Context.current._get_live_operation_objects()
    # for op in live_ops:
    #   sys.stderr.write(f"Warning: {op} is still live. Referrers:\n")
    #   for referrer in gc.get_referrers(op)[0]:
    #     sys.stderr.write(f"  {referrer}\n")
    num_ops_live = ir.Context.current._clear_live_operations()
    if num_ops_live > 0:
      sys.stderr.write(
          f"Warning: something is holding references to {num_ops_live} " +
          " MLIR ops\n")

  @property
  def symbols(self):
    if self._symbols is None:
      self._symbols = {}
      for op in self._module.operation.regions[0].blocks[0]:
        if "sym_name" in op.attributes:
          self._symbols[ir.StringAttr(op.attributes["sym_name"]).value] = op
    return self._symbols

  def op(self, symbol: str) -> ir.OpView:
    """Resolve a symbol to an op."""
    return self.symbols[symbol]

  def register_pyproxy(self, pyproxy: _PyProxy):
    """Used to report a new _PyProxy to the cache which doesn't have a symbol."""
    self._pyproxies.add(weakref.ref(pyproxy))

  def create_symbol(self, pyproxy: _PyProxy) -> Tuple[str, Callable]:
    """Create a unique symbol and add it to the cache. If it is to be preserved,
    the caller must use it as the symbol on a top-level op. Returns the symbol
    string and a callback to install the mapping. Return (None, None) if
    `spec_mod` already has a symbol."""

    if pyproxy in self._pyproxy_symbols:
      return (None, None)
    ctr = 0
    # Get the sanitized name.
    basename = "".join([c if c.isalnum() else '_' for c in pyproxy.name])
    symbol = basename
    while symbol in self.symbols:
      ctr += 1
      symbol = basename + "_" + str(ctr)

    def install(op):
      self._symbols[symbol] = op
      self._pyproxy_symbols[pyproxy] = symbol
      self._symbol_pyproxy[symbol] = pyproxy
      self._pyproxies.add(weakref.ref(pyproxy))

    return symbol, install

  def get_symbol_pyproxy(self, symbol):
    """Get the _PyProxy for a symbol."""
    if isinstance(symbol, ir.Attribute):
      symbol = ir.FlatSymbolRefAttr(symbol).value
    return self._symbol_pyproxy[symbol]

  def get_pyproxy_symbol(self, spec_mod) -> str:
    """Get the symbol for a module or its associated _PyProxy."""
    if not isinstance(spec_mod, Module):
      if isinstance(spec_mod, ModuleLikeType):
        spec_mod = spec_mod._builder
    if spec_mod not in self._pyproxy_symbols:
      return None
    return self._pyproxy_symbols[spec_mod]

  def get_circt_mod(self, spec_mod: Module) -> Optional[ir.Operation]:
    """Get the CIRCT module op for a PyCDE module."""
    sym = self.get_pyproxy_symbol(spec_mod)
    if sym in self.symbols:
      return self.symbols[sym]
    return None

  def _build_instance_hier_cache(self):
    """If the instance hierarchy cache doesn't exist, build it."""
    if self._instance_hier_cache is None:
      self._instance_hier_cache = {}
      for op in self._module.operation.regions[0].blocks[0]:
        if isinstance(op, msft.InstanceHierarchyOp):
          self._instance_hier_cache[(op.top_module_ref, op.instName)] = op

  def create_instance_hier_op(
      self, inst_hier: InstanceHierarchyRoot) -> msft.InstanceHierarchyOp:
    """Create an instance hierarchy op 'inst_hier' and add it to the cache.
    Assert if one already exists in the cache."""

    self._build_instance_hier_cache()

    (root_mod_symbol, instance_name) = inst_hier._cache_key
    assert root_mod_symbol not in self._instance_hier_cache, \
      "Cannot create two instance hierarchy roots for same module"

    with ir.InsertionPoint(self._module.body):
      hier_op = msft.InstanceHierarchyOp.create(root_mod_symbol, instance_name)
      self._instance_hier_cache[(root_mod_symbol, instance_name)] = hier_op
      self._instance_hier_obj_cache[(root_mod_symbol,
                                     instance_name)] = inst_hier

    return hier_op

  def get_instance_hier_op(
      self, inst_hier: InstanceHierarchyRoot) -> msft.InstanceHierarchyOp:
    """Lookup an instance hierarchy op in the cache. None if not found."""

    self._build_instance_hier_cache()
    return self._instance_hier_cache.get(inst_hier._cache_key, None)

  def create_or_get_dyn_inst(self, inst: Instance) -> msft.DynamicInstanceOp:
    """Get the dynamic instance op corresponding to 'inst'. Returns 'None' if
    the instance doesn't have a static op in the IR."""

    # Check static op existence.
    inside_of_syms = self.get_inner_sym_ops_in_module(inst.inside_of)
    if inst.symbol not in inside_of_syms:
      return None

    if inst not in self._instance_cache:
      ref = hw.InnerRefAttr.get(ir.StringAttr.get(inst._inside_of_symbol),
                                inst.symbol.symName)
      # Check if the dynamic instance op exists.
      parent_op = inst.parent._dyn_inst
      insts_in_parent = self.get_dyn_insts_in_inst(parent_op)
      if ref in insts_in_parent:
        # If it is, install it into the instance cache
        inst_op = insts_in_parent[ref]
        self._instance_cache[inst] = inst_op
      else:
        # If not, create a new one and install it into the instance cache and
        # add it to the insts in parent cache.
        with inst.parent._get_ip():
          new_inst = msft.DynamicInstanceOp.create(ref)
          self._instance_cache[inst] = new_inst
          insts_in_parent[ref] = new_inst

    return self._instance_cache[inst]

  def get_or_create_inst_from_op(self, op: ir.OpView) -> pi.Instance:
    """Descend the Python instance hierarchy from the CIRCT IR, returning the
    Python Instance corresponding to 'op'."""

    if isinstance(op, msft.InstanceHierarchyOp):
      return self._instance_hier_obj_cache[(op.top_module_ref, op.instName)]
    if isinstance(op, msft.DynamicInstanceOp):
      parent_inst = self.get_or_create_inst_from_op(op.operation.parent.opview)
      instance_ref = hw.InnerRefAttr(op.instanceRef)
      return parent_inst._children()[hw.InnerSymAttr.get(instance_ref.name)]
    raise TypeError(
        "Can only resolve from InstanceHierarchyOp or DynamicInstanceOp")

  def get_inner_sym_ops_in_module(
      self, module: Module) -> Dict[ir.Attribute, ir.Operation]:
    """Look into the IR inside 'module' for any ops which have an `inner_sym`
    attribute. Cached."""

    if module is None:
      return {}
    circt_mod = self.get_circt_mod(module)
    if isinstance(circt_mod, hw.HWModuleExternOp):
      return {}

    if circt_mod not in self._module_inside_sym_cache:
      self._module_inside_sym_cache[circt_mod] = \
        {op.attributes["inner_sym"]: op
         for op in circt_mod.entry_block
         if "inner_sym" in op.attributes}

    return self._module_inside_sym_cache[circt_mod]

  def get_dyn_insts_in_inst(
      self, inst: ir.Operation) -> Dict[ir.Attribute, msft.DynamicInstanceOp]:
    """Get a mapping of existing dynamic instances inside of instance-like
    'inst'."""

    if inst not in self._dyn_insts_in_inst:
      self._dyn_insts_in_inst[inst] = \
        {op.instanceRef: op for op in inst.body.blocks[0]
         if isinstance(op, msft.DynamicInstanceOp)}
    return self._dyn_insts_in_inst[inst]
