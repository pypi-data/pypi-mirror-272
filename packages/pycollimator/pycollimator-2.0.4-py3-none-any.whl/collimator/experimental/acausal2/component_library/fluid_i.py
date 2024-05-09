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
from dataclasses import dataclass
from enum import Enum

"""
fluid_i stantds for fluid incompressible, e.g. water, hydraulic fluid, etc. when operating
under conditions where their compressibility can be neglected.

The concepts are heavily based on these sources:
Modelica Fluids library
https://doc.modelica.org/Modelica%204.0.0/Resources/helpDymola/Modelica_Fluid.html#Modelica.Fluid

Modelica Stream connectors concepts:
https://doc.modelica.org/Modelica%204.0.0/Resources/Documentation/Fluid/Stream-Connectors-Overview-Rationale.pdf
This stream thing seems potentially over complicated for the first attempt.

I'll try to just do the naive thing first.

we will need some global way to define fluid properties. for now I'm creating dataclass type objects.
to define the fluid for a given fluid network, the user instantiates a dataclass, and passes it to
the eqn_env constructor like this:
    from base import eqn_env
    from .fluid_i import FluidPropWater
    ev = eqn_env(fluid=FluidPropWater())
"""


class FluidName(Enum):
    water = 0
    hydraulic_fluid = 1


@dataclass
class Water:
    name = "water"
    density = 1000  # kg/m**3
    viscosity = 0.89  # mPa*s


@dataclass
class HydraulicFluid:
    # FIXME wrong property values, just example for now to show how different fluids can be defined.
    name = "hydraulic_fluid"
    density = 1000  # kg/m**3
    viscosity = 0.89  # mPa*s


class Fluid:
    def __init__(self, fluid="water"):
        if fluid == FluidName.water:
            fp = Water()
        elif fluid == FluidName.hydraulic_fluid:
            fp = HydraulicFluid()
        else:
            raise ValueError(
                f"Fluid class, {fluid} is incorrect input for arg 'fluid'."
            )

        self.density = Sym(
            name=fp.name + "_density",
            kind=SymKind.param,
            val=fp.density,
        )
        self.viscosity = Sym(
            name=fp.name + "_viscosity",
            kind=SymKind.param,
            val=fp.viscosity,
        )


# flow variable:Units = mass_flow_rate:kg/second
# potential variable:Units = pressure:MPa
class FluidPort(PortBase):
    """
    port for a fluid component to interface with others.
    """

    def __init__(self, P_sym=None, M_sym=None):
        self.domain = Domain.fluid
        self.pot = P_sym
        self.flow = M_sym


class FluidOnePort(ComponentBase):
    """
    Fluid domain component with 1 port.
    Incomplete component.
    """

    def __init__(self, eqn_env, name, P_ic=None, p="port"):
        self.P = Sym(eqn_env, name + "_P", kind=SymKind.pot, ic=P_ic)
        self.M = Sym(eqn_env, name + "_M", kind=SymKind.flow)

        self.ports = {p: FluidPort(P_sym=self.P, M_sym=self.M)}
        self.syms = set([self.P, self.M])
        self.eqs = set()


class Fluid2Port(ComponentBase):
    """
    Fluid domain component with 2 ports.
    Incomplete component.
    """

    def __init__(self, eqn_env, name, p1="port_a", p2="port_b"):
        self.P1 = Sym(eqn_env, name + "_P1", kind=SymKind.pot)
        self.P2 = Sym(eqn_env, name + "_P2", kind=SymKind.pot)
        self.M1 = Sym(eqn_env, name + "_M1", kind=SymKind.flow)
        self.M2 = Sym(eqn_env, name + "_M2", kind=SymKind.flow)
        self.dP = Sym(eqn_env, name + "_dP", kind=SymKind.var)

        self.ports = {
            p1: FluidPort(P_sym=self.P1, M_sym=self.M1),
            p2: FluidPort(P_sym=self.P2, M_sym=self.M2),
        }

        self.syms = set([self.P1, self.P2, self.M1, self.M2, self.dP])
        self.eqs = set(
            [
                Eqn(e=Eq(self.dP.s, self.P1.s - self.P2.s), kind=EqnKind.comp),
            ]
        )


class PressureSource(FluidOnePort):
    """
    ideal pressure source in fluid domain
    """

    def __init__(self, eqn_env, name=None, pressure=0.1, enable_pressure_input=False):
        self.name = "fps" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_pressure_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = pressure

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Pparam = Sym(eqn_env, self.name + "_Pparam", kind=kind, val=val)
        self.syms.add(self.Pparam)

        # pressure source equality
        self.eqs.add(Eqn(e=Eq(self.P.s, self.Pparam.s), kind=EqnKind.comp))


class MassflowSource(FluidOnePort):
    """
    ideal mass flow source in fluid domain
    """

    def __init__(self, eqn_env, name=None, M=1.0, enable_massflow_input=False):
        self.name = "ths" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_massflow_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = M

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Mparam = Sym(eqn_env, self.name + "_Mparam", kind=kind, val=val)
        self.syms.add(self.Mparam)

        # pressure source equality
        self.eqs.add(Eqn(e=Eq(self.M.s, self.Mparam.s), kind=EqnKind.comp))


class Pipe(Fluid2Port):
    """
    Simple pipe in fluid domain.
    The R is the resitance to mass flow, just like a resistor in electrical domain.
    We could do better here by havign params for like diameter, wetted surface roughness, etc.
    But this is an acceptable starting point.
    """

    def __init__(self, eqn_env, name=None, R=1.0):
        self.name = "fpipe" if name is None else name
        super().__init__(eqn_env, self.name)

        if R <= 0.0:
            raise ValueError(f"Component Pipe {self.name} must have R>0")

        self.R = Sym(eqn_env, self.name + "_R", kind=SymKind.param, val=R)
        self.syms.add(self.R)

        # does not store mass
        self.eqs.add(Eqn(e=Eq(0, self.M1.s + self.M2.s), kind=EqnKind.comp))

        # pressure drop equation. use Q1 due to sign convention
        self.eqs.add(Eqn(e=Eq(self.dP.s, self.R.s * self.M1.s)))


class Accumulator(FluidOnePort):
    """
    Accumulator in fluid domain. Pressure increases when mass flows in, and vice versa.
    relationship between internal pressure and mass flow is either spring law, of ideal gas law.
    There is no restrictor at the port, no pressure loss a fucntion of flow rate.

    for spring.
        mass_flow/(fluid.density) = der(V)
        force = (V/area)*k
        pressure = force/area

        V_init = f*area/k = pressure*area*area/k (N/m*m)*(m*m)*(m*m)/(N/m)->(N)*(m*m)/(N/m)->m**3
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        P_ic=0.0,
        area=1.0,
        k=1.0,
    ):
        self.name = "facc" if name is None else name

        if area <= 0.0:
            raise ValueError(f"Component Accumulator {self.name} must have area>0")
        if k <= 0.0:
            raise ValueError(f"Component Accumulator {self.name} must have k>0")

        super().__init__(eqn_env, self.name, P_ic=P_ic)
        V_ic = P_ic * area * area / k

        self.area = Sym(eqn_env, self.name + "_area", kind=SymKind.param, val=area)
        self.k = Sym(eqn_env, self.name + "_k", kind=SymKind.param, val=k)
        self.f = Sym(eqn_env, self.name + "_f", kind=SymKind.var)
        self.V = Sym(eqn_env, self.name + "_V", kind=SymKind.var, val=V_ic)
        self.dV = Sym(eqn_env, self.name + "_dV", kind=SymKind.var, int_sym=self.V)
        self.V.der_sym = self.dV
        self.syms.update(set([self.area, self.k, self.f, self.V, self.dV]))

        # pressure-force relationship
        self.eqs.add(Eqn(e=Eq(self.P.s, self.f.s / self.area.s), kind=EqnKind.comp))

        # force-volume relationship for 'spring' accumulator.
        self.eqs.add(
            Eqn(e=Eq(self.f.s, self.V.s * self.k.s / self.area.s), kind=EqnKind.comp)
        )

        # volume-mass_flow relationship.
        self.eqs.add(
            Eqn(
                e=Eq(self.dV.s, self.M.s / eqn_env.fluid.density.s),
                kind=EqnKind.comp,
            )
        )


class Pump(Fluid2Port):
    """
    Ideal pump in the fluid domain.

    Pump has a maximum pressure differential, dP_max, which it can produce.
    Therefore, the max outlet pressure is dP_max - P_in.
    Pump has some input power, pwr, which is a causal input signal,
    that represents the external work doesn't by the pump on the fluid
    system.
    Pump has some performance coefficient that converts dP*pwr to mass_flow,
    CoP, which has units of kg*s*MPa/Watt.
        mass_flow = pwr * CoP / ((dP_max - Pin) - P_out) [1]
        but dP = P_out - P_in -> P_out = dP + P_in [2]
    subing [2] into [1] and rearranging:
        mass_flow = pwr * CoP / (dP_max - dP)

    Note on sign convention.
    Pump component has 2 ports: p1=inlet and p2=outlet.
    mass_flow is defined as positive going into the comnponent.
    Therefore the inlet mass_flow is positive when pump operating normally.

    """

    def __init__(
        self,
        eqn_env,
        name=None,
        dPmax=1.0,
        CoP=1.0,
    ):
        self.name = "fpmp" if name is None else name

        if dPmax <= 0.0:
            raise ValueError(f"Component Pump {self.name} must have dPmax>0")
        if CoP <= 0.0:
            raise ValueError(f"Component Pump {self.name} must have CoP>0")

        super().__init__(eqn_env, self.name)
        self.dPmax = Sym(eqn_env, self.name + "_dPmax", kind=SymKind.param, val=dPmax)
        self.CoP = Sym(eqn_env, self.name + "_CoP", kind=SymKind.param, val=CoP)
        self.pwr = Sym(eqn_env, self.name + "_pwr", kind=SymKind.inp)
        self.syms.update(set([self.dPmax, self.CoP, self.pwr]))

        # does not store mass
        self.eqs.add(Eqn(e=Eq(0, self.M1.s + self.M2.s), kind=EqnKind.comp))

        # pressure-mass_flow relationship.
        self.eqs.add(
            Eqn(
                e=Eq(self.M1.s, self.pwr.s * self.CoP.s / (self.dPmax.s - self.dP.s)),
                kind=EqnKind.comp,
            )
        )
