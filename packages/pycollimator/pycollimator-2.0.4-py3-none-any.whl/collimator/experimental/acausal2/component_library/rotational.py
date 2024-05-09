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


# Mechnical Rotational
# flow variable:Units = torque:Newton-meters
# potential variable:Units = angular_velocity:radians/second
class MechRotPort(PortBase):
    """
    port for a rotational mechanical component to interface with others.
    """

    def __init__(self, w_sym=None, t_sym=None):
        self.domain = Domain.rotational
        self.flow = t_sym
        self.pot = w_sym


class MechRotOnePort(ComponentBase):
    """
    a partial component with one mechanical rotational connection.
    """

    def __init__(self, eqn_env, name, w_ic=None, ang_ic=None, p="flange"):
        self.t = Sym(eqn_env, name + "_t", kind=SymKind.flow)
        self.ang = Sym(eqn_env, name + "_ang", kind=SymKind.var, ic=ang_ic)
        self.w = Sym(eqn_env, name + "_w", kind=SymKind.pot, int_sym=self.ang, ic=w_ic)
        self.alpha = Sym(eqn_env, name + "_alpha", kind=SymKind.var, int_sym=self.w)
        # encode the derivative relationships
        self.ang.der_sym = self.w
        self.w.der_sym = self.alpha

        self.ports = {p: MechRotPort(w_sym=self.w, t_sym=self.t)}
        self.syms = set([self.t, self.alpha, self.w, self.ang])
        self.eqs = set()


class MechRotTwoPort(ComponentBase):
    """
    a partial component with two mechanical rotational connections.
    """

    def __init__(
        self,
        eqn_env,
        name,
        ang1_ic=None,
        w1_ic=None,
        ang2_ic=None,
        w2_ic=None,
        p1="flange_a",
        p2="flange_b",
    ):
        self.t1 = Sym(eqn_env, self.name + "_t1", kind=SymKind.flow)
        self.t2 = Sym(eqn_env, self.name + "_t2", kind=SymKind.flow)

        self.ang1 = Sym(eqn_env, self.name + "_ang1", kind=SymKind.var, ic=ang1_ic)
        self.w1 = Sym(
            eqn_env, self.name + "_w1", kind=SymKind.pot, int_sym=self.ang1, ic=w1_ic
        )
        self.alpha1 = Sym(
            eqn_env, self.name + "_alpha1", kind=SymKind.var, int_sym=self.w1
        )
        # encode the dreivative relationships
        self.ang1.der_sym = self.w1
        self.w1.der_sym = self.alpha1

        self.ang2 = Sym(eqn_env, self.name + "_ang2", kind=SymKind.var, ic=ang2_ic)
        self.w2 = Sym(
            eqn_env, self.name + "_w2", kind=SymKind.pot, int_sym=self.ang2, ic=w2_ic
        )
        self.alpha2 = Sym(
            eqn_env, self.name + "_alpha2", kind=SymKind.var, int_sym=self.w2
        )
        # encode the dreivative relationships
        self.ang2.der_sym = self.w2
        self.w2.der_sym = self.alpha2

        self.ports = {
            p1: MechRotPort(w_sym=self.w1, t_sym=self.t1),
            p2: MechRotPort(w_sym=self.w2, t_sym=self.t2),
        }
        self.syms = set(
            [
                self.t1,
                self.t2,
                self.alpha1,
                self.w1,
                self.ang1,
                self.alpha2,
                self.w2,
                self.ang2,
            ]
        )
        self.eqs = set([Eqn(e=Eq(0, self.t1.s + self.t2.s), kind=EqnKind.comp)])


class TorqueSource(MechRotOnePort):
    """
    ideal torque source in mechanical rotational domain
    """

    def __init__(self, eqn_env, name=None, T=0.0, enable_torque_input=False):
        self.name = "mrt" if name is None else name
        super().__init__(eqn_env, self.name)

        if enable_torque_input:
            kind = SymKind.inp
            val = None
        else:
            kind = SymKind.param
            val = T

        # in this case we have to create an additional symbol since it is not OK
        # to change the kind of a potential/flow variable.
        self.Tparam = Sym(eqn_env, self.name + "_Tparam", kind=kind, val=val)
        self.syms.add(self.Tparam)

        # pressure source equality
        self.eqs.add(Eqn(e=Eq(self.t.s, self.Tparam.s), kind=EqnKind.comp))


class Inertia(MechRotOnePort):
    """
    ideal inertia in mechanical rotational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        I=1.0,  # noqa
        initial_velocity=None,
        initial_angle=None,
    ):
        self.name = "mri" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            w_ic=initial_velocity,
            ang_ic=initial_angle,
        )

        if I <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have I>0"
            )

        self.I = Sym(eqn_env, self.name + "_I", kind=SymKind.param, val=I)  # noqa
        self.syms.add(self.I)
        self.eqs.add(Eqn(e=Eq(self.t.s, self.I.s * self.alpha.s), kind=EqnKind.comp))


class Spring(MechRotTwoPort):
    """
    ideal spring in mechanical rotational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        K=1.0,
        initial_velocity_A=None,
        initial_angle_A=None,
        initial_velocity_B=None,
        initial_angle_B=None,
    ):
        self.name = "mrs" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            w1_ic=initial_velocity_A,
            ang1_ic=initial_angle_A,
            w2_ic=initial_velocity_B,
            ang2_ic=initial_angle_B,
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if K <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have K>0"
            )

        self.k = Sym(eqn_env, self.name + "_K", kind=SymKind.param, val=K)
        self.syms.add(self.k)
        self.eqs.add(
            Eqn(
                e=Eq(
                    self.t1.s, self.k.s * (self.ang1.s - self.ang2.s), kind=EqnKind.comp
                )
            )
        )


class Damper(MechRotTwoPort):
    """
    ideal damper in mechanical rotational domain
    """

    def __init__(
        self,
        eqn_env,
        name=None,
        D=1.0,
        initial_velocity_A=None,
        initial_angle_A=None,
        initial_velocity_B=None,
        initial_angle_B=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(
            eqn_env,
            self.name,
            w1_ic=initial_velocity_A,
            ang1_ic=initial_angle_A,
            w2_ic=initial_velocity_B,
            ang2_ic=initial_angle_B,
        )

        # maybe not a necessary contraint, but doing it for now to avoid confusing myself when debugging.
        if D <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have D>0"
            )

        self.d = Sym(eqn_env, self.name + "_c", kind=SymKind.param, val=D)
        self.syms.add(self.d)
        self.eqs.add(
            Eqn(e=Eq(self.t1.s, self.d.s * (self.w1.s - self.w2.s), kind=EqnKind.comp))
        )


class FixedAngle(MechRotOnePort):
    """
    rigid(non-moving) reference in mechanical rotational domain
    """

    def __init__(self, eqn_env, name=None, ang_ic=None):
        self.name = "mrr" if name is None else name
        super().__init__(eqn_env, self.name, w_ic=0, ang_ic=ang_ic)
        self.eqs.update(
            {
                Eqn(e=Eq(0, self.alpha.s), kind=EqnKind.comp),
                Eqn(e=Eq(0, self.w.s), kind=EqnKind.comp),
                Eqn(
                    e=Eq(0, self.ang.s), kind=EqnKind.comp
                ),  # FIXME: should be set to ang_ic
            }
        )
