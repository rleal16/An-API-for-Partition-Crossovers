import networkx as nx
import nx_junction_tree as nxjt
import matplotlib.pyplot as plt

class Graph:

    def __init__(self):

        self.graph = nx.Graph() # the recombination graph

        self.clique_tree = None
        self.cliques = None # the nodes of the clique tree
        self.chordal_graph = None
        self.alpha = None # the alpha array that resulted from the maximum cardinality search
        self.alpha_inv = None # the inverse of the alpha array that resulted from the maximum cardinality search
        self.cliqueTreePostOrder = None # nodes of the clique tree ordered in postorder

        # the node with the highest id
        self.max_node_value = -1


    def add_edge(self, u, v):
        # by default parallel edges are not allowed
        if(u > self.max_node_value):
            self.max_node_value = u
        if(v > self.max_node_value):
            self.max_node_value = v

        self.graph.add_edge(u, v)

    def add_node(self, v):
        if(v > self.max_node_value):
            self.max_node_value = v
        self.graph.add_node(v)

    # assign sub-functions to the cliques
    def assignSubFuncs(self, sub_funcs):
        if(self.clique_tree == None):
            _ = self.getCliqueTree() # we do everything at once

        self.getCliqueTreePostOrder()
        sf_ix = 0 # subfunction index

        while(sf_ix < len(sub_funcs)):

            # assign sub-functions to the clique tree's nodes in post-order
            for node in self.cliqueTreePostOrder:
                sf = sub_funcs[sf_ix]
                add_sf = True
                for v in sf:
                    if v not in node: # if true, sf cannot be assigned to this node
                        add_sf = False
                        break

                # add sub-function if all of its variables are in the clique
                if add_sf:
                    self.clique_tree.nodes[node]['sub_funcs'].append(sf_ix)
                    sf_ix+=1
                    break

    # get the sub-functions assigned to a given clique
    def getCliqueSubFunctions(self, clique):
        return self.clique_tree.nodes[clique]['sub_funcs']

    def getVerticesList(self):
        return list(self.graph.nodes)

    def hasEdge(self, u, v):
        return self.graph.has_edge(u, v)

    def getMaxNodeValue(self):
        return self.max_node_value

    # Returns the clique tree. Creates one, if non-existent.
    def getCliqueTree(self):
        if(self.clique_tree == None):
            self.clique_tree, self.cliques, self.chordal_graph, self.alpha = nxjt.junction_tree(self.graph)
        self.alpha_inv = {}
        for k, v in self.alpha.items():
            self.alpha_inv[v] = k
        return self.clique_tree


    def getAlpha(self):
        if(self.alpha == None):
            _ = self.getCliqueTree()
        return self.alpha

    def getAlphaInv(self):
        if(self.alpha == None):
            _ = self.getCliqueTree()
        return self.alpha_inv

    # get the nodes (cliques) of the clique tree
    def getCliques(self):
        if(self.cliques == None):
            _ = self.getCliqueTree()
        return self.cliques

    # get the separator of a given clique
    def getCliqueSeparator(self, clique):
        if(self.clique_tree == None):
            _ = self.getCliqueTree()
        return self.cliques[clique]["sepset"]

    # get the separator of a given clique
    def getCliqueResidue(self, clique):
        if(self.clique_tree == None):
            _ = self.getCliqueTree()
        return self.cliques[clique]["resset"]

    def getCliqueTreePostOrder(self):
        if(self.clique_tree == None):
            _ = self.getCliqueTree()
        self.cliqueTreePostOrder = list(nx.dfs_postorder_nodes(self.clique_tree))
        return self.cliqueTreePostOrder

    def getCliqueTreeBFS(self):
        if(self.clique_tree == None):
            _ = self.getCliqueTree()
        return list(nx.bfs_edges(self.clique_tree))

    # draw the recombination graph
    def print_graph(self):
        nx.draw_networkx(self.graph, pos=nx.spring_layout(self.graph), with_labels=True, node_size=1000, connectionstyle='arc3, rad = 0.4', label="Recombination Graph")
        plt.show()

    # print the clique tree
    def print_clique_tree(self):
        if(self.clique_tree == None):
            self.getCliqueTree()

        plt.figure(1, figsize=(15, 30))
        nx.draw_networkx(self.clique_tree, pos=nx.planar_layout(self.clique_tree), with_labels = True, node_size = 5000, connectionstyle='arc3, rad = 0.1', arrowsize=20, label="Clique Tree")
        plt.show()

    # print the chordal graph
    def print_chordal_graph(self):
        if(self.chordal_graph == None):
            _ = self.getCliqueTree()

        nx.draw_networkx(self.chordal_graph, with_labels = True, node_size = 500, connectionstyle='arc3, rad = 0.1', label="Chordal Graph")
        plt.show()
