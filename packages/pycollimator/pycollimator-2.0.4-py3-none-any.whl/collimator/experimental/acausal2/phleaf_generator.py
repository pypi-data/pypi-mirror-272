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
from collimator.framework import LeafSystem, DependencyTicket
from collimator.backend import numpy_api as cnp


class PhleafGenerator:
    """
    This class transforms index-1 DAEs into a wildcat leaf system.
    PHLEAF stands for 'PHysical model LEAF system'.

    substages of phleaf generation:
    TBD
    """

    def __init__(self):
        pass

    # methods for phleaf generation start here.
    def generate_phleaf(
        self,
        name="phleaf",
        leaf_backend="jax",
    ):
        """
        This function is used for generating a phleaf from a AcausalNetwork
        """
        if not self.diagram_processing_done:
            self.diagram_processing()
        if not self.index_reduction_done:
            self.index_reduction()

        # LEAF SYSTEM
        phleaf = LeafSystem(name=name)

        # INPUT PORTS
        # this ensure that inports of the phleaf are in the same order as
        # the 'inputs' portion of the lambdify args
        insym_to_portid = {}
        for sym in self.diagram.input_syms:
            idx = phleaf.declare_input_port(name=sym.name)
            insym_to_portid[sym] = idx

        # COMMON TO ODE AND OUTPUTS
        # create the lambda functions input args tuple.
        # (time, states, inputs, params)
        time = self.eqn_env.t
        state = []  # list(s.s for s in self.rhs_exprs.keys()) FIXME
        inputs = self.diagram.input_syms
        params = list(s.s for s in self.params.keys())
        lambda_args = (time, state, *inputs, *params)

        # PARAMETERS IN CONTEXT
        for k, v in self.params.items():
            phleaf.declare_dynamic_parameter(str(k), v)

        # CONTINUOUS STATE AND DYNAMICS
        # FIXME: this needs to define the call back for LeafSystem DAE interface
        # x0 = ???
        # lambdify_rhs = sp.lambdify(
        #     lambda_args, list(self.rhs_exprs.values()), leaf_backend
        # )

        # def _ode(time, state, *inputs, **params):
        #     cstate = state.continuous_state
        #     param_values = [params[str(k)] for k in self.params.keys()]
        #     return cnp.array(lambdify_rhs(time, cstate, *inputs, *param_values))

        # phleaf.declare_continuous_state(default_value=x0, ode=_ode)

        # OUTPUT PORTS
        outsym_to_portid = {}
        if self.diagram.num_outputs == 0:
            # if not output, output the state vector
            phleaf.declare_continuous_state_output(name=f"{phleaf.name}:output")
            outsym_to_portid = None
        else:

            def _make_outp_callback2(outp_expr):
                lambdify_output = sp.lambdify(lambda_args, outp_expr, leaf_backend)

                def _output_fun(time, state, *inputs, **params):
                    cstate = state.continuous_state
                    param_values = [params[str(k)] for k in self.params.keys()]
                    return cnp.array(
                        lambdify_output(time, cstate, *inputs, *param_values)
                    )

                return _output_fun

            # declaring phleaf output ports in this order means that the ordering
            # 'source of truth' is self.diagramoutput_syms which can be used to link
            # back to the acausal sensors causal port for diagram link src point remapping.
            for sym in self.diagramoutput_syms:
                outp_expr = self.output_exprs[sym]
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
        self.generate_phleaf()
