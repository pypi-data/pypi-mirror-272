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

from collimator.experimental.acausal2.component_library.base import EqnEnv
from collimator.experimental.acausal2.diagram_processing import (
    DiagramProcessing,
    AcausalDiagram,
)
from collimator.experimental.acausal2.index_reduction.index_reduction import (
    IndexReduction,
)
from collimator.framework import LeafSystem, DependencyTicket
import sympy as sp
from collimator.backend import numpy_api as cnp


class AcausalSystem(LeafSystem):
    pass


class AcausalCompiler:
    """
    This class ochestrates the compilation of Acausal models to Acausal Phleafs.

    There are 3 primary stages:
        1] diagram_processing. AcausalDiagram -> DAEs
        2] index_reduction. DAEs -> index-1 DAEs
        3] phleaf_generation. index-1 DAEs -> pleaf
    """

    def __init__(self, eqn_env: EqnEnv, diagram: AcausalDiagram):
        self.dp = DiagramProcessing(eqn_env, diagram)
        # TODO: self.pg = PhleafGenerator()

    def diagram_processing(self):
        self.dp()

    def index_reduction(self):
        self.ir = IndexReduction(
            diag_proc_data=self.dp.index_reduction_inputs(),
            # verbose=True,
        )
        self.ir()

    def phleaf_generation(
        self,
        name="pwrcat",
        leaf_backend="numpy",
    ):
        """
        This function is used for generating a phleaf from a AcausalNetwork
        """
        if not self.dp.diagram_processing_done:
            self.diagram_processing()
        if not self.ir.index_reduction_done:
            self.index_reduction()

        # INITIAL STATE
        # FIXME: hard coded to 2 state variables
        x0 = cnp.array([0.0, 1.0])

        # LEAF SYSTEM
        phleaf = AcausalSystem(name=name)

        # INPUT PORTS
        # this ensure that inports of the phleaf are in the same order as
        # the 'inputs' portion of the lambdify args
        insym_to_portid = {}
        for sym in self.dp.diagram.input_syms:
            idx = phleaf.declare_input_port(name=sym.name)
            insym_to_portid[sym] = idx

        # COMMON TO ODE AND OUTPUTS
        # create the lambda functions input args tuple.
        # (time, states, inputs, params)
        time = self.dp.eqn_env.t
        # FIXME: hard coded to 2 state variables
        x1 = sp.Function("x1")(time)
        x2 = sp.Function("x2")(time)
        state = [x1, x2]
        inputs = [s.s for s in self.dp.diagram.input_syms]
        print(f"{inputs=}")
        params = [s.s for s in self.dp.params.keys()]
        lambda_args = (time, state, *inputs, *params)
        print(f"{lambda_args=}")

        # CONTINUOUS STATE AND DYNAMICS
        # FIXME: hard coded to 2 state derivatives
        if not inputs:
            dx1dt_expr = -4.0 * x2
            dx2dt_expr = x1
        else:
            # HACK: this is just to check if inputs can abe passed in
            dx1dt_expr = (inputs[0] - 1.0) * 2.0
            dx2dt_expr = 1.0
        lambdify_rhs = sp.lambdify(lambda_args, [dx1dt_expr, dx2dt_expr], leaf_backend)

        # PARAMETERS IN CONTEXT
        for k, v in self.dp.params.items():
            phleaf.declare_dynamic_parameter(str(k), v)

        def _ode(time, state, *inputs, **params):
            cstate = state.continuous_state
            param_values = [params[str(k)] for k in self.dp.params.keys()]
            return cnp.array(lambdify_rhs(time, cstate, *inputs, *param_values))

        phleaf.declare_continuous_state(default_value=x0, ode=_ode)

        # OUTPUT PORTS
        outsym_to_portid = {}
        if self.dp.diagram.num_outputs == 0:
            # if not output, output the state vector
            phleaf.declare_continuous_state_output(name=f"{phleaf.name}:output")
            outsym_to_portid = None
        else:

            def _make_outp_callback2(outp_expr):
                lambdify_output = sp.lambdify(lambda_args, outp_expr, leaf_backend)

                def _output_fun(time, state, *inputs, **params):
                    cstate = state.continuous_state
                    param_values = [params[str(k)] for k in self.dp.params.keys()]
                    return cnp.array(
                        lambdify_output(time, cstate, *inputs, *param_values)
                    )

                return _output_fun

            # declaring phleaf output ports in this order means that the ordering
            # 'source of truth' is self.model.output_syms which can be used to link
            # back to the acausal sensors causal port for diagram link src point remapping.
            for sym in self.dp.diagram.output_syms:
                # outp_expr = self.output_exprs[sym]
                # FIXME: hardcoded so that all output return the second state
                outp_expr = x1
                _output = _make_outp_callback2(outp_expr)
                idx = phleaf.declare_output_port(
                    _output,
                    name=sym.name,  # FIXME: not the name from the block port
                    prerequisites_of_calc=[DependencyTicket.xc],
                    requires_inputs=True,
                )
                outsym_to_portid[sym] = idx

        return phleaf, insym_to_portid, outsym_to_portid

    # execute compilation
    def __call__(self):
        self.diagram_processing()
        self.index_reduction()
        return self.phleaf_generation()
