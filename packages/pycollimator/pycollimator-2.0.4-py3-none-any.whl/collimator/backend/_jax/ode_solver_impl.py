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

from __future__ import annotations
from typing import TYPE_CHECKING
from functools import partial

import jax
import jax.numpy as jnp
from jax._src.numpy.util import promote_dtypes_inexact
from jax.flatten_util import ravel_pytree
from jax.experimental.ode import ravel_first_arg
import equinox as eqx

from ..ode_solver import ODESolverBase, ODESolverState

if TYPE_CHECKING:
    from ...framework import ContextBase

__all__ = ["ODESolverImpl", "norm"]


def norm(x):
    return jnp.linalg.norm(x) / x.size**0.5


class ODESolverImpl(ODESolverBase):
    """Common implementation for JAX ODE solvers.

    This class includes common functionality for JAX ODE solvers, such as
    overriding the `initialize` method to provide custom VJP definitions
    and a method for computing the initial step size.
    """

    def _finalize(self):
        self.hmin = self.min_step_size or 0.0
        self.hmax = self.max_step_size or jnp.inf
        self.initialize = self._override_initialize_vjp()

    def initialize(self, context: ContextBase, dt: float = None) -> ODESolverImpl:
        # The abstract base class requires an implementation of this method.
        # However, in order to provide a custom VJP definition, the class will
        # override this method with a custom VJP definition in `_override_initialize_vjp`.
        # Hence, this is a dummy implementation that should never actually be called.
        raise RuntimeError(
            "Default method should have been overridden in __post_init__"
        )

    def _initialize_state(
        self, func, t0, xc0, unravel, *args, dt=None
    ) -> ODESolverState:
        raise NotImplementedError

    # Inherits docstring from `ODESolverBase`
    def _initialize(self, context: ContextBase, dt: float = None) -> ODESolverState:
        xc0 = context.continuous_state
        t0 = context.time
        xc0, unravel = ravel_pytree(xc0)
        self.flat_ode_rhs = ravel_first_arg(self.ode_rhs, unravel)
        return self._initialize_state(
            self.flat_ode_rhs, t0, xc0, unravel, context, dt=dt
        )

    def _override_initialize_vjp(self):
        if not self.enable_autodiff:
            return self._initialize

        def _wrapped_initialize(self: ODESolverImpl, context, dt=None):
            return self._initialize(context, dt=dt)

        def _wrapped_initialize_fwd(self: ODESolverImpl, context, dt):
            # Need to correctly initialize the time step if it is not
            # provided.  This is probably not the most efficient
            # implementation, since it results in multiple call sites
            # to the RHS evaluation.  However, it will not typically end
            # up in the JIT computation graph unless differentiating through
            # reset maps. From some simple timing, the overhead seems to be pretty
            # minimal, at least.

            if dt is None:
                state = self._initialize(context, dt)
                dt = state.dt

            primals, vjp_fun = jax.vjp(partial(self._initialize, dt=dt), context)
            residuals = (vjp_fun,)
            return primals, residuals

        def _wrapped_initialize_adj(self, dt, residuals, adjoints):
            (vjp_fun,) = residuals
            (context_adj,) = vjp_fun(adjoints)
            return (context_adj,)

        initialize = jax.custom_vjp(_wrapped_initialize, nondiff_argnums=(0, 2))
        initialize.defvjp(_wrapped_initialize_fwd, _wrapped_initialize_adj)

        # Copy docstring and type hints
        initialize.__doc__ = super().initialize.__doc__
        initialize.__annotations__ = self._initialize.__annotations__

        return partial(initialize, self)

    def initialize_adjoint(self, func, init_adj_state, tf, context):
        """Initialize the solver configured for the adjoint reverse-time solve."""

        def adj_dynamics(aug_state, neg_t, context):
            """Original system augmented with vjp_y, vjp_t and vjp_args."""
            y, y_bar, *_ = aug_state
            # `neg_t` here is negative time, so we need to negate again to get back to
            # normal time.  The VJP is filtered to only differentiable arguments
            y_dot, vjpfun = eqx.filter_vjp(func, y, -neg_t, context)
            return (-y_dot, *vjpfun(y_bar))

        init_adj_state, unravel = ravel_pytree(init_adj_state)
        adj_dynamics = ravel_first_arg(adj_dynamics, unravel)
        adj_solver_state = self._initialize_state(
            adj_dynamics, -tf, init_adj_state, unravel, context
        )
        return adj_solver_state, adj_dynamics

    def initial_step_size(self, func, y0, t0, order, f0, *args):
        # Algorithm from:
        # E. Hairer, S. P. Norsett G. Wanner,
        # Solving Ordinary Differential Equations I: Nonstiff Problems, Sec. II.4.
        y0, f0 = promote_dtypes_inexact(y0, f0)
        dtype = y0.dtype

        scale = self.atol + jnp.abs(y0) * self.rtol
        scale = scale.astype(dtype)
        d0 = norm(y0 / scale)
        d1 = norm(f0 / scale)

        h0 = jnp.where((d0 < 1e-5) | (d1 < 1e-5), 1e-6, 0.01 * d0 / d1)
        y1 = y0 + h0.astype(dtype) * f0
        f1 = func(y1, t0 + h0, *args)
        d2 = norm((f1 - f0) / scale) / h0

        h1 = jnp.where(
            (d1 <= 1e-15) & (d2 <= 1e-15),
            jnp.maximum(1e-6, h0 * 1e-3),
            (0.01 / jnp.maximum(d1, d2)) ** (1.0 / (order + 1.0)),
        )

        dt = jnp.minimum(100.0 * h0, h1)
        return jnp.clip(dt, a_min=self.hmin, a_max=self.hmax)
