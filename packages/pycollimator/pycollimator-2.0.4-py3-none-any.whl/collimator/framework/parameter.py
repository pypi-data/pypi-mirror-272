# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import ast
from collections import defaultdict
import dataclasses
import enum
from typing import Union

from jax import Array
from jax.flatten_util import ravel_pytree
import jax.numpy as jnp
import numpy as np

from .error import ParameterError


from ..backend.typing import ArrayLike, DTypeLike, ShapeLike


class ParameterExpr(list):
    pass


class Ops(enum.Enum):
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    FLOORDIV = enum.auto()
    MOD = enum.auto()
    POW = enum.auto()
    NEG = enum.auto()
    POS = enum.auto()
    ABS = enum.auto()
    EQ = enum.auto()
    NE = enum.auto()
    LT = enum.auto()
    LE = enum.auto()
    GT = enum.auto()
    GE = enum.auto()
    MATMUL = enum.auto()


__OPS_FN__ = {
    Ops.ADD: lambda x, y: x + y,
    Ops.SUB: lambda x, y: x - y,
    Ops.MUL: lambda x, y: x * y,
    Ops.DIV: lambda x, y: x / y,
    Ops.FLOORDIV: lambda x, y: x // y,
    Ops.MOD: lambda x, y: x % y,
    Ops.POW: lambda x, y: x**y,
    Ops.NEG: lambda x: -x,
    Ops.POS: lambda x: +x,
    Ops.ABS: abs,
    Ops.EQ: lambda x, y: x == y,
    Ops.NE: lambda x, y: x != y,
    Ops.LT: lambda x, y: x < y,
    Ops.LE: lambda x, y: x <= y,
    Ops.GT: lambda x, y: x > y,
    Ops.GE: lambda x, y: x >= y,
    Ops.MATMUL: lambda x, y: x @ y,
}

__OPS_STR__ = {
    Ops.ADD: "+",
    Ops.SUB: "-",
    Ops.MUL: "*",
    Ops.DIV: "/",
    Ops.FLOORDIV: "//",
    Ops.MOD: "%",
    Ops.POW: "**",
    Ops.NEG: "-",
    Ops.POS: "+",
    Ops.ABS: "abs",
    Ops.EQ: "==",
    Ops.NE: "!=",
    Ops.LT: "<",
    Ops.LE: "<=",
    Ops.GT: ">",
    Ops.GE: ">=",
    Ops.MATMUL: "@",
}


class _VarRecorder(ast.NodeVisitor):
    """Used to record all variables in a Python expression."""

    def __init__(self):
        super().__init__()
        self.vars = set()

    def visit_Name(self, node):
        self.vars.add(node.id)
        return node.id


ArrayLikeTypes = (
    Array,  # JAX array type
    np.ndarray,  # NumPy array type
    np.bool_,
    np.number,  # NumPy scalar types
    bool,
    int,
    float,
    complex,  # Python scalar types
)


def resolve_parameters(python_expr: str, env: dict):
    # look for variables used in the expression
    tree = ast.parse(python_expr, mode="eval")
    var_recorder = _VarRecorder()
    var_recorder.visit(tree.body)

    # record the parameters and resolve them
    parameters = set()
    resolved_params = {}
    for var in var_recorder.vars:
        if var in env:
            if isinstance(env[var], Parameter):
                parameters.add(env[var])
                resolved_params[var] = env[var].get()

    return parameters, resolved_params


def _resolve_array_like(value: ArrayLike) -> ArrayLike:
    vals = []
    if value.ndim == 0:
        return value
    for val in value:
        if isinstance(val, Parameter):
            vals.append(ParameterCache.__compute__(val))
        else:
            vals.append(_resolve_array_like(val))

    numeric_types = (int, float, complex, np.number, bool)
    is_numeric = all(isinstance(v, numeric_types) for v in vals)
    if not is_numeric:
        return vals

    return np.array(vals)


def _list_to_str(lst):
    str_repr = []
    for val in lst:
        if isinstance(val, list):
            str_repr.append(_list_to_str(val))
        else:
            str_repr.append(str(val))
    return f"[{', '.join(str_repr)}]"


def _tuple_to_str(tpl):
    str_repr = []
    for val in tpl:
        if isinstance(val, tuple):
            str_repr.append(_tuple_to_str(val))
        else:
            str_repr.append(str(val))
    if len(str_repr) == 1:
        return f"({str_repr[0]},)"
    return f"({', '.join(str_repr)})"


def _compute_list(tpl, is_tuple):
    new_lst = []
    for val in tpl:
        if isinstance(val, Parameter):
            new_lst.append(val.get())
        elif isinstance(val, list):
            new_lst.append(_compute_list(val, is_tuple=False))
        elif isinstance(val, tuple):
            new_lst.append(_compute_list(val, is_tuple=True))
        else:
            new_lst.append(val)
    if is_tuple:
        return tuple(new_lst)
    return new_lst


def _add_dependents(lst, param):
    for val in lst:
        if isinstance(val, Parameter):
            ParameterCache.add_dependent(val, param)
        elif isinstance(val, (list, tuple)):
            _add_dependents(val, param)


def _array_to_str(arr):
    if isinstance(arr, Parameter):
        return str(arr)
    if isinstance(arr, str):
        return f'"{arr}"'
    if arr.ndim == 0:
        return str(arr.item())
    arr = [_array_to_str(v) for v in arr]
    arr = ", ".join(arr)
    return f"np.array([{arr}])"


def _value_as_str(value):
    if isinstance(value, ArrayLikeTypes):
        if isinstance(value, (Array, np.ndarray)):
            return _array_to_str(value)
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, np.number):
            dtype = value.dtype
            return f"np.{dtype}({value.item()})"
        return str(value)

    if isinstance(value, ParameterExpr):
        i = 0
        str_repr = []
        while i < len(value):
            val = value[i]
            if isinstance(val, Parameter):
                val_str = val.name if val.name is not None else str(val)
                if isinstance(val.value, ParameterExpr):
                    val_str = f"({val_str})"
                str_repr.append(val_str)
            elif isinstance(val, Ops):
                if val in (Ops.NEG, Ops.POS, Ops.ABS):
                    if i + 1 >= len(value):
                        raise ValueError()
                    next_val = value[i + 1]
                    if val is Ops.ABS:
                        str_repr.append(f"abs({next_val})")
                    elif val is Ops.NEG:
                        str_repr.append(f"-{next_val}")
                    elif val is Ops.POS:
                        str_repr.append(f"+{next_val}")
                    i += 1
                else:
                    str_repr.append(__OPS_STR__[val])
            elif isinstance(val, (Array, np.ndarray)):
                str_repr.append(f"np.array({val.tolist()})")
            else:
                str_repr.append(str(val))
            i += 1

        t = " ".join(str_repr)
        return t

    if isinstance(value, list):
        return _list_to_str(value)

    if isinstance(value, tuple):
        return _tuple_to_str(value)

    if isinstance(value, str):
        return value

    if value is None:
        return ""

    # if is a Pytree
    try:
        value, _ = ravel_pytree(value)
        return _value_as_str(value)
    except BaseException:
        # Not a pytree
        pass

    return str(value)


class ParameterCache:
    __dependents__: dict["Parameter", set["Parameter"]] = {}
    __cache__: dict["Parameter", ArrayLike] = {}
    __is_dirty__ = defaultdict(lambda: True)

    @classmethod
    def get(cls, param: "Parameter") -> ArrayLike:
        if cls.__is_dirty__[param]:
            cls.__cache__[param] = cls.__compute__(param)
            cls.__is_dirty__[param] = False

        return cls.__cache__[param]

    @classmethod
    def replace(cls, param: "Parameter", value: ArrayLike):
        # TODO: update dependencies of this parameter
        param.value = value
        cls.__invalidate__(param)

    @classmethod
    def remove(cls, param: "Parameter"):
        for dependents in cls.__dependents__.values():
            if param in dependents:
                dependents.remove(param)

        if param in cls.__dependents__:
            del cls.__dependents__[param]
        if param in cls.__cache__:
            del cls.__cache__[param]
        if param in cls.__is_dirty__:
            del cls.__is_dirty__[param]

    @classmethod
    def add_dependent(cls, param: "Parameter", dependent: "Parameter"):
        cls.__dependents__[param].add(dependent)

    @classmethod
    def __invalidate__(cls, param: "Parameter"):
        cls.__cache__[param] = None
        cls.__is_dirty__[param] = True
        for dependent in cls.__dependents__[param]:
            cls.__invalidate__(dependent)

    @classmethod
    def __compute__(cls, param: "Parameter"):
        if isinstance(param.value, ParameterExpr):
            acc = None
            right_value = None
            op = None
            i = 0

            while i < len(param.value):
                val = param.value[i]

                if isinstance(val, Parameter):
                    right_value = val.get()
                elif isinstance(val, ArrayLikeTypes):
                    right_value = val
                elif isinstance(val, Ops):
                    if val in (Ops.NEG, Ops.POS, Ops.ABS):
                        if i + 1 >= len(param.value):
                            raise ParameterError(
                                param, message="Invalid parameter value"
                            )
                        if isinstance(param.value[i + 1], Parameter):
                            right_value = __OPS_FN__[val](param.value[i + 1].get())
                        elif isinstance(param.value[i + 1], ArrayLikeTypes):
                            right_value = __OPS_FN__[val](param.value[i + 1])
                        else:
                            raise ParameterError(
                                param,
                                message=f"Invalid value in parameter list: {param.value[i + 1]} of type {type(param.value[i + 1])}",
                            )
                        i += 1
                    else:
                        op = val
                else:
                    raise ParameterError(
                        param,
                        message=f"Invalid value in parameter list: {val} of type {type(val)}",
                    )

                if acc is not None and right_value is not None and op is not None:
                    acc = __OPS_FN__[op](acc, right_value)
                    op = None
                    right_value = None
                elif right_value is not None:
                    acc = right_value
                    right_value = None
                i += 1

            if acc is not None:
                return acc
            if right_value is not None:
                return right_value
            raise ParameterError(param, message="Invalid parameter value")

        if isinstance(param.value, Parameter):
            return cls.__compute__(param.value)

        if isinstance(param.value, tuple):
            t = _compute_list(param.value, is_tuple=True)
            return t

        if isinstance(param.value, list):
            t = _compute_list(param.value, is_tuple=False)
            return t

        if isinstance(param.value, np.ndarray):
            vals = _resolve_array_like(param.value)
            return np.array(vals, dtype=param.value.dtype)

        if isinstance(param.value, Array):
            vals = _resolve_array_like(param.value)
            if param.value.weak_type:
                return jnp.array(vals)
            return jnp.array(vals, dtype=param.value.dtype)

        if isinstance(param.value, np.number):
            if isinstance(param.value.item(), Parameter):
                return type(param.value)(cls.__compute__(param.value.item()))
            return param.value

        if isinstance(param.value, str) and param.is_python_expr:
            _, params_in_global_resolved = resolve_parameters(
                param.value, param.globals_
            )
            _, params_in_local_resolved = resolve_parameters(param.value, param.locals_)
            resolved_parameters = {
                **params_in_global_resolved,
                **params_in_local_resolved,
            }
            return eval(
                param.value, param.globals_, {**param.locals_, **resolved_parameters}
            )

        return param.value


def _op(op: Ops, left, right):
    param = Parameter(
        value=ParameterExpr([left, op, right]),
    )
    if isinstance(left, Parameter):
        ParameterCache.add_dependent(left, param)
    if isinstance(right, Parameter):
        ParameterCache.add_dependent(right, param)
    return param


@dataclasses.dataclass
class Parameter:
    value: Union[ParameterExpr, "Parameter", ArrayLike, str, tuple]
    dtype: DTypeLike = None
    shape: ShapeLike = None

    # name is used by reference submodels, model parameters and init script
    # variables so that they can be referred to in other fields
    # (we need this for serialization).
    name: str = None

    # For complex parameter values, we can specify a Python expression as string
    # This is useful for expressions like "np.eye(p)" where p is a parameter.
    is_python_expr: bool = False
    globals_: dict = None
    locals_: dict = None

    def get(self):
        return ParameterCache.get(self)

    def set(self, value: Union["Parameter", ArrayLike, str, tuple]):
        ParameterCache.replace(self, value)

    def __post_init__(self):
        if isinstance(self.value, Parameter):
            ParameterCache.add_dependent(self.value, self)
        if isinstance(self.value, ParameterExpr):
            for val in self.value:
                if isinstance(val, Parameter):
                    ParameterCache.add_dependent(val, self)
        if isinstance(self.value, (list, tuple)):
            _add_dependents(self.value, self)

        ParameterCache.__dependents__[self] = set()

    def __add__(self, other):
        return _op(Ops.ADD, self, other)

    def __radd__(self, other):
        return _op(Ops.ADD, other, self)

    def __sub__(self, other):
        return _op(Ops.SUB, self, other)

    def __rsub__(self, other):
        return _op(Ops.SUB, other, self)

    def __mul__(self, other):
        return _op(Ops.MUL, self, other)

    def __rmul__(self, other):
        return _op(Ops.MUL, other, self)

    def __truediv__(self, other):
        return _op(Ops.DIV, self, other)

    def __rtruediv__(self, other):
        return _op(Ops.DIV, other, self)

    def __floordiv__(self, other):
        return _op(Ops.FLOORDIV, self, other)

    def __rfloordiv__(self, other):
        return _op(Ops.FLOORDIV, other, self)

    def __mod__(self, other):
        return _op(Ops.MOD, self, other)

    def __rmod__(self, other):
        return _op(Ops.MOD, other, self)

    def __pow__(self, other):
        return _op(Ops.POW, self, other)

    def __rpow__(self, other):
        return _op(Ops.POW, other, self)

    def __neg__(self):
        p = Parameter(value=ParameterExpr([Ops.NEG, self]))
        ParameterCache.add_dependent(self, p)
        return p

    def __pos__(self):
        p = Parameter(value=ParameterExpr([Ops.POS, self]))
        ParameterCache.add_dependent(self, p)
        return p

    def __abs__(self):
        p = Parameter(value=ParameterExpr([Ops.ABS, self]))
        ParameterCache.add_dependent(self, p)
        return p

    def __eq__(self, other):
        return _op(Ops.EQ, self, other)

    def __ne__(self, other):
        return _op(Ops.NE, self, other)

    def __lt__(self, other):
        return _op(Ops.LT, self, other)

    def __le__(self, other):
        return _op(Ops.LE, self, other)

    def __gt__(self, other):
        return _op(Ops.GT, self, other)

    def __ge__(self, other):
        return _op(Ops.GE, self, other)

    def __del__(self):
        ParameterCache.remove(self)

    def __hash__(self):
        return id(self)

    def __str__(self):
        if self.name is not None:
            return self.name

        return self.value_as_str()

    def __matmul__(self, other):
        return _op(Ops.MATMUL, self, other)

    def __int__(self):
        if self.dtype is not None:
            return self.dtype(self.get())
        return int(self.get())

    def __float__(self):
        if self.dtype is not None:
            return self.dtype(self.get())
        return float(self.get())

    # FIXME: this is not working as expected - it will break some tests
    # def __bool__(self):
    #     return bool(self.get())

    def __complex__(self):
        return complex(self.get())

    def value_as_str(self):
        """Used for serialization of parameters. This string is displayed in the
        UI text fields for the parameters."""
        try:
            return _value_as_str(self.value)
        except ValueError as e:
            raise ParameterError(
                self, message=f"Invalid parameter value: {self.value}"
            ) from e

    def __repr__(self):
        return f"Parameter(name={self.name}, value={self.value_as_str()}, value_type={type(self.value)})"
