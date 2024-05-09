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
    "Mass",
    "Spring",
    "FixedPosition",
    "ForceSource",
    "Damper",
]


class MechTransPort(PortBase):
    """
    port for a translational mechanical component to interface with others.
    """

    def __init__(self, v_sym=None, f_sym=None):
        self.flow = f_sym
        self.pot = v_sym


class MechTransOnePort(ComponentBase):
    """
    a partial component with one mechanical translational connection.
    """

    def __init__(self, name, v_ic=None, x_ic=None, p="flange"):
        self.f = sym(name + "_f", kind="flow")
        self.a = sym(name + "_a", kind="var")
        self.v = sym(name + "_v", kind="pot", der_sym=self.a.s, ic=v_ic)
        self.x = sym(name + "_x", kind="var", der_sym=self.v.s, ic=x_ic)

        self.ports = {p: MechTransPort(v_sym=self.v, f_sym=self.f)}
        self.syms = set([self.f, self.a, self.v, self.x])

        self.port_idx_to_name = {-1: p}


class MechTransTwoPort(ComponentBase):
    """
    a partial component with two mechanical translational connections.
    """

    def __init__(
        self,
        name,
        x1_ic=None,
        v1_ic=None,
        x2_ic=None,
        v2_ic=None,
        p1="flange_a",
        p2="flange_b",
    ):
        self.f1 = sym(name + "_f1", kind="flow")
        self.f2 = sym(name + "_f2", kind="flow")
        self.a1 = sym(name + "_a1", kind="var")
        self.v1 = sym(name + "_v1", kind="pot", der_sym=self.a1.s, ic=v1_ic)
        self.x1 = sym(name + "_x1", kind="var", der_sym=self.v1.s, ic=x1_ic)
        self.a2 = sym(name + "_a2", kind="var")
        self.v2 = sym(name + "_v2", kind="pot", der_sym=self.a2.s, ic=v2_ic)
        self.x2 = sym(name + "_x2", kind="var", der_sym=self.v2.s, ic=x2_ic)

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
        self.eqs = set([eqn(e=Eq(0, self.f1.s + self.f2.s))])

        self.port_idx_to_name = {-1: p1, 1: p2}


class ForceSource(MechTransOnePort):
    """
    ideal force source in mechanical translational domain
    """

    def __init__(self, name=None, F=0.0, enable_force_port=False, enable_flange_b=True):
        self.name = "mtf" if name is None else name
        super().__init__(self.name, p="flange_a")
        self.fparam = sym(self.name + "_F", kind="param", val=F)
        self.syms.add(self.fparam)
        self.eqs = set([eqn(e=Eq(self.fparam.s, self.f.s))])

        if enable_force_port or not enable_flange_b:
            raise NotImplementedError(
                "enable_force_port and enable_flange_b not supported"
            )

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "flange_a"}


class Mass(MechTransOnePort):
    """
    ideal point mass in mechanical translational domain
    """

    def __init__(self, name=None, M=1.0, initial_velocity=None, initial_position=None):
        self.name = "mtm" if name is None else name
        super().__init__(self.name, v_ic=initial_velocity, x_ic=initial_position)

        if M <= 0.0:
            raise ValueError(
                f"Component {self.__class__.__name__ } {self.name} must have M>0"
            )

        self.m = sym(self.name + "_M", kind="param", val=M)
        self.syms.add(self.m)
        self.eqs = set([eqn(e=Eq(self.f.s, self.m.s * self.a.s))])


class Spring(MechTransTwoPort):
    """
    ideal spring in mechanical translational domain
    """

    def __init__(
        self,
        name=None,
        K=1.0,
        initial_velocity_A=None,
        initial_position_A=None,
        initial_velocity_B=None,
        initial_position_B=None,
    ):
        self.name = "mts" if name is None else name
        super().__init__(
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

        self.k = sym(self.name + "_K", kind="param", val=K)
        self.syms.add(self.k)
        self.eqs.add(eqn(e=Eq(self.f1.s, self.k.s * (self.x1.s - self.x2.s))))


class Damper(MechTransTwoPort):
    """
    ideal damper in mechanical translational domain
    """

    def __init__(
        self,
        name=None,
        D=1.0,
        initial_velocity_A=None,
        initial_position_A=None,
        initial_velocity_B=None,
        initial_position_B=None,
    ):
        self.name = "mtd" if name is None else name
        super().__init__(
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

        self.d = sym(self.name + "_D", kind="param", val=D)
        self.syms.add(self.d)
        self.eqs.add(eqn(e=Eq(self.f1.s, self.d.s * (self.v1.s - self.v2.s))))


class FixedPosition(MechTransOnePort):
    """
    rigid(non-moving) reference in mechanical translational domain
    """

    def __init__(self, name=None, x_ic=None):
        self.name = "mtr" if name is None else name
        super().__init__(self.name, v_ic=0, x_ic=x_ic)
        self.eqs = set([eqn(e=Eq(0, self.a.s)), eqn(e=Eq(0, self.v.s))])

        # this sucks. need this here because not all one port blocks
        # use the 'input' of the block.
        self.port_idx_to_name = {1: "flange"}
