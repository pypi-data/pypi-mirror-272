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


# Mechnical Translational
# flow variable:Units = force:Newtons
# potential variable:Units = velocity:meters/second
class MechTransPort(PortBase):
    """
    port for a translational mechanical component to interface with others.
    """

    def __init__(self, v_sym=None, f_sym=None):
        self.domain = Domain.translational
        self.flow = f_sym
        self.pot = v_sym


class MechTransOnePort(ComponentBase):
    """
    a partial component with one mechanical translational connection.
    """

    def __init__(self, eqn_env, name, v_ic=None, x_ic=None, p="flange"):
        self.f = Sym(eqn_env, name + "_f", kind=SymKind.flow)
        self.x = Sym(eqn_env, name + "_x", kind=SymKind.var, ic=x_ic)
        self.v = Sym(eqn_env, name + "_v", kind=SymKind.pot, int_sym=self.x, ic=v_ic)
        self.a = Sym(eqn_env, name + "_a", kind=SymKind.var, int_sym=self.v)
        # encode the derivative relationships
        self.x.der_sym = self.v
        self.v.der_sym = self.a

        self.ports = {p: MechTransPort(v_sym=self.v, f_sym=self.f)}
        self.syms = set([self.f, self.a, self.v, self.x])
        self.eqs = set()


class MechTransTwoPort(ComponentBase):
    """
    a partial component with two mechanical translational connections.
    """

    def __init__(
        self,
        eqn_env,
        name,
        x1_ic=None,
        v1_ic=None,
        x2_ic=None,
        v2_ic=None,
        p1="flange_a",
        p2="flange_b",
    ):
        self.f1 = Sym(eqn_env, name + "_f1", kind=SymKind.flow)
        self.f2 = Sym(eqn_env, name + "_f2", kind=SymKind.flow)

        self.x1 = Sym(eqn_env, name + "_x1", kind=SymKind.var, ic=x1_ic)
        self.v1 = Sym(
            eqn_env, name + "_v1", kind=SymKind.pot, int_sym=self.x1, ic=v1_ic
        )
        self.a1 = Sym(eqn_env, name + "_a1", kind=SymKind.var, int_sym=self.v1)
        # encode the dreivative relationships
        self.x1.der_sym = self.v1
        self.v1.der_sym = self.a1

        self.x2 = Sym(eqn_env, name + "_x2", kind=SymKind.var, ic=x2_ic)
        self.v2 = Sym(
            eqn_env, name + "_v2", kind=SymKind.pot, int_sym=self.x2, ic=v2_ic
        )
        self.a2 = Sym(eqn_env, name + "_a2", kind=SymKind.var, int_sym=self.v2)
        # encode the dreivative relationships
        self.x2.der_sym = self.v2
        self.v2.der_sym = self.a2

        self.ports = {
            p1: MechTransPort(v_sym=self.v1, f_sym=self.f1),
            p2: MechTransPort(v_sym=self.v2, f_sym=self.f2),
        }
        self.syms = set(
            [
                self.f1,
                self.f2,
                self.a1,
                self.v1,
                self.x1,
                self.a2,
                self.v2,
                self.x2,
            ]
        )
        self.eqs = set([Eqn(e=Eq(0, self.f1.s + self.f2.s), kind=EqnKind.comp)])


class ForceSource(MechTransOnePort):
    """
    ideal force source in mechanical translational domain
    """

    def __init__(self, eqn_env, name=None, F=0.0, enable_force_input=False):
        self.name = "mtf" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_force_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = F

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Fparam = Sym(eqn_env, self.name + "_Fparam", kind=kind, val=val)
        self.syms.add(self.Fparam)

        # pressure source equality
        self.eqs.add(Eqn(e=Eq(self.f.s, self.Fparam.s), kind=EqnKind.comp))


class Mass(MechTransOnePort):
    """
    ideal point mass in mechanical translational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        M=1.0,
        initial_velocity=None,
        initial_position=None,
    ):
        self.name = "mtm" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            v_ic=initial_velocity,
            x_ic=initial_position,
        )

        if M <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have M>0"
            )

        self.m = Sym(eqn_env, self.name + "_M", kind=SymKind.param, val=M)
        self.syms.add(self.m)
        self.eqs.add(Eqn(e=Eq(self.f.s, self.m.s * self.a.s), kind=EqnKind.comp))


class Spring(MechTransTwoPort):
    """
    ideal spring in mechanical translational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        K=1.0,
        initial_velocity_A=None,
        initial_position_A=None,
        initial_velocity_B=None,
        initial_position_B=None,
    ):
        self.name = "mts" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            v1_ic=initial_velocity_A,
            x1_ic=initial_position_A,
            v2_ic=initial_velocity_B,
            x2_ic=initial_position_B,
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if K <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have K>0"
            )

        self.k = Sym(eqn_env, self.name + "_K", kind=SymKind.param, val=K)
        self.syms.add(self.k)
        self.eqs.add(
            Eqn(e=Eq(self.f1.s, self.k.s * (self.x1.s - self.x2.s), kind=EqnKind.comp))
        )


class Damper(MechTransTwoPort):
    """
    ideal damper in mechanical translational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        D=1.0,
        initial_velocity_A=None,
        initial_position_A=None,
        initial_velocity_B=None,
        initial_position_B=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            v1_ic=initial_velocity_A,
            x1_ic=initial_position_A,
            v2_ic=initial_velocity_B,
            x2_ic=initial_position_B,
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if D <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have D>0"
            )

        self.d = Sym(eqn_env, self.name + "_D", kind=SymKind.param, val=D)
        self.syms.add(self.d)
        self.eqs.add(
            Eqn(e=Eq(self.f1.s, self.d.s * (self.v1.s - self.v2.s), kind=EqnKind.comp))
        )


class FixedPosition(MechTransOnePort):
    """
    rigid(non-moving) reference in mechanical translational domain
    """

    def __init__(self, eqn_env, name=None, x_ic=None):
        self.name = "mtr" if name is None else name
        super().__init__(eqn_env, self.name, v_ic=0, x_ic=x_ic)
        self.eqs.update(
            {
                Eqn(e=Eq(0, self.a.s), kind=EqnKind.comp),
                Eqn(e=Eq(0, self.v.s), kind=EqnKind.comp),
                Eqn(
                    e=Eq(0, self.x.s), kind=EqnKind.comp
                ),  # FIXME: should be set to x_ic
            }
        )


class SpeedSensor(ComponentBase):
    """
    sensor for relative speed.
    when flange_b enabled, senses between flange_a and flange_b.
    when flange_b disbaled, sense between flange_a and reference zero speed.
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        enable_flange_b=True,
    ):
        self.name = "mtspdsnsr" if name is None else name

        if enable_flange_b:
            self.ports = MechTransTwoPort(eqn_env, name)
        else:
            self.ports = MechTransOnePort(eqn_env, name)

        self.ports = {**self.ports.ports}
        self.syms = set(self.ports.syms)
        self.eqs = set(self.ports.eqs)

        self.v_rel = Sym(eqn_env, self.name + "_v_rel", kind=SymKind.outp)
        self.syms.add(self.v_rel)
        if enable_flange_b:
            self.eqs.add(
                Eqn(
                    e=Eq(
                        self.v_rel.s,
                        self.ports.v1.s - self.ports.v2.s,
                        kind=EqnKind.comp,
                    )
                )
            )
        else:
            self.eqs.add(Eqn(e=Eq(self.v_rel.s, self.ports.v.s, kind=EqnKind.comp)))
