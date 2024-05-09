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

import warnings
import networkx as nx
from networkx.algorithms import bipartite

import sympy as sp

from .graph_utils import (
    delete_var_nodes_with_zero_A,
    augmentpath,
    is_structurally_feasible,
    sort_block_by_number_of_eq_derivatives,
)
from .equation_utils import process_equations, compute_consistent_initial_conditions


class IndexReduction:
    """
    Class to perform index reduction of a DAE system using the Pantelides algorithm
    and the method of dummy derivatives.

    Pantelides, C.C., 1988. The consistent initialization of differential-algebraic
    systems. SIAM Journal on scientific and statistical computing, 9(2), pp.213-231.

    Mattsson, S.E. and Söderlind, G., 1993. Index reduction in differential-algebraic
    equations using dummy derivatives. SIAM Journal on Scientific Computing, 14(3).

    Parameters:
        t : sympy.Symbol
            The independent variable representing time.
        eqs : list of sympy.Expr
            The list of expressions (`expr`) in the DAE system. Each equation is assumed
            to be `expr=0`.
        knowns : dict
            Dictionary of known variables in the DAE system. The keys are the known
            sympy variables and the values are their corresponding numeric values.
        ics : dict
            Dictionary of initial conditions for the DAE system. The keys are the
            sympy variables and the values are the numerical initial values.
    """

    def __init__(
        self,
        t=None,
        eqs=None,
        knowns=None,
        ics=None,  # is this really optional?
        diag_proc_data=None,
        verbose=False,
    ):
        self.verbose = verbose
        self.index_reduction_done = False
        self.ic_computed = False
        if diag_proc_data is not None:
            # FIXME: presently diagram_processing data is passed in
            # as a giant tuple. make this a dataclass ocne type has matured.
            (
                self.t,
                self.x,
                self.x_dot,
                self.y,
                self.X,
                self.eqs,
                self.vars_in_eqs,
                self.eqs_idx,
                self.knowns,
                self.known_vars,
                self.ics,
            ) = diag_proc_data
        else:
            self.t = t
            self.eqs = eqs
            self.knowns = knowns
            self.known_vars = set(knowns.keys())
            self.ics = {} if ics is None else ics
            self.verbose = verbose

            (
                self.x,
                self.x_dot,
                self.y,
                self.X,
                self.vars_in_eqs,
                self.eqs_idx,
            ) = process_equations(self.eqs, self.known_vars)

    def __call__(self):
        self.check_system()
        self.prepare_pantelides_system()
        self.pantelides()
        self.find_free_variables_for_consistent_initialization()
        # self.compute_initial_conditions()
        self.make_BLT_graph()
        self.dummy_derivatives()
        self.index_reduction_done = True

    def check_system(self):
        if self.y is None:
            warnings.warn("No algebraic variables found in the DAE system")
            self.is_ODE = True
        elif self.x is None:
            warnings.warn(
                "No differential variables exist. Consider using an algebraic solver."
            )

        self.n = len(self.x)
        self.m = len(self.y)

        self.N = self.n + self.m  # number of equations
        self.M = 2 * self.n + self.m  # number of variables

        if self.N != len(self.eqs):
            raise ValueError(
                "Mismatch between the number of equations and the number of variables."
            )

        if self.verbose:
            print("##### Input system Information #####", "\n")
            print(f"Total equations: {self.N}")
            print(f"Total variables: {self.M}")
            print(f"Number of differential variables: {self.n}")
            print(f"Number of algebraic variables: {self.m}")
            print("\n")
            for idx, eq in enumerate(self.eqs):
                print(f"Equation {idx}: {eq}")
            print("\n")
            for idx, x in enumerate(self.X):
                print(f"Variable {idx}: {x}")
            print("\n")

    def prepare_pantelides_system(self):
        self.Nprime = self.N
        self.Mprime = self.M

        self.create_bipartite_graph()

        # Create association list
        A = [None] * len(self.X)
        for idx, x in enumerate(self.X):
            if sp.diff(x, self.t) in self.X:
                A[idx] = self.X.index(sp.diff(x, self.t))
        self.A = A

        self.assign = [None] * len(self.X)
        self.B = [None] * self.N

    def create_bipartite_graph(self):
        """
        Create a bipartite graph from the DAE system equations and variables.
        - Equation nodes named by their indices in self.eqs from 0 to N-1.
        - Variable nodes are named by their symbols in self.X. Forward and reverse
          mappings from these names to indices are created.
        """

        self.G = nx.Graph()

        # Add nodes with the bipartite attribute. Equation nodes are bipartite 0, and
        # variable nodes are bipartite 1.
        self.G.add_nodes_from([i for i, _ in enumerate(self.eqs)], bipartite=0)
        self.G.add_nodes_from(self.X, bipartite=1)

        # Add edges based on variable presence in each equation
        for eq_idx, (_, vars_in_eq) in enumerate(self.vars_in_eqs.items()):
            for var in vars_in_eq:
                self.G.add_edge(eq_idx, var)

        self.e_nodes = [n for n, d in self.G.nodes(data=True) if d["bipartite"] == 0]
        self.v_nodes = [n for n, d in self.G.nodes(data=True) if d["bipartite"] == 1]

        # Create a mapping from variable node labels to indices and vice versa
        self.v_mapping = {node: idx for idx, node in enumerate(self.v_nodes)}
        self.reverse_v_mapping = {idx: node for node, idx in self.v_mapping.items()}

        # Graph to keep track of equation differentiations
        self.eq_diff_graph = nx.DiGraph()
        self.eq_diff_graph.add_nodes_from(self.e_nodes)

    def pantelides(self, max_steps=20):
        """
        Algorithm 4.1 of
        Pantelides, C.C., 1988. The consistent initialization of differential-algebraic
        systems. SIAM Journal on scientific and statistical computing, 9(2), pp.213-231.
        """
        # Steps 1 and 2 are performed in `prepare_pantelides_system`
        # Step 3
        for k in range(self.Nprime):
            i = k
            pathfound = False
            counter_steps = 0
            while not pathfound and (counter_steps < max_steps):
                G = self.G.copy()
                delete_var_nodes_with_zero_A(G, self.A, self.X)
                nx.set_node_attributes(G, "white", "color")
                pathfound = False
                pathfound, self.assign = augmentpath(
                    G, i, pathfound, self.assign, self.v_mapping
                )
                colored_e_nodes = [
                    n
                    for n, d in G.nodes(data=True)
                    if d["color"] == "red" and d["bipartite"] == 0
                ]
                colored_v_nodes = [
                    n
                    for n, d in G.nodes(data=True)
                    if d["color"] == "red" and d["bipartite"] == 1
                ]

                if not pathfound:
                    # (i)
                    for v_node in colored_v_nodes:
                        j = self.v_mapping[v_node]
                        self.M = self.M + 1

                        new_diff_var = sp.diff(self.X[j], self.t)
                        new_diff_var_name = str(new_diff_var)
                        self.X.append(new_diff_var)
                        self.G.add_node(new_diff_var_name, bipartite=1)
                        self.A.append(None)
                        self.assign.append(None)

                        self.v_nodes.append(new_diff_var_name)
                        self.v_mapping[new_diff_var_name] = (
                            self.M - 1
                        )  # -1 because of 0-based indexing
                        self.reverse_v_mapping[self.M - 1] = new_diff_var_name

                        self.A[j] = self.M - 1

                    # (ii)
                    for e_node in colored_e_nodes:
                        self.N = self.N + 1

                        new_eq_node = self.N - 1  # -1 because of 0-based indexing
                        self.G.add_node(new_eq_node, bipartite=0)
                        self.B.append(None)
                        self.eqs.append(sp.diff(self.eqs[e_node], self.t))

                        self.e_nodes.append(new_eq_node)

                        self.eq_diff_graph.add_node(self.N - 1)
                        self.eq_diff_graph.add_edge(e_node, self.N - 1)

                        neighbors = self.G.neighbors(e_node)
                        for v_node in neighbors:
                            j = self.v_mapping[v_node]
                            self.G.add_edge(new_eq_node, v_node)
                            if self.A[j] is not None:
                                self.G.add_edge(
                                    new_eq_node, self.reverse_v_mapping[self.A[j]]
                                )

                        self.B[e_node] = self.N - 1

                    # (iii)
                    for v_node in colored_v_nodes:
                        j = self.v_mapping[v_node]
                        self.assign[self.A[j]] = self.B[self.assign[j]]

                    # (iv)
                    i = self.B[i]
                counter_steps += 1

        # Variable to equation matching: index in self.X -> index in self.eqs
        self.matching = {}
        self.reverse_matching = {}

        for idx_var, idx_eq in enumerate(self.assign):
            if idx_eq is not None:
                self.matching[idx_var] = idx_eq
                self.reverse_matching[idx_eq] = idx_var

        self.pantelides_dae_eqs = [
            eq_idx
            for eq_idx in self.eq_diff_graph.nodes()
            if self.eq_diff_graph.out_degree(eq_idx) == 0
        ]

        self.pantelides_dae_vars = [
            self.reverse_matching[eq_idx] for eq_idx in self.pantelides_dae_eqs
        ]

        self.pantelides_dae_reverse_matching = {
            eq_idx: self.reverse_matching[eq_idx] for eq_idx in self.pantelides_dae_eqs
        }

        if self.verbose:
            assignment_dict = dict(
                zip(self.X, [i if i is not None else "" for i in self.assign])
            )
            eq_differentiation_dict = dict(
                zip(
                    [i if i is not None else "" for i in range(len(self.B))],
                    [i if i is not None else "" for i in self.B],
                )
            )

            derivative_mapping_dict = {
                self.X[base]: self.X[derivative]
                for base, derivative in enumerate(self.A)
                if derivative is not None
            }

            print("##### Panteides Algorithm Completed #####", "\n")

            print(f"Total equations (before|after): {self.Nprime}|{self.N}")
            print(f"Total variables (before|after): {self.Mprime}|{self.M}")

            print("\n")
            print("# Variables", "\n")
            for idx, var in enumerate(self.X):
                print(f"Variable {idx}: {var}")
            print("\n")
            print("# Equations", "\n")
            for idx, eq in enumerate(self.eqs):
                print(f"Equation {idx}: {eq}")

            print("\n")
            print("# Variable assignments")
            for k, v in assignment_dict.items():
                print(f"Variable {k} is assigned to -> e{v}")

            print("\n")
            print("# Differentiated equations")
            for k, v in eq_differentiation_dict.items():
                print(f"Differentiate e{k} to get  -> e{v}")

            print("\n")
            print("# Derivatives present in the variable association list")
            for k, v in derivative_mapping_dict.items():
                print(f"Present derivative of {k} is  -> {v}")

            print("\n")
            print("##### Index-1 (atmost) system after Pantelides #####", "\n")

            print("# Equations in the index-1 DAE system", "\n")
            for eq_idx in self.pantelides_dae_eqs:
                print(f"Equation {eq_idx}: {self.eqs[eq_idx]}")

            print("\n")
            print("Variables in the index-1 DAE system", "\n")
            for var_idx in self.pantelides_dae_vars:
                print(f"Variable {var_idx}: {self.X[var_idx]}")

    def find_free_variables_for_consistent_initialization(self):
        """
        Find the variables that can be freely chosen for consistent initialization
        of the system produced by the Pantelides algorithm.
        """
        # Determine if system is over/under-determined
        if self.N > self.M:
            raise ValueError("The system of equations is over-determined. Aborting!")
        elif self.N == self.M:
            print(
                "\n"
                f"Structural analysis: {self.M} equations in {self.N} variables. "
                "No variables can be freely chosen for consistent initialization."
            )
            self.X_free_idx = []
            self.X_free = []
            return
        else:
            self.num_fake_equations = self.M - self.N

        # Create a new graph with the fake equations
        G = self.G.copy()
        e_nodes = self.e_nodes.copy()

        for i in range(self.num_fake_equations):
            new_eq_node = self.N + i
            G.add_node(new_eq_node, bipartite=0)
            e_nodes.append(new_eq_node)

            for v_node in self.v_nodes:
                G.add_edge(new_eq_node, v_node)

        # Find maximum matching
        _mm = bipartite.matching.maximum_matching(G, top_nodes=self.v_nodes)
        mm = {k: v for k, v in _mm.items() if k in e_nodes}

        if len(mm) != len(self.X):
            raise ValueError(
                "The system of equations for initial conditions obtained after "
                "Pantelides algorithm is not solvable. A complete matching could not "
                "be found."
            )
        # Variable to equation matching
        max_matching = {}
        # Equation to variable matching
        reverse_max_matching = {}

        for eq, var in mm.items():
            max_matching[self.v_mapping[var]] = eq
            reverse_max_matching[eq] = self.v_mapping[var]

        D = nx.DiGraph()
        D.add_nodes_from(reverse_max_matching.keys())

        for eq_parent, idx_matched_var in reverse_max_matching.items():
            eq_neighbors_of_matched_var = list(
                G.neighbors(self.reverse_v_mapping[idx_matched_var])
            )
            for eq_child in eq_neighbors_of_matched_var:
                if eq_child != eq_parent:
                    D.add_edge(eq_parent, eq_child)

        scc = [list(x) for x in nx.strongly_connected_components(D)]

        # Construct new graph with SCCs as nodes
        scc_graph = nx.DiGraph()
        scc_map = {}  # Map each node to its SCC
        for idx, component in enumerate(scc):
            scc_graph.add_node(idx)
            for node in component:
                scc_map[node] = idx

        # Add edges between SCCs in the new graph
        for u, v in D.edges():
            if scc_map[u] != scc_map[v]:
                scc_graph.add_edge(scc_map[u], scc_map[v])

        # Sort the SCCs in topological order
        topological_sorted_scc = list(nx.topological_sort(scc_graph))

        # Convert back to the actual nodes in the original graph
        eBLT = [scc[idx] for idx in topological_sorted_scc]

        last_block = eBLT[-1]

        self.X_free_idx = [reverse_max_matching[eq_idx] for eq_idx in last_block]
        self.X_free = [self.X[idx] for idx in self.X_free_idx]
        self.num_free_vars = len(self.X_free)
        if self.verbose:
            print("##### Structural analysis for consistent initialization #####", "\n")
            print("# Blocks Triangular equations")
            print(f"{eBLT=}", "\n")
            print(
                f"Structural analysis: any {self.M-self.N} variables from the following "
                f"{len(self.X_free)} variables can be freely chosen for consistent "
                f"initialization of {self.M} equations:",
                "\n",
            )
            for idx, x in enumerate(self.X_free):
                print(f"Variable {idx}: {x}")

    def compute_initial_conditions(self):
        """
        Compute the initial conditions for the system of equations obtained after the
        Pantelides algorithm.
        """
        if len(self.ics) != self.M - self.N:
            raise ValueError(
                "Insufficient initial conditions for consistent initialization. "
                f"{self.M-self.N} conditions are required but only {len(self.ics)} are "
                f"provided. "
                f"Please provide initial values for any {self.M-self.N} variables from "
                f"the following {len(self.X_free)} variables: {self.X_free}"
            )

        # Check that the provided initial conditions are amongst the variables
        # found by structural analysis
        if any(ic_var not in self.X_free for ic_var in self.ics.keys()):
            raise ValueError(
                "Initial conditions should be provided for the variables found by "
                "prelimary structural analysis."
                f"Please provide initial values for any {self.M-self.N} variables from "
                f"the following {len(self.X_free)} variables: {self.X_free}"
            )

        if not is_structurally_feasible(self.ics, self.G):
            raise ValueError(
                "The initial conditions provided are not structurally feasible. "
                f"Provided initial conditions were for variables: {self.ics.keys()}. "
                f"Provide a different combination of initial values for any "
                f"{self.M-self.N} variables from "
                f"the following {len(self.X_free)} variables: {self.X_free}"
            )

        if self.verbose:
            print(
                "\n"
                "Initial condition computation is structurally feasible. "
                "Proceeding with numerical computation.",
            )

        self.X_ic = compute_consistent_initial_conditions(
            self.eqs, self.X, self.ics, self.knowns
        )

        self.X_ic_mapping = {var: ic for var, ic in zip(self.X, self.X_ic)}

        self.ic_computed = True

        if self.verbose:
            print("\n")
            print("##### Initial conditions #####", "\n")
            for var, var_ic in self.X_ic_mapping.items():
                print(f"{var} = {var_ic}")

    def make_BLT_graph(self):
        """
        For the atmost index-1 system produced by Pantelides algorith, create a
        Block lower triangular (BLT) ordering. The BLT ordering is a topological
        ordering of the strongly connected components (SCCs) of the directed graph.
        """

        # Create an equation dependency (in terms of matched variables) graph D
        D = nx.DiGraph()
        D.add_nodes_from(self.pantelides_dae_reverse_matching.keys())

        for eq_parent, idx_matched_var in self.pantelides_dae_reverse_matching.items():
            eq_neighbors_of_matched_var = list(
                self.G.neighbors(self.reverse_v_mapping[idx_matched_var])
            )
            for eq_child in eq_neighbors_of_matched_var:
                if eq_child != eq_parent:
                    D.add_edge(eq_parent, eq_child)

        scc = [list(x) for x in nx.strongly_connected_components(D)]

        # Construct new graph with SCCs as nodes
        scc_graph = nx.DiGraph()
        scc_map = {}  # Map each node to its SCC
        for idx, component in enumerate(scc):
            scc_graph.add_node(idx)
            for node in component:
                scc_map[node] = idx

        # Add edges between SCCs in the new graph
        for u, v in D.edges():
            if scc_map[u] != scc_map[v]:
                scc_graph.add_edge(scc_map[u], scc_map[v])

        # Sort the SCCs in topological order
        topological_sorted_scc = list(nx.topological_sort(scc_graph))

        # Convert back to the actual nodes in the original graph
        self.eBLT = [scc[idx] for idx in topological_sorted_scc]

        if self.verbose:
            print("##### Block Lower Triangular (BLT) ordering #####", "\n")

            print("BLT equation ordering")
            print([[f"e{idx}" for idx in block] for block in self.eBLT])

            print("BLT variable ordering")
            print(
                [
                    [self.X[self.pantelides_dae_reverse_matching[idx]] for idx in block]
                    for block in self.eBLT
                ]
            )

    def dummy_derivatives(self):
        """
        Algorithm in Section 3.1 of
        Mattsson, S.E. and Söderlind, G., 1993. Index reduction in
        differential-algebraic equations using dummy derivatives.
        SIAM Journal on Scientific Computing, 14(3), pp.677-692.
        """
        BLT_eq_blocks = self.eBLT

        self.dummy_vars = {}
        self.final_dae_eqs_pre_replacement = []
        self.replace = {}

        for unsorted_eq_block in BLT_eq_blocks:
            # Step 1
            num_parents, eq_block = sort_block_by_number_of_eq_derivatives(
                self.eq_diff_graph, unsorted_eq_block
            )
            vars_block = [
                self.pantelides_dae_reverse_matching[eq_idx] for eq_idx in eq_block
            ]

            g = sp.Matrix([self.eqs[eq_idx] for eq_idx in eq_block])
            z = sp.Matrix([self.X[var_idx] for var_idx in vars_block])
            G = g.jacobian(z)

            block_replace = {}
            sub_blocks = [eq_block]
            while True:
                # Step 2
                if sum(num_parents) == 0:
                    # Go to Step 6
                    break
                else:
                    # Step 3
                    m = sum([1 for n in num_parents if n != 0])

                    H = G[:m, :]

                    # Step 4
                    _, pivot_columns = H.rref()

                    # Step 5
                    M = H[:, pivot_columns]

                    for replacing_eq, replacing_var in zip(
                        eq_block[:m], [vars_block[idx] for idx in pivot_columns]
                    ):
                        block_replace[replacing_eq] = replacing_var

                    G = M
                    eq_block = [
                        list(self.eq_diff_graph.predecessors(eq_idx))[0]
                        for eq_idx in eq_block[:m]
                    ]
                    vars_block = [
                        self.A.index(vars_block[idx]) for idx in pivot_columns
                    ]

                    num_parents = [n - 1 for n in num_parents[:m]]

                    sub_blocks.append(eq_block)

            # Step 6

            final_block_eqs = []
            if block_replace:
                # Create dummy variables
                block_dummy_vars = {}
                for eq_idx, var_idx in block_replace.items():
                    dummy_var = sp.Symbol("d_" + str(self.X[var_idx]))
                    block_dummy_vars[self.X[var_idx]] = dummy_var
            else:
                block_dummy_vars = {}

            # Gather equations in reverse block order
            for sub_block in reversed(sub_blocks):
                for eq_idx in sub_block:
                    final_block_eqs.append(self.eqs[eq_idx])

            self.final_dae_eqs_pre_replacement.extend(final_block_eqs)
            self.dummy_vars.update(block_dummy_vars)
            self.replace.update(block_replace)

        # Replace true variables with dummy variables
        self.final_dae_eqs = []
        for eq in self.final_dae_eqs_pre_replacement:
            replaced_eq = eq.subs(self.dummy_vars)
            self.final_dae_eqs.append(replaced_eq)

        Xset = set(self.X)
        Dset = set(self.dummy_vars.keys())  # dummy vars are algebraic
        Vset = Xset - Dset

        self.final_dae_x, self.final_dae_y = set(), set()

        for var in Vset:
            if isinstance(var, sp.Derivative):
                self.final_dae_x.add(var.expr)
            else:
                self.final_dae_y.add(var)

        self.final_dae_y = self.final_dae_y.difference(self.final_dae_x)
        self.final_dae_y = self.final_dae_y.union(
            {self.dummy_vars[var] for var in Dset}
        )

        self.final_dae_x = list(self.final_dae_x)
        self.final_dae_y = list(self.final_dae_y)

        self.final_dae_x_dot = [var.diff(self.t) for var in self.final_dae_x]
        self.final_dae_X = list(
            set().union(self.final_dae_x, self.final_dae_x_dot, self.final_dae_y)
        )

        self.X_to_dae_X_mapping = {}
        for var in self.X:
            if var in self.dummy_vars:
                self.X_to_dae_X_mapping[var] = self.dummy_vars[var]
            else:
                self.X_to_dae_X_mapping[var] = var

        self.dae_X_to_X_mapping = {v: k for k, v in self.X_to_dae_X_mapping.items()}

        if self.ic_computed:
            self.final_dae_x_ic = [
                self.X_ic_mapping[self.dae_X_to_X_mapping[var]]
                for var in self.final_dae_x
            ]
            self.final_dae_x_dot_ic = [
                self.X_ic_mapping[self.dae_X_to_X_mapping[var]]
                for var in self.final_dae_x_dot
            ]
            self.final_dae_y_ic = [
                self.X_ic_mapping[self.dae_X_to_X_mapping[var]]
                for var in self.final_dae_y
            ]

        if self.verbose:
            print("\n")
            print("#" * 10, "Dummy Derivatives computed succesfully", "#" * 10, "\n")
            print("#" * 10, "Final DAE equations F(x, x_dot, y)=0", "#" * 12, "\n")
            for idx, eq in enumerate(self.final_dae_eqs):
                print(f"Eq {idx:<4}:  ", eq)

            print("\n# with, x =\n")
            for var, ic in zip(self.final_dae_x, self.final_dae_x_ic):
                print(f"{str(var):30} with ic= {ic}")

            print("\n# x_dot =\n")
            for var, ic in zip(self.final_dae_x_dot, self.final_dae_x_dot_ic):
                print(f"{str(var):30} with ic= {ic}")

            print("\n# and, y =\n")
            for var, ic in zip(self.final_dae_y, self.final_dae_y_ic):
                print(f"{str(var):30} with ic= {ic}")

            print("\n", "#" * 60, "\n")
