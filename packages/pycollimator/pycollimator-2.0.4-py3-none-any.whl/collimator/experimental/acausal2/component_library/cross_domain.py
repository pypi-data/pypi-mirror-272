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
from .base import Sym, Eqn, ComponentBase, SymKind, EqnKind
from .elec import Elec2Pin
from .rotational import MechRotOnePort
from .translational import MechTransOnePort, MechTransTwoPort
from .thermal import ThermalOnePort
from .fluid_i import Fluid2Port
import numpy as np

"""
Components that have ports in more than one domain.
e.g. an electric motor has Elec ports for + and -, MechRotational for it's output shaft,
and optionally a Thermal port for heat transfer.
"""


class Varistor(Elec2Pin):
    """
    resistor is function of lookup table: R = f(I)
    this is just a dummy component used for trialing lookup tables.
    this component should eventually be removed.
    """

    def __init__(self, eqn_env, name=None):
        self.name = "varistor" if name is None else name
        super().__init__(eqn_env, self.name)

        # create component specific lookup table function symbols
        self.r_i = Sym(
            eqn_env,
            self.name + "_r_i",
            kind=SymKind.param,
            val=np.array([0.0, 1.0, 2.0]),
        )
        self.r_r = Sym(
            eqn_env,
            self.name + "_r_r",
            kind=SymKind.param,
            val=np.array([1.0, 1.0, 2.0]),
        )
        r_lut_sym = sp.Function("interp")(
            self.I1.s,
            self.r_i.s,
            self.r_r.s,
        )
        self.r_lut = Sym(eqn_env, self.name + "_r_lut", sym=r_lut_sym, kind=SymKind.lut)
        self.syms.update({self.r_i, self.r_r, self.r_lut})
        self.eqs.add(
            Eqn(e=sp.Eq(self.V.s, self.I1.s * self.r_lut.s), kind=EqnKind.comp)
        )


class IdealMotor(ComponentBase):
    """
    Ideal 4-quadrant motor with no inertia. The governing equations:
        trq = K*I
        backEMF = E*w
        V - backEMF = I*R
    or as one equation:
        trq = K*(V - E*w)/R

    But the above 3 are more suitable to entering in Sympy.Eq.

    Note on efficiency. In this simple case, power loss is I*I*R,
    but this is not explicitly computed, unless the heat_port is enabled.

    Note on sign convention. We use I1 everywhere, to maintain consistent
    sign of the current in the equations.
    BackEFM and rotation velocity always have the same sign.
    Current and Torque always have the same sign.
    """

    def __init__(self, eqn_env, name=None, R=1.0, K=1.0, E=1.0, enable_heat_port=False):
        self.name = "mot" if name is None else name

        self.elec = Elec2Pin(eqn_env, self.name, p1="pos", p2="neg")
        self.shaft = MechRotOnePort(eqn_env, self.name, p="shaft")

        self.ports = {**self.elec.ports, **self.shaft.ports}
        self.syms = self.elec.syms | self.shaft.syms
        self.eqs = self.elec.eqs | self.shaft.eqs

        if R <= 0.0:
            raise ValueError(f"Component IdealMotor {self.name} must have R>0")
        if K <= 0.0:
            raise ValueError(f"Component IdealMotor {self.name} must have K>0")
        if E <= 0.0:
            raise ValueError(f"Component IdealMotor {self.name} must have E>0")

        self.R = Sym(eqn_env, self.name + "_R", kind=SymKind.param, val=R)
        self.K = Sym(eqn_env, self.name + "_K", kind=SymKind.param, val=K)
        self.E = Sym(eqn_env, self.name + "_E", kind=SymKind.param, val=E)
        self.backEMF = Sym(eqn_env, self.name + "_backEMF", kind=SymKind.var)
        self.syms.update({self.R, self.K, self.E, self.backEMF})
        self.eqs.update(
            {
                Eqn(
                    e=sp.Eq(self.shaft.t.s, self.K.s * self.elec.I1.s),
                    kind=EqnKind.comp,
                ),
                Eqn(
                    e=sp.Eq(self.backEMF.s, self.E.s * self.elec.I1.s),
                    kind=EqnKind.comp,
                ),
                Eqn(
                    e=sp.Eq(self.elec.V.s - self.backEMF.s, self.elec.I1.s * self.R.s),
                    kind=EqnKind.comp,
                ),
            }
        )

        if enable_heat_port:
            self.heat = ThermalOnePort(eqn_env, self.name, p="heat")

            self.ports.update(self.heat.ports)
            self.syms.update(self.heat.syms)
            self.eqs.update(
                {
                    Eqn(
                        e=sp.Eq(
                            self.heat.Q.s, self.elec.I1.s * self.elec.I1.s * self.R.s
                        ),
                        kind=EqnKind.comp,
                    ),
                }
            )


def process_peak_trq(
    name,
    peaktrq_spd=None,
    peaktrq_trq=None,
    peak_trq=None,
    peak_pwr=None,
):
    if peaktrq_spd is None:
        peaktrq_spd = np.arange(0, 1000, 50)
    if peaktrq_trq is None:
        if peak_pwr is None:
            peak_pwr = 100e3  # Watts
        if peak_trq is None:
            peak_trq = 200  # Nm
        peak_trq_v = np.ones_like(peaktrq_spd) * peak_trq  # Nm
        peak_pwrTrq_v = peak_pwr / np.minimum(peaktrq_spd, 1.0)  # Nm
        peaktrq_trq = np.minimum(peak_trq_v, peak_pwrTrq_v)

    return peaktrq_spd, peaktrq_trq


class BLDC(ComponentBase):
    """
    This is still WIP. Not tested.
    FIXME: equation 4 below is not implemented yet.
    Brushless Direct Current Motor (BLDC).
    Combined Motor-Inverter model for a 4 Quadrant BLDC motor. The governing equations:
        1. trq = min(trq_req, peaktrq_lut(speed))
        2. mech_pwr = trq * speed
        3. eff_1quad = eff_table(abs(trq),abs(speed))
        4. eff = if sign(trq*speed) > 0 then eff_1quad, else 1/eff_1quad
        5. elec_pwr = mech * eff
        6. I = elec_pwr/V
    optionally:
        7. heat = abs(elec_pwr - mech_pwr)

    This component requires the following lookup tables:
        peaktrq: 1D lookup from speed[0:inf] to trq[0:inf]
        eff_table: 2D lookup from (speed[0:inf],trq[0:inf]) to eff[0:1]
    where [a:b] means the range of the variable.

    Inputs:
        trq_req: causal signal for torque request from external controller.

    From the rotational domain, the components is like a torque source, from the
    electrical domain, the component is like a current source. And optionally, from
    the thermal domain, the component is like a heat source.

    Note on sign convention. We use I1 everywhere, to maintain consistent
    sign of the current in the equations.
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        peaktrq_spd=None,
        peaktrq_trq=None,
        peak_trq=None,
        peak_pwr=None,
        eff_spd=None,
        eff_trq=None,
        eff_eff=None,
        enable_heat_port=False,
    ):
        self.name = "bldc" if name is None else name

        self.elec = Elec2Pin(eqn_env, self.name, p1="pos", p2="neg")
        self.shaft = MechRotOnePort(eqn_env, self.name, p="shaft")

        self.ports = {**self.elec.ports, **self.shaft.ports}
        self.syms = self.elec.syms | self.shaft.syms
        self.eqs = self.elec.eqs | self.shaft.eqs

        # process user provided parameters
        self.peaktrq_spd, self.peaktrq_trq = process_peak_trq(
            self.name,
            peaktrq_spd,
            peaktrq_trq,
            peak_trq,
            peak_pwr,
        )

        if len(self.peaktrq_spd) != len(self.peaktrq_trq):
            raise ValueError(
                f"Component BLDC {self.name} peaktrq_spd and peaktrq_trq must be same length."
            )

        eff_params = [eff_spd, eff_trq, eff_eff]
        if any(eff_params) and not all(eff_params):
            raise ValueError(
                f"Component BLDC {self.name} eff_spd, eff_trq and eff_eff must be all defined, or all None."
            )
        if None in eff_params:
            self.eff_spd = np.linspace(0, np.max(self.peaktrq_spd), 20)
            self.eff_trq = np.linspace(0, np.max(self.peaktrq_trq), 20)
            self.eff_eff = np.ones((len(self.eff_spd), len(self.eff_trq))) * 0.9

        # create component symbols
        self.peaktrq_spd_s = Sym(
            eqn_env,
            self.name + "_peaktrq_spd",
            kind=SymKind.param,
            val=self.peaktrq_spd,
        )
        self.peaktrq_trq_s = Sym(
            eqn_env,
            self.name + "_peaktrq_trq",
            kind=SymKind.param,
            val=self.peaktrq_trq,
        )
        self.eff_spd_s = Sym(
            eqn_env, self.name + "_eff_spd", kind=SymKind.param, val=self.eff_spd
        )
        self.eff_trq_s = Sym(
            eqn_env, self.name + "_eff_trq", kind=SymKind.param, val=self.eff_trq
        )
        self.eff_eff_s = Sym(
            eqn_env, self.name + "_eff_eff", kind=SymKind.param, val=self.eff_eff
        )

        self.Pmech = Sym(eqn_env, self.name + "_Pmech", kind=SymKind.var)
        self.Pelec = Sym(eqn_env, self.name + "_Pelec", kind=SymKind.var)
        self.Treq = Sym(eqn_env, self.name + "_Treq", kind=SymKind.inp)
        self.Eff1Quad = Sym(eqn_env, self.name + "_Eff1Quad", kind=SymKind.var)
        self.Eff = Sym(eqn_env, self.name + "_Eff", kind=SymKind.var)

        # create component specific lookup table function symbols
        self.peak_trq_lut = sp.Function("interp")(
            self.shaft.w.s,
            self.peaktrq_spd_s.s,
            self.peaktrq_trq_s.s,
        )
        self.eff_lut = sp.Function("interp2d")(
            self.shaft.w.s,
            self.shaft.t.s,
            self.eff_spd_s.s,
            self.eff_trq_s.s,
            self.eff_eff_s.s,
        )
        self.syms.update(
            {
                self.peaktrq_spd_s,
                self.peaktrq_trq_s,
                self.eff_spd_s,
                self.eff_trq_s,
                self.eff_eff_s,
                self.Pmech,
                self.Pelec,
                self.Treq,
                self.Eff1Quad,
                self.Eff,
                self.peak_trq_lut,
                self.eff_lut,
            }
        )

        self.eqs.update(
            {
                Eqn(
                    e=sp.Eq(self.shaft.t.s, sp.min(self.Treq.s, self.peak_trq_lut)),
                    kind=EqnKind.comp,
                ),  # eqn 1
                Eqn(
                    e=sp.Eq(self.Pmech.s, self.shaft.t.s * self.shaft.w.s),
                    kind=EqnKind.comp,
                ),  # eqn 2
                Eqn(
                    e=sp.Eq(self.Eff.s, self.eff_lut),
                    kind=EqnKind.comp,
                ),  # eqn 3
                # FIXME: eqn 4 is missing, so energy is not conserved
                Eqn(
                    e=sp.Eq(self.Pelec.s, self.Pmech.s * self.Eff.s),
                    kind=EqnKind.comp,
                ),  # eqn 5
                Eqn(
                    e=sp.Eq(self.elec.I1.s, self.Pelec.s / self.elec.V.s),
                    kind=EqnKind.comp,
                ),  # eqn 6
            }
        )

        if enable_heat_port:
            self.heat = ThermalOnePort(eqn_env, self.name, p="heat")

            self.ports.update(self.heat.ports)
            self.syms.update(self.heat.syms)
            self.eqs.update(
                {
                    Eqn(
                        e=sp.Eq(self.heat.Q.s, sp.abs(self.Pelec.s - self.Pmech.s)),
                        kind=EqnKind.comp,
                    ),
                }
            )


class IdealWheel(ComponentBase):
    """
    Ideal wheel between rotational and translational.
    velocity = radius*angular_velocity
    force = torque/radius
    """

    def __init__(self, eqn_env, name=None, r=1.0):
        self.name = "whl" if name is None else name

        self.trans = MechTransOnePort(eqn_env, self.name, p="p")
        self.shaft = MechRotOnePort(eqn_env, self.name, p="shaft")

        self.ports = {**self.trans.ports, **self.shaft.ports}
        self.syms = self.trans.syms | self.shaft.syms
        self.eqs = self.trans.eqs | self.shaft.eqs

        if r <= 0.0:
            raise ValueError(f"Component IdealWheel {self.name} must have r>0")

        self.r = Sym(eqn_env, self.name + "_r", kind=SymKind.param, val=r)
        self.syms.add(self.r)
        self.eqs.update(
            {
                Eqn(
                    e=sp.Eq(self.trans.v.s, self.r.s * self.shaft.w.s),
                    kind=EqnKind.comp,
                ),
                Eqn(
                    e=sp.Eq(self.trans.f.s, self.shaft.t.s / self.r.s),
                    kind=EqnKind.comp,
                ),
            }
        )


class HydraulicActuatorLinear(ComponentBase):
    """
    Converters pressure to force, and mass_flow to translational motion.
    Component has 2 mechanical connections like a spring, p1 and p2.
    Components has 2 fluid connections, like a hydraulic actuator, f1, and f2.
    dP=P1-P2
    dF=F1-F2
    Assuming all Ps and Fs are >0, when dP*area>pF, p1 and p2 get further apart, and vice versa.
    I'm not sure they have to all be positive for that to hold, but I know when they are, it does.
    """

    def __init__(self, eqn_env, name=None, area=1.0, x_ic=0.0):
        self.name = "hal" if name is None else name

        self.trans = MechTransTwoPort(eqn_env, self.name)
        self.fluid = Fluid2Port(eqn_env, self.name, p1="f1", p2="f2")

        self.ports = {**self.trans.ports, **self.fluid.ports}
        self.syms = self.trans.syms | self.fluid.syms
        self.eqs = self.trans.eqs | self.fluid.eqs

        if area <= 0.0:
            raise ValueError(
                f"Component HydraulicActuatorLinear {self.name} must have area>0"
            )

        self.area = Sym(eqn_env, self.name + "_area", kind=SymKind.param, val=area)
        self.V = Sym(eqn_env, self.name + "_V", kind=SymKind.var, val=x_ic * area)
        self.dV = Sym(eqn_env, self.name + "_dV", kind=SymKind.var, int_sym=self.V)
        self.V.der_sym = self.dV
        self.syms.update(set([self.area, self.V, self.dV]))

        # force<->pressure relationships
        self.eqs.add(
            Eqn(
                e=sp.Eq(self.fluid.dP.s * self.area.s, -self.trans.f2.s),
                kind=EqnKind.comp,
            ),
        )

        # velocity<->mass_flow relationships
        # the 'tracked' volume of fluid in the actuator increases when M1 is positive
        self.eqs.add(
            Eqn(
                e=sp.Eq(self.dV.s, self.fluid.M1.s / eqn_env.fluid.density.s),
                kind=EqnKind.comp,
            ),
        )
        # the 'tracked' volume of fluid increases when the actuator gets longer.
        self.eqs.add(
            Eqn(
                e=sp.Eq(self.V.s / self.area.s, self.trans.x1.s - self.trans.x2.s),
                kind=EqnKind.comp,
            ),
        )

        # mass_flow constrain. e.g. conservation of mass.
        # here we consider the actuator 'ideal' in the sense that piston area on both sides is equal.
        # in reality this is not true, because there is typically one side with a rod which reduces
        # the piston area
        self.eqs.add(
            Eqn(e=sp.Eq(0, self.fluid.M1.s + self.fluid.M2.s), kind=EqnKind.comp),
        )
