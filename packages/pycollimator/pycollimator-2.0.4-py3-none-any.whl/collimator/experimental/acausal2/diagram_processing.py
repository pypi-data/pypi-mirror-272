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

import copy
import sympy as sp
from collimator.experimental.acausal2.component_library.base import (
    Eqn,
    Sym,
    SymKind,
    EqnKind,
    EqnEnv,
)


class AcausalDiagram:
    """
    collection of components and connections representing a network of acausal components.
    """

    def __init__(self, name=None, comp_list=None, cnctn_list=None):
        self.name = "sys" if name is None else name
        self.comps = set() if comp_list is None else set(comp_list)
        self.connections = [] if cnctn_list is None else cnctn_list
        self.syms = set()
        self.eqs = set()  # accumulate equations, and remove
        # dict[sym:cmp] needed to dereference syms to their source compnent
        self.sym_to_cmp = {}
        if comp_list is not None:
            for cmp in comp_list:
                self.add_cmp_syms(cmp)

    def connect(self, cmp_a, port_a, cmp_b, port_b):
        # add the components
        self.comps.update(set([cmp_a, cmp_b]))
        self.add_cmp_syms(cmp_a)
        self.add_cmp_syms(cmp_b)

        # add the symbols from each component
        self.syms.update(cmp_a.syms)
        self.syms.update(cmp_b.syms)

        # add the equations from the components
        self.eqs.update(cmp_a.eqs)
        self.eqs.update(cmp_b.eqs)

        # add the connection between the components
        self.connections.append(((cmp_a, port_a), (cmp_b, port_b)))

    def add_cmp_syms(self, cmp):
        if cmp not in self.sym_to_cmp.keys():
            for sym_ in list(cmp.syms):
                self.sym_to_cmp[sym_] = cmp

    @property
    def input_syms(self):
        syms = []
        for comp in self.comps:
            sym = comp.get_in_sym()
            if sym is not None:
                syms.append(sym)
        return syms

    @property
    def num_inputs(self):
        return len(self.input_syms)

    @property
    def has_inputs(self):
        return self.num_inputs > 0

    @property
    def output_syms(self):
        syms = []
        for comp in self.comps:
            sym = comp.get_out_sym()
            if sym is not None:
                syms.append(sym)
        return syms

    @property
    def num_outputs(self):
        return len(self.output_syms)

    @property
    def has_outputs(self):
        return self.num_outputs > 0


class DiagramProcessing:
    """
    This class transforms an AcausalDiagram object into a set of differential algebraic equations.
    The output form this class is the input for index reduction.

    The stages of diagram_processing (in order):
    - identify the AcausalDiagram nodes
    - generate node flow equations.
    - generate node potential variables and equations.
    - add derivative relation equations. e.g. ff(t) = Derivative(f(t))
    - 'finalize', i.e. update sets of equations and symbols.
    - alias elimination
    - prune unnecesary derivative relations. some ff(t) were eliminated by alias elimination, their derivative relations are not needed.
    - initial condition consistency check
    - identify params, inputs, and outputs.
    - prepare inputs for index reduction
    """

    def __init__(self, eqn_env: EqnEnv, diagram: AcausalDiagram):
        self.eqn_env = eqn_env
        self.diagram = diagram

        syms = list(diagram.syms)
        if eqn_env.fluid is not None:
            syms.append(eqn_env.fluid.density)
            syms.append(eqn_env.fluid.viscosity)
        # ordered(indexed) symbols and equations sets
        self.syms = {idx: s for idx, s in enumerate(syms)}
        self.next_sym_idx = len(self.syms.keys())
        self.eqs = {idx: e for idx, e in enumerate(diagram.eqs)}
        # dict{sympy symbol: parent 'Sym' object} used to dereference to the parent.
        self.update_syms_map()

        self.eqs_original = {}  # copy of eqs, but never perform any substitutions.
        self.syms_original = {}
        self.syms_map_original = {}

        self.nodes = {}  # dict of node_id to set of ports
        self.node_domains = {}  # dict of node_id to node domain
        self.pot_alias_map = {}  # dict{node_id:dict{der_idx:pot_sym}}
        self.alias_map = {}  # dict from Sym removed to Sym that replaced it.
        self.alias_eqs = []  # list of the equation in which alises were found.
        # dict{aliaser:[aliasees]} aliasees are replaced by aliasers
        self.aliaser_map = {}
        self.sym_ic = {}  # dict from Sympy.symbol to it's initial condition value
        self.params = {}  # dict from param symbol to param value
        self.inputs = []  # list of input Sym objects
        self.outputs = []  # list of input Sym objects
        self.diagram_processing_done = False

    # helper functions for diagram processing
    def pp_eqs(self, eqs_all=False, tabs=""):
        if self.eqs_original:
            print(tabs + "original equations")
            for idx, eq in self.eqs_original.items():
                print(tabs + f"\t{idx}: {eq}")
        print(tabs + "equations")
        for eq_idx, eq in self.eqs.items():
            print(tabs + f"\t{eq_idx}: {eq}")

    def sanitize_solve(self, s, eq):
        # handle the various options for what can be returned from solve().
        exprs = sp.solve(eq.e, s)
        if isinstance(exprs, list):
            if len(exprs) > 1:
                raise RuntimeError(
                    f"solving {eq} for {s} produced more than one solution:{exprs}."
                )
            elif len(exprs) == 0:
                raise RuntimeError(f"solving {eq} for {s} produced no solutions.")
            else:
                return exprs[0]
        else:
            # @am. its not clear whether 'not a list' is an acceptable outcome,
            # so block it for now.
            print(f"sanitize_solve failed: s={s}, eq={eq}")
            raise RuntimeError("sanitize_solve expr arg is not a list.")

    def pp(self):
        print(f"DiagramProcessing {self.diagram.name}:")

        print(f"\tComponents:{[c.name for c in self.diagram.comps]}")

        print("\tConnections:")
        for port_tuple_a, port_tuple_b in self.diagram.connections:
            ca, pa = port_tuple_a
            cb, pb = port_tuple_b
            print(f"\t\t{ca.name},{pa}\tto {cb.name},{pb}")

        print(f"\tsyms:{self.syms}")

        self.pp_eqs(tabs="\t")

        print("\tnode_sets:")
        for id, nset in self.nodes.items():
            if len(nset) > 3:
                print(f"\t\t{id}:")
                for n in nset:
                    print(f"\t\t\t{n}:")
            else:
                print(f"\t\t{id}:{nset}")

        print(f"\tsym_ic={self.sym_ic}")
        print(f"\tparams={self.params}")
        print(f"\tinputs={self.inputs}")
        print(f"\toutputs={self.outputs}")

        print(f"end {self.diagram.name}\n")

    def pp_nodepots(self):
        print("=================== pp nodepots")
        for nodepots in self.pot_alias_map.values():
            for der_idx, n in nodepots.items():
                print(f"{n.name}. ic={n.ic}")

    def eqs_append(self, eq):
        self.eqs[len(self.eqs)] = eq

    def update_syms(self):
        # find all unique symbols in all active equations,
        # rebuilt self.syms from the symbols found.
        remaining_syms = set()
        for eq in self.eqs.values():
            symbols = eq.e.atoms(sp.Symbol)
            symbols.discard(self.eqn_env.t)
            fcns = eq.e.atoms(sp.Function)
            remaining_syms.update(symbols)
            remaining_syms.update(fcns)

        remaining_syms = list(remaining_syms)
        remaining_syms = [self.syms_map[s] for s in remaining_syms]
        self.syms = {i: s for i, s in self.syms.items() if s in remaining_syms}

    def get_some_syms(self, eqn_kind_filter: list = None):
        # similar to update_syms, but has filter to only find
        # a subset of the symbols based on their SymKind.
        remaining_syms = set()
        for eq in self.eqs.values():
            if eq.kind in eqn_kind_filter:
                continue
            symbols = eq.e.atoms(sp.Symbol)
            symbols.discard(self.eqn_env.t)
            fcns = eq.e.atoms(sp.Function)
            remaining_syms.update(symbols)
            remaining_syms.update(fcns)

        remaining_syms = list(remaining_syms)
        remaining_syms = [self.syms_map[s] for s in remaining_syms]
        syms_new = {i: s for i, s in self.syms.items() if s in remaining_syms}

        return syms_new

    def update_syms_map(self):
        # update the inverse mapping from Sympy Symbol to Sym object.
        self.syms_map = {s.s: s for s in self.syms.values()}

    def eqs_subs(self, sym, sub_expr):
        # given a substitution pair, perform the substitution in any
        # active equation where the substitution is applicable.
        # for any instances of function symbols appearing in an equation
        # which have as their args, the symbol being replace, this sub
        # will be applied. this means that the instance of the function
        # symbol will differ from the symbol key in the self.syms dict.
        # syms_subs() below is meant to fix this discrepancy.
        for i, eq in self.eqs.items():
            self.eqs[i] = eq.subs(sym, sub_expr)

    def syms_subs(self, sym, sub_expr):
        # given a substitution pair, perform the  subsitution in any
        # symbol where the substitution is applicable.
        # for example, the symbol for a lookup table function is:
        #   interp(x,xp,fp)
        # if the substitution pair is x->a, then this function will
        # update the value in self.syms so that the value matches any
        # instance of the value's symbol in the equations.
        for i, s in self.syms.items():
            if s.kind == SymKind.lut:
                del self.syms_map[s.s]
                s_new = s.subs(sym, sub_expr)
                self.syms[i] = s_new
                self.syms_map[s.s] = s_new

    def check_port_set_domain(self, port_set, node_id):
        domain = None
        for port_tuple in port_set:
            comp, port_name = port_tuple
            port = comp.ports[port_name]
            if domain is None:
                domain = port.domain
            else:
                assert (
                    port.domain == domain
                ), f"node {node_id} has ports mismatched domains: {domain} and {port.domain}"

        return domain

    def add_sym(self, sym):
        self.syms[self.next_sym_idx] = sym
        self.next_sym_idx += 1

    # methods for diagram processing start here.
    def identify_nodes(self):
        """
        This function does the following;
         - identify the nodes of the network. nodes are junctions between two or more components.
         - verify that all ports connected to the node are of the same domain.

        Naive algorithm to sort port-pairs into sets of ports belonging to a node in the network.
        Start by assuming each port-pair is its own node, i.e. a network with components connected in a line.
        Intialize a dict 'nodes' by enumerating each of these into a dict{1:set1,2:set2, ...etc.}
        Initial 'workset' as a list nodes.keys(), e.g. a list fo all the node IDs.
        Then, pop an ID from workset, and pop the corresponding node(N) from 'nodes'.
            check if any other node shares a port with N,
                if say node M shares a port with N, merge all ports of node N into node M, leaving M in 'nodes'.
                if no other nodes share a port with N, re-add N to workset, because it is a complete node.
        If workset empty, we are done.
        """
        # print("AcausalCompiler.identify_nodes()")
        nodes = {
            id: set(port_pair) for id, port_pair in enumerate(self.diagram.connections)
        }
        workset = list(nodes.keys())
        while workset:
            this_id = workset.pop()
            this_port_set = nodes.pop(this_id)
            # print(f'this_id={this_id}, this_port_set={this_port_set}, workset={workset}')
            this_set_grouped = False
            for node_id, port_set in nodes.items():
                if not port_set.isdisjoint(this_port_set):
                    nodes[node_id].update(this_port_set)
                    this_set_grouped = True

            if not this_set_grouped:
                nodes[this_id] = this_port_set
                self.node_domains[this_id] = self.check_port_set_domain(
                    this_port_set, this_id
                )

        # print(f"self.node_domains={self.node_domains}")
        self.nodes = nodes

    def add_node_flow_eqs(self):
        """
        For each node in the system, generate the flow equations.
        sum(all flow syms) = 0
        """

        # print("AcausalCompiler.add_node_eqs()")
        for node_id, port_set in self.nodes.items():
            flow_syms_on_node = set()

            for port_tuple in port_set:
                cmp, port_id = port_tuple
                port = cmp.ports[port_id]

                # collect the flow symbols to create balancing equation for node
                flow_syms_on_node.add(port.flow.s)

            # create and save the balancing equation for the node
            sum_expr = sp.core.add.Add(*flow_syms_on_node)
            eq = Eqn(e=sp.Eq(0, sum_expr), kind=EqnKind.flow, node_id=node_id)
            self.eqs_append(eq)

    def add_node_potential_eqs(self):
        """
        For each node in the system, generate the potential variable constraint
        equations.

        Constraints are made between the potential variable of the node, and the
        potential variable of a component connected to the node. So if components
        A, B, C are connected to a node, we will generate the following contraint
        equations: Np=Ap, Np=Bp, Np=Cp. Where Np is the node potential variable.

        Additionally, we need to create these constraints for each of the variables
        in the 'derivative index'.

        The 'derivative index' of a potential variable is a measure of how many derivatives there
        are of the underlying variable, for which the potential variable is either that underlying
        variable, or one of its derivatives.

        This is best explained by examples.
        MechTrans: the potential variable is velocity; however, the underlying variable is position,
        and the derivative index includes the acceleration.
        Elec: the potential variable is the pin voltage (not the voltage across the component),
        this is also the underlying variable, and there are no further derivatives.

        If we think of derivatives in an ordinal sense, and say that the potential variable is
        0, then for the examples above, the 'derivative index' are:
        MechTrans: [-1,1] i.e. position is -1 because it is an integral of potential variable velocity,
        and acceleration is 1 because it is a derivative of velocity.
        Elec: [0,0] i.e. the terminal/pin voltage has no integrals nor derivatives defined.

        The 'derivative index' of potential variables is required because it defines the set of
        contraint equations required for a given node. Continuing with the exmaples:
        MechTrans: if components A and B are connected at the node, we need 3 constraint equations,
        Ax=Bx, Av=Bv, Aa=Ba. This means that the initial conditions for these must be consistent as well.
        Elec: if components C and D are connected at the node, we need 1 constraint equation,
        C_volts = D_volts. Recall, C_volts and D_volts are pin voltages, not voltages across components.

        However, rather than create constraints between components directly, we do so between the node
        variables and the components variables. These 'constrains' are also alias equations, which
        means that during alias elimination, we will remove all the components potential variables,
        retaining only the node potential variables. Of course nothing is lost, because via the
        compiler alias_map, we can always know the value of any component potential variable.

        """

        for node_id, port_set in self.nodes.items():
            # start defining potential symbols family for the node
            node_alias_map = {}
            for port_tuple in port_set:
                cmp, port_id = port_tuple
                port = cmp.ports[port_id]

                # then all the 'integrals' of the potential variable
                this_var = port.pot
                der_idx = -1
                while this_var.int_sym is not None:
                    if der_idx not in node_alias_map.keys():
                        node_pot = Sym(
                            self.eqn_env,
                            name=f"np{node_id}_n{abs(der_idx)}",
                            kind=SymKind.node_pot,
                        )
                        self.add_sym(node_pot)
                        node_alias_map[der_idx] = node_pot
                    else:
                        node_pot = node_alias_map[der_idx]
                    self.eqs_append(
                        Eqn(
                            e=sp.Eq(node_pot.s, this_var.int_sym.s),
                            kind=EqnKind.pot,
                            node_id=node_id,
                        )
                    )
                    der_idx -= 1
                    this_var = this_var.int_sym

                # do the pot var here so dict indices are naturally in order.
                # this is temporary. eventually we can sort them.
                if 0 not in node_alias_map.keys():
                    node_pot = Sym(
                        self.eqn_env, name=f"np{node_id}_0", kind=SymKind.node_pot
                    )
                    self.add_sym(node_pot)
                    node_alias_map[0] = node_pot
                else:
                    node_pot = node_alias_map[0]
                # constraint equation for the potential variable
                self.eqs_append(
                    Eqn(
                        e=sp.Eq(node_pot.s, port.pot.s),
                        kind=EqnKind.pot,
                        node_id=node_id,
                    )
                )

                # then all the 'derivatives' of the potential variable
                this_var = port.pot
                der_idx = 1
                while this_var.der_sym is not None:
                    if der_idx not in node_alias_map.keys():
                        node_pot = Sym(
                            self.eqn_env,
                            name=f"np{node_id}_p{abs(der_idx)}",
                            kind=SymKind.node_pot,
                        )
                        self.add_sym(node_pot)
                        node_alias_map[der_idx] = node_pot
                    else:
                        node_pot = node_alias_map[der_idx]
                    self.eqs_append(
                        Eqn(
                            e=sp.Eq(node_pot.s, this_var.der_sym.s),
                            kind=EqnKind.pot,
                            node_id=node_id,
                        )
                    )
                    der_idx += 1
                    this_var = this_var.der_sym

            self.pot_alias_map[node_id] = node_alias_map

            # update the int_sym and der_sym of the newly created pot vars
            pot_min = min(node_alias_map.keys())
            pot_max = max(node_alias_map.keys())
            # go from underlying variable to highest derivative, adding the der_sym
            for der_idx in range(pot_min, pot_max):
                this_pot = node_alias_map[der_idx]
                this_pot.der_sym = node_alias_map[der_idx + 1]
            # go from highest derivative, to underlying variable, adding the int_sym
            for der_idx in range(pot_max, pot_min, -1):
                this_pot = node_alias_map[der_idx]
                this_pot.int_sym = node_alias_map[der_idx - 1]

            # denug print
            # print("\n+++++++++++++++++++++++++")
            # for idx, np in node_alias_map.items():
            #     print(
            #         f"\tder_idx={der_idx} der_sym={np.der_sym} np={np} int_sym={np.int_sym}"
            #     )

        # print(f"pot_alias_map={self.pot_alias_map}")

    def add_derivative_relations(self):
        """
        iterate over symbols and collect any derivative relation equations.
        """
        for sym in self.syms.values():
            if sym.der_relation is not None:
                self.eqs_append(eq=sym.der_relation)

    def finalize_equations(self):
        """
        The addition of equations to the system is complete.
        This function just records the status such that at any
        point we can always see what were all the equations.
        Note, there are no new symbols created beyond those created
        by the components, equations however, are created, using
        symbols from the components.
        """
        self.update_syms_map()
        self.eqs_original = copy.deepcopy(self.eqs)
        self.syms_original = copy.deepcopy(self.syms)
        self.syms_map_original = copy.deepcopy(self.syms_map)

    def alias_elimination(self):
        """
        Find equations of the form:
            type 0: a=b, a=-b
            type 1: 0=a+b, 0=a-b
            type 2: a+b=0, a-b=0
            type 3: 0=a
            type 4: a=0
        Replaces all a with b, or replaces a with 0,and removes the equation from system.
        The substitution process changes all equations which include a, this means it is
        possible the change transforms an equation that previously did not match any
        of the types above, but now does. This means we need to use a workset to ensure
        the process converges to a 'fixed point' where no more equations in the system match
        any of the types above.

        Note: it's not deterministic because Sympy returns sets,
        and therefore the it's not always the same replacements that happen, even for
        sequential runs with the same diagram.

        what about equations of the form:
            type 5: 1=a/g
            type 6: a=1/g
            type 5: const=a, a=const

        What about initial conditions? This is handled later, and since we keep a record of
        what aliased what, we can always go back and ensure any alias set has initial
        conditions verified for consistency and completeness.
        """
        # print("\nCompiler.alias_elimination()")

        def alias_priorities(symbols):
            # 'alias_sym' is the one being replaced everywhere by something else.
            # never replace Syms with kind = "params", or "in"
            inp_or_param = [SymKind.inp, SymKind.param]
            sym0 = symbols.pop()
            if symbols:
                sym1 = symbols.pop()
                s0s = self.syms_map[sym0]
                s1s = self.syms_map[sym1]
                # print(f"\t\t[alias_priorities] {s0s}:{s0s.kind} {s1s}:{s1s.kind}")
                if s0s.kind in inp_or_param:
                    return sym1
                elif s1s.kind in inp_or_param:
                    return sym0
                elif s0s.kind == SymKind.node_pot:
                    return sym1
                elif s1s.kind == SymKind.node_pot:
                    return sym0
                else:
                    return sym0  # arbitrary
            else:
                # the alias equation only had one sym, the other side was 0
                return sym0

        workset = list(self.eqs.keys())
        while workset:
            eq_idx = workset.pop()
            eq = self.eqs[eq_idx]
            alias_sym = None
            if eq.kind == EqnKind.pot:
                # when dealing with potential variable aliases, always chose the
                # component var to be replaced. when potential equations are created,
                # they always have the node_pot on LHS, and comp_pot on RHS.
                alias_sym = eq.e.rhs.atoms(sp.Function).pop()
            elif isinstance(eq.e, sp.logic.boolalg.BooleanTrue):
                # alias elimination has resulted in a equation like 0 = a - a = 0 -> BooleanTrue;
                # therefore, remove eqn from eqs.
                del self.eqs[eq_idx]
            elif eq.kind == EqnKind.der_relation:
                # derivative relation equations are alias equations by design.
                # derivative relations are alias equations that might need to be in the
                # final set of equations, so we do not consider them as opportunities
                # for simplification.
                pass
            else:
                # print("\n\n===========================")
                # print(f"{eq_idx} eq={eq}")
                # we should never have Derivative(f(t),t) in any 'system equations'.
                # 'system equations should use the alias symbol for Derivative(f(t),t),
                # and this alias relationship is resolved in the derivative relation equations.
                if len(eq.e.atoms(sp.Derivative)) > 0:
                    raise RuntimeError(
                        f"{eq_idx}: {eq} has sombols of type Sympy.Derivative. not allowed"
                    )
                lhs_symbols = eq.e.lhs.atoms(sp.Symbol)
                lhs_symbols.discard(self.eqn_env.t)
                lhs_fcns = eq.e.lhs.atoms(sp.Function)

                rhs_symbols = eq.e.rhs.atoms(sp.Symbol)
                rhs_symbols.discard(self.eqn_env.t)
                rhs_fcns = eq.e.rhs.atoms(sp.Function)

                # print(f"lhs_symbols={lhs_symbols} rhs_symbols={rhs_symbols}")
                # print(f"lhs_fcns={lhs_fcns} rhs_fcns={rhs_fcns}")

                # conditions for type0: a=b, a=-b
                lhs_1_sym = len(lhs_symbols) + len(lhs_fcns) == 1
                rhs_1_sym = len(rhs_symbols) + len(rhs_fcns) == 1
                is_type0 = lhs_1_sym and rhs_1_sym

                # conditions for type1: 0=a+b, 0=a-b
                type1_sym_or_fun = len(rhs_symbols) + len(rhs_fcns) == 2
                is_type1 = eq.e.rhs.is_Add and eq.e.lhs == 0 and type1_sym_or_fun

                # conditions for type2: a+b=0, a-b=0
                type2_sym_or_fun = len(lhs_symbols) + len(lhs_fcns) == 2
                is_type2 = eq.e.lhs.is_Add and eq.e.rhs == 0 and type2_sym_or_fun

                # conditions for types3: 0=a
                is_type3 = eq.e.lhs == 0 and len(rhs_symbols) + len(rhs_fcns) == 1

                # conditions for types4: a=0
                is_type4 = eq.e.rhs == 0 and len(lhs_symbols) + len(lhs_fcns) == 1

                # alias elimination
                if is_type0 or is_type1 or is_type2 or is_type3 or is_type4:
                    self.alias_eqs.append(eq_idx)
                    eq_symbols = lhs_symbols | rhs_symbols | lhs_fcns | rhs_fcns
                    alias_sym = alias_priorities(eq_symbols)

            if alias_sym is not None:
                # print(f"alias_sym={alias_sym} eqn {eq.e}. ")
                # track the relationship: alias->substitution_expression
                alias_sub_expr = self.sanitize_solve(alias_sym, eq)
                self.alias_map[alias_sym] = alias_sub_expr

                # track the inverse relationship: substituter->alias_expression
                # it happens that the substituter is 0, in this case we don't track it.
                # the main reason we need this is as input to initial_condition_validation().
                # see the method documentation for more details.
                aliasee = self.syms_map[alias_sym]
                sub_expr_fcns = alias_sub_expr.atoms(sp.Function)
                sub_expr_symbols = alias_sub_expr.atoms(sp.Symbol)
                sub_expr_symbols.discard(self.eqn_env.t)
                aliaser_sym = None
                if sub_expr_fcns:
                    aliaser_sym = sub_expr_fcns.pop()
                elif sub_expr_symbols:
                    aliaser_sym = sub_expr_symbols.pop()

                if aliaser_sym is not None:
                    aliaser = self.syms_map[aliaser_sym]
                    # print(f"aliaser={aliaser} eqn {eq.e}. ")
                    if aliaser.kind == SymKind.node_pot:
                        aliasee_expr = alias_sym
                    else:
                        aliasee_expr = self.sanitize_solve(aliaser_sym, eq)
                    aliasee_list = self.aliaser_map.get(aliaser, [])
                    aliasee_list.append((aliasee, aliasee_expr))
                    self.aliaser_map[aliaser] = aliasee_list

                # perform the substitution
                self.eqs_subs(alias_sym, alias_sub_expr)
                self.syms_subs(alias_sym, alias_sub_expr)

                # remove eqn from eqs.
                del self.eqs[eq_idx]
                # print(f"substitute {alias_sym} with {alias_sub_expr}")

                # re-add all indices to the workset.
                # FIXME: really we only need to re-add those indices that were
                # changed by the self.eqs_subs() call above.
                workset = list(self.eqs.keys())

        # prune syms to only those found in the remaining equations.
        self.update_syms()
        # debug prints
        # print("alias_map:")
        # for ae, ar in self.alias_map.items():
        #     aes = self.syms_map_original[ae]
        #     print(f"\t{ae}:{aes.kind}->{ar}")
        # print("syms_map_original:")
        # for ss, sym in self.syms_map_original.items():
        #     print(f"\t{ss}:{sym}")
        # print("syms_map:")
        # for ss, sym in self.syms_map.items():
        #     print(f"\t{ss}:{sym}")
        # self.pp_eqs()

    def prune_derivative_relations(self):
        """
        iterate over equations and remove any derivative relations that do not define the system.
        """
        # print("======================== prune_derivative_relations")
        # get the syms in the system equations. do not get symbols from derivative relation equations.
        eqs_syms = self.get_some_syms(eqn_kind_filter=["der_relation"])
        eqs_syms = list(eqs_syms.values())
        # print(f"eqs_syms={eqs_syms}")

        # get all their derivative family
        syms_relatives = set()
        for sym in eqs_syms:
            this_var = sym
            while this_var.int_sym is not None:
                syms_relatives.add(this_var.int_sym)
                this_var = this_var.int_sym
            this_var = sym
            while this_var.der_sym is not None:
                syms_relatives.add(this_var.der_sym)
                this_var = this_var.der_sym

        # print(f"syms_relatives={syms_relatives}")

        # get a list of eqn syms and their relatives. no duplicates, so use set1.union(set2).
        eqs_syms = list(set(eqs_syms) | syms_relatives)
        eqs_syms = set([s.s for s in eqs_syms])
        # print(f"eqs_syms={eqs_syms}")

        # iterate over the derivative relation equations, and identify all those which are
        # NOT needed to define a time derivative relationship between two sp.Function symbols
        # appearing in the 'system equations'.
        remove_eq_ids = []
        lshs = set()
        for eq_idx, eq in self.eqs.items():
            if eq.kind == EqnKind.der_relation:
                # print(f"\n\t {eq_idx}: {eq}")
                if eq.e.lhs == 0:
                    # the intent is to match equations of form Eq(0, Derivative(0, t))
                    # FIXME: the condition above is potentially inadequately robust.
                    # i tried eq.e.match(sp.Eq(0, sp.Derivative(0, self.eqn_env.t))),
                    # but that didn't work for some reason.
                    # since we declare der_relations like ff(t) = Derivative(f(t)), the
                    # naive condition used here seems to work 'all' the time.
                    # print("\t remove because it is 0=der(0)")
                    remove_eq_ids.append(eq_idx)
                    continue

                lhs_fcns = eq.e.lhs.atoms(sp.Function)
                rhs_fcns = eq.e.rhs.atoms(sp.Function)
                # print(f"\t lhs_fcns={lhs_fcns} rhs_fcns={rhs_fcns}")

                # print(f"\t lshs={lshs}")
                if lhs_fcns.issubset(lshs):
                    # the intent is to remove derivative_relations which have been made
                    # identical to
                    # print("\t remove because its a duplicate")
                    remove_eq_ids.append(eq_idx)
                    continue

                fncs = lhs_fcns | rhs_fcns
                # intersection = eqs_syms.intersection(fncs)
                intersection = fncs.issubset(eqs_syms)
                # print(f"\t intersection={intersection}")
                if not intersection:
                    # the intent is to remove der_relations for which neither of their symbols
                    # appear in the fimal 'system equations'.
                    # print("\t remove because no matching symbols")
                    remove_eq_ids.append(eq_idx)
                    continue

                # if we cant remove this derivative relation, keep track of its lhs,
                # that way, if we find a duplicate der_relation, we can remove the duplicate.
                lshs.update(lhs_fcns)

        # print(f"remove_eq_ids={remove_eq_ids}")

        for idx in remove_eq_ids:
            del self.eqs[idx]

    def initial_condition_validation(self):
        """
        For all alias sets, verify that the initial conditions for all symbols in
        an alias set are consistent and complete.

        When an aliaser replaces several
        aliasees, there may be one or more aliasees that have initial conditions
        specificed in the diagram. to ensure that these intial conditions are
        all respected and consistent, we will evaluate each alisees initial
        condition in its aliasee_expr, to get the initial condition from the
        view of the aliaser. Then, including any initial condition directly assigned
        to the aliaser, we now have a set of source initial conditions
        for the aliaser, and can chose an appropriate initial condition for the set,
        by processing that it for consistency (all values are the same).
        Although the above may seem like it is relying too many assumptions about
        aliasee<->aliaser relationship, this is not the case, because alias elimination
        only choses these pairs from equations which have been established to define
        these simple relationships between exactly 2 symbols.

        if aliaser and all aliasses initial conditions are none, we just leave it as that.
        """
        for aliaser, aliasee_pairs in self.aliaser_map.items():
            aliasees_ics = []
            for alias, alias_expr in aliasee_pairs:
                if alias.ic is not None:
                    alias_to_aliaser_ic = alias_expr.subs(alias.s, alias.ic)
                    aliasees_ics.append(alias_to_aliaser_ic)

            for ic in aliasees_ics:
                if aliaser.ic is None and ic is not None:
                    aliaser.ic = ic
                elif ic is not None and ic != aliaser.ic:
                    raise AssertionError("conflicting ICs")

    def get_params_ic_interface(self):
        """
        This collects the symbols that meet certain conditions. This is
        just for conveniece of getting these at some later stage.
        """
        # print("AcausalCompiler.get_params_ic_inputs()")

        for sym in self.syms.values():
            if sym.ic is not None:
                self.sym_ic[sym.s] = sym.ic
            elif sym.kind == SymKind.param:
                self.params[sym] = sym.val
            elif sym.kind == SymKind.inp:
                self.inputs.append(sym)
            elif sym.kind == SymKind.outp:
                self.outputs.append(sym)

    def index_reduction_inputs(self):
        """
        collect the various lists, dicts, sets of info required by index reduction.
        nothing new computed really, just repackaging/organizing existing data.

        t = EqnEnv.t
        x = list of all differetiated variables
        x_dot = list of RHS of each der_relation
        y = list of all algebraic variables
        X = list(y,x,x_dot)
        exprs = list[eq.expr for eq in self.eqs.values()]
        vars_in_exprs = dict{expr:[all_members_of_X_in_eq]}
        exprs_idx = dict{expr:idx for idx,expr in self.eqs.values()}
        knowns = dict{sym.s:val} when sym.kind in [in,out,param,lut]
        known_vars = set(self.knowns.keys())
        ics = dict{sym.s:sym.ic for sym in X when sym.ic is not None}
        """
        # collect x and x_dot
        x = []
        x_dot = []
        for eq_idx, eq in self.eqs.items():
            if eq.kind == EqnKind.der_relation:
                x_el = eq.e.rhs.atoms(sp.Function).pop()
                x.append(x_el)
                x_dot.append(x_el.diff(self.eqn_env.t))
                # this was the original idea, but this occassionally results
                # one of: -Der(f(t),t) or Der(-f(t),t), and those '-' seem to
                # break index reduction because they make the Der() symbol more
                # like an expression, whihc is not what is needed.
                # self.x_dot.append(sp.simplify(eq.e.rhs))

        # create a list of all syms that cant be in y
        x_set = set(x)
        x_dot_set = set(x_dot)
        knowns_keys = (
            [s.s for s in self.params]
            + [s.s for s in self.inputs]
            + [s.s for s in self.outputs]
            + [s.s for s in self.syms.values() if s.kind == SymKind.lut]
        )
        knowns = {}
        for known in knowns_keys:
            # FIXME: always 0.0 for inputs, outputs, lookup_tables
            knowns[known] = known.val if known.kind == SymKind.param else 0.0
        known_vars = set(knowns_keys)
        print(f"{known_vars=}")
        not_y_list = list(x_set | x_dot_set | known_vars)

        # collect y by getting all other syms
        y = [s.s for s in self.syms.values() if s.s not in not_y_list]

        X = x_set | x_dot_set | set(y)

        exprs = []
        exprs_idx = {}
        vars_in_exprs = {}
        for eq_idx, eq in self.eqs.items():
            # list of expressions, from the equations
            # FIXME: this fixes Der(-x(t),t), which presently trip up index reduction
            # self.exprs[eq_idx] = sp.simplify(eq.expr)
            expr = sp.simplify(eq.expr)
            exprs.append(expr)
            exprs_idx[expr] = eq_idx

            # list of which variables appear in which expression
            ders = expr.atoms(sp.Derivative)
            symbols = expr.atoms(sp.Symbol)
            symbols.discard(self.eqn_env.t)
            fcns = expr.atoms(sp.Function)

            syms_set = ders | symbols | fcns
            vars_in_exprs[expr] = X & syms_set  # intersection

        X = list(X)

        # self.ics = [self.sym_ic.get(s, None) for s in X]
        # ics = {sym.s: sym.ic for sym in X if sym.ic is not None}
        ics = {}
        for s in X:
            sym = self.syms_map.get(s, None)
            if sym is not None and sym.ic is not None:
                ics[s] = sym.ic
        print(f"{x_dot=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{X=}")
        print(f"{exprs=}")
        print(f"{vars_in_exprs=}")
        print(f"{knowns=}")
        print(f"{ics=}")
        return (
            self.eqn_env.t,
            x,
            x_dot,
            y,
            X,
            exprs,
            vars_in_exprs,
            exprs_idx,
            knowns,
            known_vars,
            ics,
        )

    def diagram_processing(self):
        self.identify_nodes()
        self.add_node_flow_eqs()
        self.add_node_potential_eqs()
        self.add_derivative_relations()
        self.finalize_equations()  # just book keeping
        self.alias_elimination()
        self.initial_condition_validation()
        self.prune_derivative_relations()
        self.get_params_ic_interface()
        self.index_reduction_inputs()
        self.pp()
        self.diagram_processing_done = True

    # execute compilation
    def __call__(self):
        self.diagram_processing()
