
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import (
    equally_sized_accessor as _ods_equally_sized_accessor,
    get_default_loc_context as _ods_get_default_loc_context,
    get_op_result_or_op_results as _get_op_result_or_op_results,
    get_op_result_or_value as _get_op_result_or_value,
    get_op_results_or_values as _get_op_results_or_values,
    segmented_accessor as _ods_segmented_accessor,
)
_ods_ir = _ods_cext.ir

import builtins
from typing import Sequence as _Sequence, Union as _Union


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "verif"

@_ods_cext.register_operation(_Dialect)
class AssertOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.assert"

  _ODS_REGIONS = (0, True)

  def __init__(self, property, *, label=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(property))
    _ods_context = _ods_get_default_loc_context(loc)
    if label is not None: attributes["label"] = (label if (
        isinstance(label, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrAttr')) else
          _ods_ir.AttrBuilder.get('StrAttr')(label, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def property(self):
    return self.operation.operands[0]

  @builtins.property
  def label(self):
    if "label" not in self.operation.attributes:
      return None
    return self.operation.attributes["label"]

  @label.setter
  def label(self, value):
    if value is not None:
      self.operation.attributes["label"] = value
    elif "label" in self.operation.attributes:
      del self.operation.attributes["label"]

  @label.deleter
  def label(self):
    del self.operation.attributes["label"]

def assert_(property, *, label=None, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(AssertOp(property=property, label=label, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class AssumeOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.assume"

  _ODS_REGIONS = (0, True)

  def __init__(self, property, *, label=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(property))
    _ods_context = _ods_get_default_loc_context(loc)
    if label is not None: attributes["label"] = (label if (
        isinstance(label, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrAttr')) else
          _ods_ir.AttrBuilder.get('StrAttr')(label, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def property(self):
    return self.operation.operands[0]

  @builtins.property
  def label(self):
    if "label" not in self.operation.attributes:
      return None
    return self.operation.attributes["label"]

  @label.setter
  def label(self, value):
    if value is not None:
      self.operation.attributes["label"] = value
    elif "label" in self.operation.attributes:
      del self.operation.attributes["label"]

  @label.deleter
  def label(self):
    del self.operation.attributes["label"]

def assume(property, *, label=None, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(AssumeOp(property=property, label=label, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class CoverOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.cover"

  _ODS_REGIONS = (0, True)

  def __init__(self, property, *, label=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(property))
    _ods_context = _ods_get_default_loc_context(loc)
    if label is not None: attributes["label"] = (label if (
        isinstance(label, _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrAttr')) else
          _ods_ir.AttrBuilder.get('StrAttr')(label, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def property(self):
    return self.operation.operands[0]

  @builtins.property
  def label(self):
    if "label" not in self.operation.attributes:
      return None
    return self.operation.attributes["label"]

  @label.setter
  def label(self, value):
    if value is not None:
      self.operation.attributes["label"] = value
    elif "label" in self.operation.attributes:
      del self.operation.attributes["label"]

  @label.deleter
  def label(self):
    del self.operation.attributes["label"]

def cover(property, *, label=None, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(CoverOp(property=property, label=label, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class FormatVerilogStringOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.format_verilog_string"

  _ODS_REGIONS = (0, True)

  def __init__(self, formatString, substitutions, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(substitutions))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["formatString"] = (formatString if (
    isinstance(formatString, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(formatString, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def substitutions(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def formatString(self):
    return self.operation.attributes["formatString"]

  @formatString.setter
  def formatString(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["formatString"] = value

  @builtins.property
  def str(self):
    return self.operation.results[0]

def format_verilog_string(format_string, substitutions, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(FormatVerilogStringOp(formatString=format_string, substitutions=substitutions, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class HasBeenResetOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.has_been_reset"

  _ODS_REGIONS = (0, True)

  def __init__(self, clock, reset, async_, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clock))
    operands.append(_get_op_result_or_value(reset))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["async"] = (async_ if (
    isinstance(async_, _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('BoolAttr')) else
      _ods_ir.AttrBuilder.get('BoolAttr')(async_, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clock(self):
    return self.operation.operands[0]

  @builtins.property
  def reset(self):
    return self.operation.operands[1]

  @builtins.property
  def async_(self):
    return self.operation.attributes["async"]

  @async_.setter
  def async_(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["async"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]

def has_been_reset(clock, reset, async_, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(HasBeenResetOp(clock=clock, reset=reset, async_=async_, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class LogicEquivalenceCheckingOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.lec"

  _ODS_REGIONS = (2, True)

  def __init__(self, areEquivalent, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(areEquivalent)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def areEquivalent(self):
    return self.operation.results[0]

  @builtins.property
  def firstCircuit(self):
    return self.regions[0]

  @builtins.property
  def secondCircuit(self):
    return self.regions[1]

def lec(are_equivalent, *, loc=None, ip=None) -> _ods_ir.Value:
  return _get_op_result_or_op_results(LogicEquivalenceCheckingOp(areEquivalent=are_equivalent, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class PrintOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.print"

  _ODS_REGIONS = (0, True)

  def __init__(self, string, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(string))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def string(self):
    return self.operation.operands[0]

def print_(string, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(PrintOp(string=string, loc=loc, ip=ip))

@_ods_cext.register_operation(_Dialect)
class YieldOp(_ods_ir.OpView):
  OPERATION_NAME = "verif.yield"

  _ODS_REGIONS = (0, True)

  def __init__(self, inputs, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(attributes=attributes, results=results, operands=operands, successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

def yield_(inputs, *, loc=None, ip=None) -> _ods_ir.Operation:
  return _get_op_result_or_op_results(YieldOp(inputs=inputs, loc=loc, ip=ip))
