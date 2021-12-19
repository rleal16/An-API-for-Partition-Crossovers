
"""
Source: https://networkx.org/documentation/stable/_modules/networkx/algorithms/tree/decomposition.html#junction_tree
Changes:
    - Added to each node of the clique tree the atributes to store the separator, residue, sub-functions, and id
    - Create the separator and residue sets for each node of the clique tree
    - Additionally, return the cliques (with data), the chordal graph, and the alpha
"""
r"""Function for computing a junction tree of a graph."""

import networkx as nx
from networkx.utils import not_implemented_for
from networkx.algorithms import moral, complete_to_chordal_graph, chordal_graph_cliques
from itertools import combinations

__all__ = ["junction_tree"]


@not_implemented_for("multigraph", "MultiDiGraph")
def junction_tree(G):
    r"""Returns a junction tree of a given graph.

    A junction tree (or clique tree) is constructed from a (un)directed graph G.
    The tree is constructed based on a moralized and triangulated version of G.
    The tree's nodes consist of maximal cliques and sepsets of the revised graph.
    The sepset of two cliques is the intersection of the nodes of these cliques,
    e.g. the sepset of (A,B,C) and (A,C,E,F) is (A,C). These nodes are often called
    "variables" in this literature. The tree is bipartitie with each sepset
    connected to its two cliques.

    Junction Trees are not unique as the order of clique consideration determines
    which sepsets are included.

    The junction tree algorithm consists of five steps [1]_:

    1. Moralize the graph
    2. Triangulate the graph
    3. Find maximal cliques
    4. Build the tree from cliques, connecting cliques with shared
       nodes, set edge-weight to number of shared variables
    5. Find maximum spanning tree


    Parameters
    ----------
    G : networkx.Graph
        Directed or undirected graph.

    Returns
    -------
    junction_tree : networkx.Graph
        The corresponding junction tree of `G`.

    Raises
    ------
    NetworkXNotImplemented
        Raised if `G` is an instance of `MultiGraph` or `MultiDiGraph`.

    References
    ----------
    .. [1] Junction tree algorithm:
       https://en.wikipedia.org/wiki/Junction_tree_algorithm

    .. [2] Finn V. Jensen and Frank Jensen. 1994. Optimal
       junction trees. In Proceedings of the Tenth international
       conference on Uncertainty in artificial intelligence (UAI’94).
       Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 360–366.
    """

    clique_graph = nx.Graph()

    if G.is_directed():
        G = moral.moral_graph(G)
    chordal_graph, alpha = complete_to_chordal_graph(G)

    # Change: sort elements in the tuple by MCS order
    cliques = [tuple(sorted(i, key=lambda x: alpha[x])) for i in chordal_graph_cliques(chordal_graph)]
    cliques.sort(key=len, reverse=True)


    clique_graph.add_nodes_from(cliques, type="clique")

    for edge in combinations(cliques, 2):
        set_edge_0 = set(edge[0])
        set_edge_1 = set(edge[1])
        if not set_edge_0.isdisjoint(set_edge_1):
            sepset = tuple(sorted(set_edge_0.intersection(set_edge_1)))
            clique_graph.add_edge(edge[0], edge[1], weight=len(sepset), sepset=sepset)

    junction_tree = nx.maximum_spanning_tree(clique_graph)

    """
    Changes
    """
    d_junction_tree = nx.dfs_tree(junction_tree)

    nx.set_node_attributes(junction_tree, [], 'sepset')
    nx.set_node_attributes(junction_tree, [], 'resset')
    nx.set_node_attributes(junction_tree, 0, 'sub_funcs')
    nx.set_node_attributes(junction_tree, -1, 'id')
    clique_id = 0
    for node in d_junction_tree.nodes:
        junction_tree.nodes[node]['id'] = clique_id
        clique_id+=1
        for p in list(d_junction_tree.predecessors(node)):
            junction_tree.nodes[node]['sepset'] = list(junction_tree[node][p]['sepset'])
        junction_tree.nodes[node]['resset'] = [d for d in node if d not in junction_tree.nodes[node]['sepset']]
        junction_tree.nodes[node]['sub_funcs'] = []

    tree_cliques = junction_tree.nodes(data=True)

    
    return junction_tree, tree_cliques, chordal_graph, alpha
