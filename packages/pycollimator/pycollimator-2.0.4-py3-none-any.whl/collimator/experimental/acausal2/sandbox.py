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

# from component_library.base import eqn_env
# from acausal_diagram import AcausalDiagram
# from acausal_compiler import AcausalCompiler
# import component_library as lib
import sympy as sp
import numpy as np

# from sympy.utilities.lambdify import implemented_function
import jax
from typing import Iterable, Optional

import jax.numpy as jnp
from jax.scipy.ndimage import map_coordinates

"""
this is just a script i used to play around with things because I dont like note books.

trying to make custom sympy function for lookup tables
https://www.geeksforgeeks.org/python-sympy-lambdify-method/
from that explanation, we can do the following.

it seems like what we want to do is use our cnp libraray with lamdify.
"""


Array = jnp.ndarray


def interp2d(
    x: Array,
    y: Array,
    xp: Array,
    yp: Array,
    zp: Array,
    fill_value: Optional[Array] = None,
) -> Array:
    """
    Bilinear interpolation on a grid. ``CartesianGrid`` is much faster if the data
    lies on a regular grid.

    Args:
        x, y: 1D arrays of point at which to interpolate. Any out-of-bounds
            coordinates will be clamped to lie in-bounds.
        xp, yp: 1D arrays of points specifying grid points where function values
            are provided.
        zp: 2D array of function values. For a function `f(x, y)` this must
            satisfy `zp[i, j] = f(xp[i], yp[j])`

    Returns:
        1D array `z` satisfying `z[i] = f(x[i], y[i])`.
    """
    if xp.ndim != 1 or yp.ndim != 1:
        raise ValueError("xp and yp must be 1D arrays")
    if zp.shape != (xp.shape + yp.shape):
        raise ValueError("zp must be a 2D array with shape xp.shape + yp.shape")

    ix = jnp.clip(jnp.searchsorted(xp, x, side="right"), 1, len(xp) - 1)
    iy = jnp.clip(jnp.searchsorted(yp, y, side="right"), 1, len(yp) - 1)

    # Using Wikipedia's notation (https://en.wikipedia.org/wiki/Bilinear_interpolation)
    z_11 = zp[ix - 1, iy - 1]
    z_21 = zp[ix, iy - 1]
    z_12 = zp[ix - 1, iy]
    z_22 = zp[ix, iy]

    z_xy1 = (xp[ix] - x) / (xp[ix] - xp[ix - 1]) * z_11 + (x - xp[ix - 1]) / (
        xp[ix] - xp[ix - 1]
    ) * z_21
    z_xy2 = (xp[ix] - x) / (xp[ix] - xp[ix - 1]) * z_12 + (x - xp[ix - 1]) / (
        xp[ix] - xp[ix - 1]
    ) * z_22

    z = (yp[iy] - y) / (yp[iy] - yp[iy - 1]) * z_xy1 + (y - yp[iy - 1]) / (
        yp[iy] - yp[iy - 1]
    ) * z_xy2

    if fill_value is not None:
        oob = jnp.logical_or(
            x < xp[0], jnp.logical_or(x > xp[-1], jnp.logical_or(y < yp[0], y > yp[-1]))
        )
        z = jnp.where(oob, fill_value, z)

    return z


class CartesianGrid:
    """
    Linear Multivariate Cartesian Grid interpolation in arbitrary dimensions. Based
    on ``map_coordinates``.

    Notes:
        Translated directly from https://github.com/JohannesBuchner/regulargrid/ to jax.
    """

    values: Array
    """
    Values to interpolate.
    """
    limits: Iterable[Iterable[float]]
    """
    Limits along each dimension of ``values``.
    """

    def __init__(
        self,
        limits: Iterable[Iterable[float]],
        values: Array,
        mode: str = "constant",
        cval: float = jnp.nan,
    ):
        """
        Initializer.

        Args:
            limits: collection of pairs specifying limits of input variables along
                each dimension of ``values``
            values: values to interpolate. These must be defined on a regular grid.
            mode: how to handle out of bounds arguments; see docs for ``map_coordinates``
            cval: constant fill value; see docs for ``map_coordinates``
        """
        super().__init__()
        self.values = values
        self.limits = limits
        self.mode = mode
        self.cval = cval

    def __call__(self, *coords) -> Array:
        """
        Perform interpolation.

        Args:
            coords: point at which to interpolate. These will be broadcasted if
                they are not the same shape.

        Returns:
            Interpolated values, with extrapolation handled according to ``mode``.
        """
        # transform coords into pixel values
        coords = jnp.broadcast_arrays(*coords)
        # coords = jnp.asarray(coords)
        coords = [
            (c - lo) * (n - 1) / (hi - lo)
            for (lo, hi), c, n in zip(self.limits, coords, self.values.shape)
        ]
        return map_coordinates(
            self.values, coords, mode=self.mode, cval=self.cval, order=1
        )


def wc_interp(x, xp, fp):
    return jax.numpy.interp(x, xp, fp)


# def wc_jax_ifthenelse(cond, true_expr, false_expr):
#     return jax.lax.cond(cond, true_fun, false_fun)


wc_lamdify_funcs = {"interp": wc_interp, "interp2d": interp2d}

if __name__ == "__main__":
    t = sp.symbols("t")
    x = sp.symbols("x")
    xp = sp.symbols("xp")
    fp = sp.symbols("fp")

    xb = sp.symbols("xb")
    xpb = sp.symbols("xpb")
    fpb = sp.symbols("fpb")

    xpv = np.array([1.0, 2.0, 3.0])
    fpv = np.array([4.0, 5.0, 6.0])
    xpvb = np.array([1.0, 2.0, 3.0]) * 2.0
    fpvb = np.array([4.0, 5.0, 6.0]) + 2.0

    a = sp.Function("a")(t)
    interp = sp.Function("interp")(x, xp, fp)
    interpb = sp.Function("interp")(xb, xpb, fpb)
    interpa = sp.Function("interp")(a, xp, fp)

    args = [x, xp, fp]
    f = sp.lambdify(args, interp, modules=["numpy", "scipy"])
    print(f(1.5, xpv, fpv))
    print(f(2.5, xpv, fpv))

    argsb = [x, xp, fp, xb, xpb, fpb]
    expr = interp + interpb + 9.0
    fb = sp.lambdify(argsb, [interp, interpb, expr], modules=["numpy", "scipy"])
    print(fb(2.5, xpv, fpv, 2.5 * 2.0, xpvb, fpvb))

    jax_interp = sp.Function("interp")(x, xp, fp)
    # jax_interp = sp.sin(x)
    f = sp.lambdify(args, jax_interp, modules=["jax", wc_lamdify_funcs])
    print(f(1.5, xpv, fpv))
    print(f(2.5, xpv, fpv))

    f = sp.symbols("f")
    zp = sp.symbols("zp")
    zpm = np.array(
        [
            [1.0, 2.0, 3.0],
            [
                4.0,
                5.0,
                6.0,
            ],
            [7.0, 8.0, 9.0],
        ]
    )

    jax_interp2d = sp.Function("interp2d")(x, f, xp, fp, zp)
    args = [x, f, xp, fp, zp]
    f = sp.lambdify(args, jax_interp2d, modules=["jax", wc_lamdify_funcs])
    print(f(1.5, 4.5, xpv, fpv, zpm))
    print(f(2.5, 4.5, xpv, fpv, zpm))

    print(f"{interp=}")
    print(f"{interp.subs(x,a)}")
    x.subs(xp, fp)
    print(f"{x=}")

    expr_no_t = interp + interpb + 9.0
    expr_w_t = interp + interpb + 9.0 + a
    dexpr_no_t = expr_no_t.diff(t)
    dexpr_w_t = expr_w_t.diff(t)
    print(f"{dexpr_no_t=}")
    print(f"{dexpr_w_t=}")
    dinterpa = interpa.diff(t)
    print(f"{dinterpa=}")
