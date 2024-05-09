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

from sympy import Eq
from .base import Sym, Eqn, PortBase, ComponentBase, Domain, SymKind, EqnKind
from .thermal import ThermalOnePort

"""
Discussion on the design of the electrical components relative to Modelica Standard Library (MLS).

MSL Pin.mo defines the I(flow), and V(potential). We do the similar in ElecPort, but the symbols are passed in from
the component, so we get I1, I2, V1, V2.

MSL TwoPin.mo and OnePort.mo define the component I and V symbols. We do similar, but define V in Elec2Pin,
and use the I1 from component for I.

In this way, the Resistor and Capacitor end up with essetially an analogous set of symbols, and
an equivalent set of equations relative to the MSL components.
"""


# flow variable:Units = current:Amps
# potential variable:Units = voltage:Volts
class ElecPort(PortBase):
    """
    port for a electrical component to interface with others.
    """

    def __init__(self, V_sym=None, I_sym=None):
        self.domain = Domain.elec
        self.pot = V_sym
        self.flow = I_sym


class Elec2Pin(ComponentBase):
    """
    electrical domain component with 2 pins.
    Incomplete component.
    """

    # FIXME: this should also have an I_ic to set the current initial value.
    def __init__(self, eqn_env, name, V_ic=None, p1="p", p2="n"):
        self.V = Sym(eqn_env, name + "_V", kind=SymKind.var, ic=V_ic)
        self.V1 = Sym(eqn_env, name + "_V1", kind=SymKind.pot)
        self.V2 = Sym(eqn_env, name + "_V2", kind=SymKind.pot)
        self.I1 = Sym(eqn_env, name + "_I1", kind=SymKind.flow)
        self.I2 = Sym(eqn_env, name + "_I2", kind=SymKind.flow)

        self.ports = {
            p1: ElecPort(V_sym=self.V1, I_sym=self.I1),
            p2: ElecPort(V_sym=self.V2, I_sym=self.I2),
        }

        self.syms = set([self.V, self.V1, self.V2, self.I1, self.I2])
        self.eqs = set(
            [
                Eqn(e=Eq(self.V1.s - self.V2.s, self.V.s), kind=EqnKind.comp),
                Eqn(e=Eq(0, self.I1.s + self.I2.s), kind=EqnKind.comp),
            ]
        )


class VoltageSource(Elec2Pin):
    """
    ideal constant voltage source in electrical domain
    """

    def __init__(self, eqn_env, name=None, V=1.0, enable_voltage_port=False, **kwargs):
        self.name = "evs" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_voltage_port:
            # bit of a HACK here. is_fcn=False is used to override having this be a Sympy.Function
            # symbol like Vin(t), makes it just a Sympy.Symbol.
            # the reason is that lamdify doesn't like havinf Sympy.Function types in it's args
            self.Vin = Sym(eqn_env, self.name + "_Vin", kind=SymKind.inp)
        else:
            self.Vin = Sym(eqn_env, self.name + "_Vin", kind=SymKind.param, val=V)

        self.syms.add(self.Vin)
        self.eqs.add(Eqn(e=Eq(self.V.s, self.Vin.s)))

    # @am. it would be nice to be able to do it like shown below, but this isn't working, and not
    # worth our time right now.
    # def __init__(self, eqn_env, name=None, V=1.0, enable_voltage_port=False):
    #     self.name = "ecv" if name is None else name
    #     super().__init__(eqn_env, self.name)

    #     # in this case we are modifying the attribues of a symbol with kind=var,
    #     # so no need to create a new symbol to avoid changes to potential or flow variables.
    #     if enable_voltage_port:
    #         self.V.kind = SymKind.inp
    #         self.V.val = None
    #     else:
    #         self.V.kind = SymKind.param
    #         self.V.val = V


class Ground(ComponentBase):
    """
    *ground* reference in electrical domain.

    Note: the only 'single' pin component in electrical domain.
    """

    def __init__(self, eqn_env, name=None):
        self.name = "er" if name is None else name

        self.I = Sym(eqn_env, self.name + "_I", kind=SymKind.flow)  # noqa
        self.V = Sym(eqn_env, self.name + "_V", kind=SymKind.pot)
        self.dV = Sym(eqn_env, self.name + "_dV", kind=SymKind.var, int_sym=self.V)

        self.ports = {"p": ElecPort(V_sym=self.V, I_sym=self.I)}
        self.syms = set([self.I, self.V, self.dV])
        self.eqs = set(
            [
                Eqn(e=Eq(0, self.dV.s), kind=EqnKind.comp),
                Eqn(e=Eq(0, self.V.s), kind=EqnKind.comp),
                Eqn(e=Eq(0, self.I.s), kind=EqnKind.comp),
            ]
        )


class Resistor(Elec2Pin):
    """
    ideal resistor in electrical domain
    """

    def __init__(self, eqn_env, name=None, R=1.0, enable_heat_port=False):
        self.name = "er" if name is None else name
        super().__init__(eqn_env, self.name)

        if R <= 0.0:
            raise ValueError(f"Component Resistor {self.name} must have R>0")

        self.R = Sym(eqn_env, self.name + "_R", kind=SymKind.param, val=R)
        self.syms.add(self.R)
        self.eqs.add(Eqn(e=Eq(self.V.s, self.I1.s * self.R.s), kind=EqnKind.comp))

        if enable_heat_port:
            self.heat = ThermalOnePort(eqn_env, self.name, p="heat")

            self.ports.update(self.heat.ports)
            self.syms.update(self.heat.syms)
            self.eqs.add(
                Eqn(
                    e=Eq(self.heat.Q.s, self.I1.s * self.I1.s * self.R.s),
                    kind=EqnKind.comp,
                )
            )


class Capacitor(Elec2Pin):
    """
    ideal capacitor in electrical domain
    """

    def __init__(self, eqn_env, name=None, C=1.0, initial_voltage=0.0):
        self.name = "ec" if name is None else name

        if C <= 0.0:
            raise ValueError(f"Component Capacitor {self.name} must have C>0")

        super().__init__(eqn_env, self.name, V_ic=initial_voltage)
        self.C = Sym(eqn_env, self.name + "_C", kind=SymKind.param, val=C)
        self.dV = Sym(eqn_env, self.name + "_dV", kind=SymKind.var, int_sym=self.V)
        self.V.der_sym = self.dV
        self.syms.update(set([self.C, self.dV]))
        self.eqs.add(Eqn(e=Eq(self.I1.s, self.C.s * self.dV.s), kind=EqnKind.comp))


class Inductor(Elec2Pin):
    """
    ideal inductor in electrical domain
    """

    def __init__(self, eqn_env, name=None, L=1.0, V_ic=0.0):
        self.name = "ei" if name is None else name

        if L <= 0.0:
            raise ValueError(f"Component Inductor {self.name} must have L>0")

        super().__init__(eqn_env, self.name)
        self.L = Sym(eqn_env, self.name + "_L", kind=SymKind.param, val=L)
        self.dI = Sym(eqn_env, self.name + "_dI", kind=SymKind.var, int_sym=self.I1)
        self.I1.der_sym = self.dI
        self.syms.update(set([self.L, self.dI]))
        self.eqs.add(Eqn(e=Eq(self.V.s, self.L.s * self.dI.s), kind=EqnKind.comp))


class VoltageSensor(ComponentBase):
    """
    ideal voltage sensor in electrical domain
    """

    def __init__(self, eqn_env, name=None, p1="p", p2="n"):
        self.name = "evs" if name is None else name
        self.Vout = Sym(eqn_env, self.name + "_Vout", kind=SymKind.outp)
        self.V1 = Sym(eqn_env, self.name + "_V1", kind=SymKind.pot)
        self.V2 = Sym(eqn_env, self.name + "_V2", kind=SymKind.pot)

        self.ports = {
            p1: ElecPort(V_sym=self.V1),
            p2: ElecPort(V_sym=self.V2),
        }

        self.syms = set([self.Vout, self.V1, self.V2])
        self.eqs = set(
            [
                Eqn(e=Eq(self.V1.s - self.V2.s, self.Vout.s)),
            ]
        )

        # although the UI shows this block with 2 ports on the left side
        # here the causal port (the voltage input) is defined using the
        # Vout variable and its corresponding equation. So this map only
        # needs toie two acaual ports.
        self.port_idx_to_name = {-1: p1, 1: p2}
