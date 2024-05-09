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
from index_reduction import IndexReduction

# Define the symbol for time
t = sp.symbols("t")

# Define parameters
L = sp.symbols("L")
g = sp.symbols("g")

# Define functions of time
x = sp.Function("x")(t)
y = sp.Function("y")(t)
w = sp.Function("w")(t)
z = sp.Function("z")(t)
T = sp.Function("T")(t)

# knowns
knowns = {L: 1.0, g: 9.8}

# Define the derivatives of these functions with respect to time
xdot = x.diff(t)
ydot = y.diff(t)
wdot = w.diff(t)
zdot = z.diff(t)

# Define equations
eq0 = xdot - w
eq1 = ydot - z
eq2 = wdot - T * x
eq3 = zdot - T * y + g
eq4 = x**2 + y**2 - L**2

# Equations list
eqs = [eq0, eq1, eq2, eq3, eq4]

ics = {x: 3.14 / 20, ydot: 1.0}

ir = IndexReduction(t, eqs, knowns, ics, verbose=True)
ir()
