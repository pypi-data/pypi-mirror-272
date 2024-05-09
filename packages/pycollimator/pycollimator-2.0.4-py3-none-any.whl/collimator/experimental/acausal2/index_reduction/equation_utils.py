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
from sympy.core.function import AppliedUndef


def extract_vars(eq, known_vars):
    """
    Extract variables from equations in their precise form, differentiating between
    non-derivatives and derivatives, and excluding known_vars.

    x(t) + y(t) = 0 -> {}, {x, y}
    x(t).diff(t) + y(t) = 0 -> {dx/dt}, {y}
    x(t).diff(t) + y(t).diff(t) = 0 -> {dx/t, dy/dt}, {}
    x(t) + x(t).diff(t) + y(t) = 0 -> {dx/t}, {x,y}
    x(t) + x(t).diff(t,t) + y(t).diff(t) = 0 -> {d2x/dt2, dy/dt}, {x}

    Parameters
    ----------
    eq : sympy equation
        A sympy equation from which variables need to be extracted
    known_vars : set
        Set of known variables

    Returns
    -------
    d_vars : set
        Set of differential variables
    a_vars : set
        Set of algebraic variables
    """

    d_vars = set()
    a_vars = set()

    def is_known(var):
        if var in known_vars:
            return True
        # check if the integrals of the variable are known
        if isinstance(var, sp.Derivative):
            return var.expr in known_vars
        # check if the derivatives of the variable are known
        if isinstance(var, AppliedUndef):
            return any(
                var == known.expr
                for known in known_vars
                if isinstance(known, sp.Derivative)
            )
        return False

    # Create a dummy equation by replacing all the derivatives
    true_to_dummy = {}
    for der in eq.atoms(sp.Derivative):
        dummy = sp.Symbol("d_" + str(der))
        true_to_dummy[der] = dummy
    dummy_eq = eq.subs(true_to_dummy)

    # Find algebraic variables in the dummy equation
    a_vars = dummy_eq.atoms(AppliedUndef)
    a_vars = {var for var in a_vars if not is_known(var)}

    d_vars = eq.atoms(sp.Derivative)
    d_vars = {var for var in d_vars if not is_known(var)}

    return d_vars, a_vars


def process_equations(eqs, known_vars):
    """
    f(x, x_dot, y ) = 0

    extract lists of x, x_dot, and y from the list of eqs representing `f`
    """

    d_vars = set()
    a_vars = set()

    vars_in_eqs = {}
    eqs_idx = {}
    for idx, eq in enumerate(eqs):
        eq_d_vars, eq_a_vars = extract_vars(eq, known_vars)
        d_vars.update(eq_d_vars)
        a_vars.update(eq_a_vars)
        vars_in_eqs[eq] = eq_d_vars.union(eq_a_vars)
        eqs_idx[idx] = eq

    x_dot = d_vars
    x = {var.expr for var in x_dot}
    y = a_vars.difference(x)
    X = set().union(x, x_dot, y)

    return list(x), list(x_dot), list(y), list(X), vars_in_eqs, eqs_idx


def compute_consistent_initial_conditions(eqs, X, ics, knowns):
    """
    Numerically solve for initial conditions
    """
    from scipy import optimize

    import jax

    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp

    ics_and_knowns = ics.copy()
    ics_and_knowns.update(knowns)

    # Convert derivatives to dummy algebraic variables
    true_to_dummy = {}

    for var in X:
        if isinstance(var, sp.Derivative):
            dummy = sp.Symbol("d_" + str(var))
            true_to_dummy[var] = dummy
            if var in ics_and_knowns:
                ics_and_knowns[dummy] = ics_and_knowns.pop(var)

    dummy_eqs = [eq.subs(true_to_dummy) for eq in eqs]

    # create F matrix and x_free vector to solve F(x_free) = 0
    F = sp.Matrix(dummy_eqs)

    ics_and_knowns_ders = {
        k: v for k, v in ics_and_knowns.items() if isinstance(k, sp.Derivative)
    }
    ics_and_knowns_others = {
        k: v for k, v in ics_and_knowns.items() if not isinstance(k, sp.Derivative)
    }

    F = sp.Matrix(F.subs(ics_and_knowns_ders))
    F = sp.Matrix(F.subs(ics_and_knowns_others))

    x = [true_to_dummy.get(var, var) for var in X]
    x_free = [var for var in x if var not in ics_and_knowns]  # Variables free to solve

    # Lamdify to create a function for root finding and solve numerically
    residual = sp.lambdify([x_free], F, modules="jax")

    # @jax.jit
    def root_func(x):
        return jnp.ravel(residual(x))

    jac = jax.jit(jax.jacfwd(root_func))

    # FIXME: When multiple solutions to the equations being solved exist,
    # the initial condition determines which one is chosen. We need a more robust
    # way to define these guesses---possibly based on the weak initial conditions
    # provided by the user.

    # x_0 = 0.1 * jnp.ones(len(x_free))
    x_0 = 0.0 * jnp.ones(len(x_free))
    res = optimize.root(root_func, x_0, jac=jac, tol=1e-12)

    if not res.success:
        raise ValueError("Numerical solution of ICs failed")
    else:
        print(f"residual = {res.fun}")

    # Reconstruct full variable set X_ic with solved values and known ics
    x_ic = res.x
    X_ic = []
    x_ic_counter = 0
    for var in x:
        if var in x_free:
            # If the variable was free (solved for), use the solved value
            X_ic.append(x_ic[x_ic_counter])
            x_ic_counter += 1
        else:
            # If the variable was not free (had initial conditions), use the known value
            X_ic.append(ics_and_knowns[var])

    return X_ic
