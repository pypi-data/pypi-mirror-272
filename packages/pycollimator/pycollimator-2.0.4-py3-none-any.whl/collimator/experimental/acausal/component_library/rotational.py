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
from .base import sym, eqn, PortBase, ComponentBase

__all__ = [
    "TorqueSource",
    "Inertia",
    "Spring",
    "Damper",
    "FixedAngle",
]


class MechRotPort(PortBase):
    """
    port for a rotational mechanical component to interface with others.
    """

    def __init__(self, w_sym=None, t_sym=None):
        self.flow = t_sym
        self.pot = w_sym


class MechRotOnePort(ComponentBase):
    """
    a partial component with one mechanical rotational connection.
    """

    def __init__(self, name, w_ic=None, ang_ic=None, p="flange"):
        self.t = sym(name + "_t", kind="flow")
        self.alpha = sym(name + "_alpha", kind="var")
        self.w = sym(name + "_w", kind="pot", der_sym=self.alpha.s, ic=w_ic)
        self.ang = sym(name + "_ang", kind="var", der_sym=self.w.s, ic=ang_ic)

        self.ports = {p: MechRotPort(w_sym=self.w, t_sym=self.t)}

        self.syms = set([self.t, self.alpha, self.w, self.ang])

        self.port_idx_to_name = {-1: p}


class MechRotTwoPort(ComponentBase):
    """
    a partial component with two mechanical rotational connections.
    """

    def __init__(
        self,
        name,
        ang1_ic=None,
        w1_ic=None,
        ang2_ic=None,
        w2_ic=None,
        p1="flange_a",
        p2="flange_b",
    ):
        self.t1 = sym(name + "_t1", kind="flow")
        self.t2 = sym(name + "_t2", kind="flow")
        self.alpha1 = sym(name + "_alpha1", kind="var")
        self.w1 = sym(name + "_w1", kind="pot", der_sym=self.alpha1.s, ic=w1_ic)
        self.ang1 = sym(name + "_ang1", kind="var", der_sym=self.w1.s, ic=ang1_ic)
        self.alpha2 = sym(name + "_alpha2", kind="var")
        self.w2 = sym(name + "_w2", kind="pot", der_sym=self.alpha2.s, ic=w2_ic)
        self.ang2 = sym(name + "_ang2", kind="var", der_sym=self.w2.s, ic=ang2_ic)

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
        self.eqs = set([eqn(e=Eq(0, self.t1.s + self.t2.s))])

        self.port_idx_to_name = {-1: p1, 1: p2}


class TorqueSource(MechRotOnePort):
    """
    ideal torque source in mechanical rotational domain
    """

    def __init__(
        self, name=None, T=0.0, enable_torque_port=False, enable_flange_b=True
    ):
        self.name = "mrt" if name is None else name
        super().__init__(self.name, p="flange_a")
        self.tparam = sym(self.name + "_T", kind="param", val=T)
        self.syms.add(self.tparam)
        self.eqs = set([eqn(e=Eq(self.tparam.s, self.t.s))])

        if enable_torque_port or not enable_flange_b:
            raise NotImplementedError(
                "enable_torque_port and enable_flange_b not supported"
            )

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "flange_a"}


class Inertia(MechRotOnePort):
    """
    ideal inertia in mechanical rotational domain
    """

    def __init__(
        self,
        name=None,
        I=1.0,  # noqa
        initial_velocity=None,
        initial_angle=None,
    ):
        self.name = "mri" if name is None else name
        super().__init__(self.name, w_ic=initial_velocity, ang_ic=initial_angle)

        if I <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have I>0"
            )

        self.I = sym(self.name + "_I", kind="param", val=I)  # noqa
        self.syms.add(self.I)
        self.eqs = set([eqn(e=Eq(self.t.s, self.I.s * self.alpha.s))])


class Spring(MechRotTwoPort):
    """
    ideal spring in mechanical rotational domain
    """

    def __init__(
        self,
        name=None,
        K=1.0,
        initial_velocity_A=None,
        initial_angle_A=None,
        initial_velocity_B=None,
        initial_angle_B=None,
    ):
        self.name = "mrs" if name is None else name
        super().__init__(
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

        self.k = sym(self.name + "_K", kind="param", val=K)
        self.syms.add(self.k)
        self.eqs.add(eqn(e=Eq(self.t1.s, self.k.s * (self.ang1.s - self.ang2.s))))


class Damper(MechRotTwoPort):
    """
    ideal damper in mechanical rotational domain
    """

    def __init__(
        self,
        name=None,
        D=1.0,
        initial_velocity_A=None,
        initial_angle_A=None,
        initial_velocity_B=None,
        initial_angle_B=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(
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

        self.d = sym(self.name + "_D", kind="param", val=D)
        self.syms.add(self.d)
        self.eqs.add(eqn(e=Eq(self.t1.s, self.d.s * (self.w1.s - self.w2.s))))


class FixedAngle(MechRotOnePort):
    """
    rigid(non-moving) reference in mechanical rotational domain
    """

    def __init__(self, name=None, x_ic=None):
        self.name = "mrr" if name is None else name
        super().__init__(self.name, w_ic=0, ang_ic=x_ic)
        self.eqs = set([eqn(e=Eq(0, self.alpha.s)), eqn(e=Eq(0, self.w.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "flange"}
