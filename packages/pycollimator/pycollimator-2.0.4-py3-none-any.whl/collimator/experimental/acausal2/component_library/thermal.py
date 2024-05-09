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


# flow variable:Units = heat_flux:Joules/second
# potential variable:Units = temperature:Kelvin
class ThermPort(PortBase):
    """
    port for a thermal component to interface with others.
    """

    def __init__(self, T_sym=None, Q_sym=None):
        self.domain = Domain.thermal
        self.pot = T_sym
        self.flow = Q_sym


class ThermalOnePort(ComponentBase):
    """
    a partial component with one thermal connection.
    """

    def __init__(self, eqn_env, name, T_ic=None, p="port"):
        self.T = Sym(eqn_env, name + "_T", kind=SymKind.pot, ic=T_ic)
        self.Q = Sym(eqn_env, name + "_Q", kind=SymKind.flow)

        self.ports = {p: ThermPort(T_sym=self.T, Q_sym=self.Q)}
        self.syms = set([self.T, self.Q])
        self.eqs = set()


class Therm2Port(ComponentBase):
    """
    thermal domain component with 2 pins.
    Incomplete component.
    """

    def __init__(self, eqn_env, name, p1="port_a", p2="port_b"):
        self.T1 = Sym(eqn_env, name + "_T1", kind=SymKind.pot)
        self.T2 = Sym(eqn_env, name + "_T2", kind=SymKind.pot)
        self.Q1 = Sym(eqn_env, name + "_Q1", kind=SymKind.flow)
        self.Q2 = Sym(eqn_env, name + "_Q2", kind=SymKind.flow)
        self.dT = Sym(eqn_env, name + "_dT", kind=SymKind.var)

        self.ports = {
            p1: ThermPort(T_sym=self.T1, Q_sym=self.Q1),
            p2: ThermPort(T_sym=self.T2, Q_sym=self.Q2),
        }

        self.syms = set([self.T1, self.T2, self.Q1, self.Q2, self.dT])
        self.eqs = set(
            [
                Eqn(e=Eq(self.dT.s, self.T1.s - self.T2.s), kind=EqnKind.comp),
            ]
        )


class TemperatureSource(ThermalOnePort):
    """
    ideal constant temperature source in thermal domain
    """

    def __init__(self, eqn_env, name=None, temperature=300.0, enable_temp_input=False):
        self.name = "tts" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_temp_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = temperature

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Tparam = Sym(eqn_env, self.name + "_Tparam", kind=kind, val=val)
        self.syms.add(self.Tparam)

        # temperature source equality
        self.eqs.add(Eqn(e=Eq(self.T.s, self.Tparam.s), kind=EqnKind.comp))


class HeatFlowSource(ThermalOnePort):
    """
    ideal constant heat flux source in thermal domain
    """

    def __init__(self, eqn_env, name=None, Q=1.0, enable_heat_input=False):
        self.name = "ths" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_heat_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = Q

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Qparam = Sym(eqn_env, self.name + "_Qparam", kind=kind, val=val)
        self.syms.add(self.Qparam)

        # heat source equality
        self.eqs.add(Eqn(e=Eq(self.Q.s, self.Qparam.s), kind=EqnKind.comp))


class ThermalResistor(Therm2Port):
    """
    ideal resistor(insulator) in thermal domain
    """

    def __init__(self, eqn_env, name=None, R=1.0):
        self.name = "tr" if name is None else name
        super().__init__(eqn_env, self.name)

        if R <= 0.0:
            raise ValueError(f"Component ThermalResistor {self.name} must have R>0")

        self.R = Sym(eqn_env, self.name + "_R", kind=SymKind.param, val=R)
        self.syms.add(self.R)

        # does not store energy
        self.eqs.add(Eqn(e=Eq(0, self.Q1.s + self.Q2.s), kind=EqnKind.comp))

        # thermal conduction equation. use Q1 due to sign convention
        self.eqs.add(Eqn(e=Eq(self.dT.s, self.R.s * self.Q1.s)))


class HeatCapacitor(ThermalOnePort):
    """
    ideal capacitor(thermal mass) in thermal domain
    """

    def __init__(self, eqn_env, name=None, C=1.0, T_ic=0.0):
        self.name = "tc" if name is None else name

        if C <= 0.0:
            raise ValueError(f"Component HeatCapacitor {self.name} must have C>0")

        super().__init__(eqn_env, self.name, T_ic=T_ic)
        self.C = Sym(eqn_env, self.name + "_C", kind=SymKind.param, val=C)
        self.derT = Sym(eqn_env, self.name + "_derT", kind=SymKind.var, int_sym=self.T)
        self.T.der_sym = self.derT
        self.syms.update(set([self.C, self.derT]))

        # energy relationship
        self.eqs.add(Eqn(e=Eq(self.Q.s, self.C.s * self.derT.s), kind=EqnKind.comp))
