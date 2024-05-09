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

import sympy as sp
from enum import Enum


class EqnEnv:
    def __init__(self, fluid=None):
        self.t = sp.symbols("t")
        self.fluid = fluid


class Domain(Enum):
    elec = 0
    magnetic = 1
    thermal = 2
    rotational = 3
    translational = 4
    fluid = 6


class SymKind(Enum):
    """
    'kind' qualifies the symbol w.r.t. how it gets treated when rearanging/simplifying
    equations, or determining initial conditions.

    'flow' means this symbol is a flow variable. it must appear in one and only one
    conservation equation for a given 'node'. e.g. all forces sum to 0.

    'pot' means this symbol is a potential variable. it must appear in at least one
    equality constraint. e.g. all velocities of ports connected to a 'node' must be equal.

    'param' means this symbol is a parameter of the system, e.g. mass, resistance, etc.

    'in' means this symbol is an input, similar to param, but the value is read in
    periodically. e.g. force signal for controlled_ideal_force_source.

    'out' means this symbol is a output and therefore must appear on the LHS of an
    expression. e.g. force value for ideal force sensor.

    'var' means this symbol is a variable of the system that does not match any description
    above. e.g. voltage_across_capacitor = capacitor_pot_positive - capacitor_pot_negative, here
    voltage_across_capacitor is a 'var', while the other two are 'pot'.
    similarly, the time derivaive of voltage_across_capacitor would be a 'var'.

    'node_pot' means this symbol is in the potential derivative index of the node. See
    AcausalCompiler.add_node_potential_eqs() for details.

    'lut' means the symbol represents a lookup table function
    """

    flow = 0
    pot = 1
    param = 2
    inp = 3
    outp = 4
    var = 6
    node_pot = 7
    lut = 8


# FIXME: move me to acausal framework?
class Sym:
    """
    A class for a symbol that can have an association with the symbols that are it's
    integral or derivative w.r.t. time.
    Although declare derivatives using Sympy.Symbol.diff method, this only creates the
    symbolic meaning of the derivative relationship, it doesn't simultaneously track
    the relationship in a way thta we can 'search through the graph' of derivative
    relationships.
    Creation of class means we can track many other attributes of symbols making
    equation manipulation easier and clearer.
    """

    def __init__(
        self,
        eqn_env=None,
        name=None,
        val=None,
        der_sym=None,
        int_sym=None,
        kind=None,
        ic=None,
        sym=None,
    ):
        if kind not in SymKind:
            raise Exception(f"kind:{kind} of symbol:{name} not one of {SymKind}")

        if kind == SymKind.param and val is None:
            raise Exception(f"symbol:{name} has kind param, val cannot be None")

        if kind in [SymKind.flow, SymKind.param, SymKind.inp, SymKind.outp]:
            if ic is not None:
                raise Warning(f"assigning ic to symbol if kind:{kind} has no effect.")

        # to capture all the conditions which would make the symbol a function of time.
        is_fcn = kind != SymKind.param

        self.der_relation = None  # equation relating the self.s symbol to the Sympy derivative it represents
        self.s_int = None  # the sympy.Derivative object that is the derivative of the int_sym passed in
        self.name = name
        if sym is not None:
            # this symbol has been defined externally
            self.s = sym
        elif int_sym is not None:
            # when this symbol is the derivative w.r.t. time of another symbol,
            # we have to define it as such.
            self.s = sp.Function(name)(eqn_env.t)
            self.s_int = int_sym.s.diff(eqn_env.t)
            # debatable whether this shuld happen in here or in the components.
            # it's more of a components equation, but if done there, it would
            # mean lots of repeated code, where as here it's automatic.
            # when done here, it means that the compiler.diagram_processing()
            # needs to collect equations from Sym objects as well.
            self.der_relation = Eqn(
                e=sp.Eq(self.s, self.s_int), kind=EqnKind.der_relation
            )

            # NOTE: For some domains, all der_relation equations come from node potential
            # variables. In thise cases, it would cleaner to add the der_relations in the
            # compiler. However, some domains have der_relations for non-node_pot variables,
            # so at least for now, it seems best to keep declaration of der_relations here.
        elif is_fcn:
            # when this symbol is a function of time, we have to define it as such.
            self.s = sp.Function(name)(eqn_env.t)
        else:
            # otherwise, the symbol is just a plain symbol with no other relations.
            self.s = sp.Symbol(name)
        self.val = val
        self.kind = kind
        self.ic = ic
        self.int_sym = int_sym
        self.der_sym = der_sym

    def __repr__(self):
        return str(self.s)

    def subs(self, e1, e2):
        self.s = self.s.subs(e1, e2)
        return self


class EqnKind(Enum):
    pot = 0
    flow = 1
    der_relation = 2
    comp = 3


# FIXME: move me to acausal framework?
class Eqn:
    """
    class for equations and their attributes
    """

    def __init__(self, e, kind=None, node_id=None):
        self.e = e
        self.kind = kind
        self.node_id = node_id  # not user settable. assign by 'AcausalCompiler'

    def subs(self, e1, e2):
        self.e = self.e.subs(e1, e2)
        return self

    def __repr__(self):
        if self.kind is None:
            return str(self.e)
        else:
            return (
                str(self.e) + ":\t\t\t" + str(self.kind) + "\tnid:" + str(self.node_id)
            )

    @property
    def expr(self):
        # return the equation, re-arranged as an expression equal to zero.
        return self.e.lhs - self.e.rhs


class PortBase:
    domain: [Domain] = None
    flow: str = None
    pot = None

    def __repr__(self):
        return str(
            self.__class__.__name__
            + " pot:"
            + str(self.pot)
            + " flow:"
            + str(self.flow)
        )


class ComponentBase:
    ports = {}
    syms = set()
    eqs = set()

    def __repr__(self):
        return str(self.__class__.__name__ + "_" + self.name)

    def get_in_sym(self):
        # FIXME: does not support component with multiple causal input
        for sym in self.syms:
            if sym.kind == SymKind.inp:
                return sym
        return None

    def get_out_sym(self):
        # FIXME: does not support component with multiple causal outputs
        for sym in self.syms:
            if sym.kind == SymKind.outp:
                return sym
        return None
