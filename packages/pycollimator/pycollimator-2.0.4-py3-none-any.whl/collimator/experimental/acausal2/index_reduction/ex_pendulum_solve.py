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

import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from index_reduction import IndexReduction
from scikits.odes import dae

jax.config.update("jax_enable_x64", True)

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

theta_0 = np.pi / 3.0
ics = {x: knowns[L] * np.sin(theta_0), ydot: 0.0}
# ics = {x: 3.14 / 20, ydot: 1.0}

ir = IndexReduction(t, eqs, knowns, ics, verbose=True)
ir()


xy = ir.final_dae_x.copy()
xy.extend(ir.final_dae_y)

xy_dot = ir.final_dae_x_dot.copy()

F = sp.Matrix(ir.final_dae_eqs)

dF_dxy = F.jacobian(xy)
dF_dxy_dot = F.jacobian(xy_dot)

knowns_ders = {k: v for k, v in knowns.items() if isinstance(k, sp.Derivative)}
knowns_others = {k: v for k, v in knowns.items() if not isinstance(k, sp.Derivative)}

F = F.subs(knowns_ders)
F = F.subs(knowns_others)

dF_dxy = dF_dxy.subs(knowns_ders)
dF_dxy = dF_dxy.subs(knowns_others)

dF_dxy_dot = dF_dxy_dot.subs(knowns_ders)
dF_dxy_dot = dF_dxy_dot.subs(knowns_others)


dae_residual_lambdified = sp.lambdify((t, *xy, *xy_dot), F, modules="numpy")
dae_jacobian_xy_lambdified = sp.lambdify((t, *xy, *xy_dot), dF_dxy, modules="numpy")
dae_jacobian_xy_dot_lambdified = sp.lambdify(
    (t, *xy, *xy_dot), dF_dxy_dot, modules="numpy"
)

n_diff = len(ir.final_dae_x)
n_alg = len(ir.final_dae_y)


def dae_residual_contracted(t, xy, xy_dot):
    xy_dot_relevant = xy_dot[:n_diff]
    return dae_residual_lambdified(t, *xy, *xy_dot_relevant)


def dae_jacobian_xy_contracted(t, xy, xy_dot):
    xy_dot_relevant = xy_dot[:n_diff]
    return dae_jacobian_xy_lambdified(t, *xy, *xy_dot_relevant)


def dae_jacobian_xy_dot_contracted(t, xy, xy_dot):
    xy_dot_relevant = xy_dot[:n_diff]
    return dae_jacobian_xy_dot_lambdified(t, *xy, *xy_dot_relevant)


def dae_residual(t, x, xdot, result):
    residual = dae_residual_contracted(t, x, xdot)
    result[:] = residual[:, 0]
    return 0


def dae_jacobian(t, x, xdot, residual, cj, result):
    jac_x = dae_jacobian_xy_contracted(t, x, xdot)
    jac_xdot = dae_jacobian_xy_dot_contracted(t, x, xdot)

    result[:, :] = jac_x + cj * jnp.pad(
        jac_xdot, ((0, 0), (0, n_alg)), mode="constant", constant_values=(0.0,)
    )
    return 0


solver = dae(
    "ida",
    dae_residual,
    jacfn=dae_jacobian,
    first_step_size=1e-18,
    rtol=1e-06,
    atol=1e-08,
    algebraic_vars_idx=list(range(n_diff, n_diff + n_alg)),
    exclude_algvar_from_error=True,
    max_steps=500,
    old_api=False,
)


xy_0 = ir.final_dae_x_ic.copy()
xy_0.extend(ir.final_dae_y_ic)
xy_dot_0 = ir.final_dae_x_dot_ic.copy()
xy_dot_0.extend([0.00] * n_alg)


t_final = 2.0
solution = solver.solve(np.linspace(0.0, t_final, 100), xy_0, xy_dot_0)


x_index = xy.index(x)
y_index = xy.index(y)

t_sol = solution.values.t
x_sol = solution.values.y[:, x_index]
y_sol = solution.values.y[:, y_index]

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(x_sol, y_sol)
ax1.set_xlim([-1.1, 1.1])
ax1.set_ylim([-1.1, 1.1])
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.axis("equal")

ax2.plot(t_sol, x_sol, label="x")
ax2.plot(t_sol, y_sol, label="y")
ax2.set_xlabel("t")
ax2.set_ylabel("x | y")
ax2.legend()

fig.tight_layout()

plt.show()
