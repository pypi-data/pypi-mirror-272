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

from component_library.base import eqn_env, Eqn
from acausal_diagram import AcausalDiagram
from acausal_compiler import AcausalCompiler
from sympy import Eq, symbols, Function
from component_library import elec
from component_library import translational as trans


def check_port_domain():
    print("======================check_port_domain")
    # FIXME: there are better ways of catching an expected error.
    # with pytest.raises(AssertionError) for example, but we're not using pytest here.
    ev = eqn_env()
    diagram = AcausalDiagram()
    m1 = trans.Mass(ev, name="m1", M=1.0)
    r1 = elec.Resistor(ev, name="r1")
    diagram.connect(m1, "p", r1, "p")
    compiler = AcausalCompiler(ev, diagram)
    try:
        compiler.diagram_processing()
    except AssertionError:
        print("success, the assertion error was expected.")


def check_ic_consistency():
    print("======================check_ic_consistency")
    # make system with inconsistent initial conditions
    ev = eqn_env()
    diagram = AcausalDiagram()
    m1 = trans.Mass(ev, name="m1", M=1.0, initial_position=0.0)
    sp1 = trans.Spring(ev, name="sp1", initial_angle_A=1.0)
    r1 = trans.FixedPosition(ev, name="r1")
    diagram.connect(sp1, "p", m1, "p")
    diagram.connect(sp1, "n", r1, "p")
    compiler = AcausalCompiler(ev, diagram)
    try:
        compiler.diagram_processing()
    except AssertionError:
        print("success, the assertion error was expected.")


class SS:
    def __init__(self, s):
        self.s = s


def check_alias_elimination():
    # FIXME: this test fails because I haven't managed to
    # fudge all the data necessary for it to pass since I
    # made the processing more complex.
    print("======================check_alias_elimination")
    ev = eqn_env()
    diagram = AcausalDiagram()

    # Define symbols
    a, b, c, d, e, f, g = symbols("a b c d e f g")
    h = Function("h")(ev.t)
    i = Function("i")(ev.t)
    j = Function("j")(ev.t)

    # verify function
    def check_aliases(compiler, len_expected):
        # we ended up with the expected number of reminaing equations
        assert len(compiler.eqs) == len_expected

        # check that each alias pair we expected to find,
        # that only one Sym from each pair appears in the aliases.
        check_sets = [[a, b], [c, d], [h, e], [i, j]]
        aliases = set(compiler.alias_map.keys())
        for check_set in check_sets:
            check_set = set(check_set)
            intersection = aliases.intersection(check_set)
            assert len(intersection) == 1

    # type0 test
    # equations 1,2,3,4 should go away
    compiler = AcausalCompiler(ev, diagram)
    compiler.eqs = {
        1: Eqn(e=Eq(a, b)),
        2: Eqn(e=Eq(c, -d)),
        3: Eqn(e=Eq(h, e)),
        4: Eqn(e=Eq(i, j)),
        5: Eqn(e=Eq(0, g * a)),
        6: Eqn(e=Eq(0, a**2 - g / 5 + d * h - j * i)),
    }
    compiler.syms = {i: SS(s) for i, s in enumerate([a, b, c, d, e, f, g, h, i, j])}
    compiler.update_syms_map()
    compiler.alias_elimination()
    check_aliases(compiler, 2)

    # type1 test
    # equations 1,2,3,4 should go away
    compiler = AcausalCompiler(ev, diagram)
    compiler.eqs = {
        1: Eqn(e=Eq(0, a + b)),
        2: Eqn(e=Eq(0, c - d)),
        3: Eqn(e=Eq(0, h + e)),
        4: Eqn(e=Eq(0, i + j)),
        5: Eqn(e=Eq(0, g * a)),
        6: Eqn(e=Eq(0, a**2 - g / 5 + d * h - j * i)),
    }
    compiler.syms = {i: SS(s) for i, s in enumerate([a, b, c, d, e, f, g, h, i, j])}
    compiler.update_syms_map()
    compiler.alias_elimination()
    check_aliases(compiler, 2)

    # type2 test
    # equations 1,2,3,4 should go away
    compiler = AcausalCompiler(ev, diagram)
    compiler.eqs = {
        1: Eqn(e=Eq(a + b, 0)),
        2: Eqn(e=Eq(c - d, 0)),
        3: Eqn(e=Eq(h + e, 0)),
        4: Eqn(e=Eq(i + j, 0)),
        5: Eqn(e=Eq(g * a, 0)),
        6: Eqn(e=Eq(0, a**2 - g / 5 + d * h - j * i)),
    }
    compiler.syms = {i: SS(s) for i, s in enumerate([a, b, c, d, e, f, g, h, i, j])}
    compiler.update_syms_map()
    compiler.alias_elimination()
    check_aliases(compiler, 2)

    print("passed")


if __name__ == "__main__":
    check_port_domain()
    check_ic_consistency()
    check_alias_elimination()
