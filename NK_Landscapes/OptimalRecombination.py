"""
Based on the paper:
Chicano, F., Ochoa, G., Whitley, D. and Tinós, R. (2019) ‘Quasi-Optimal Recombination Operator’, Lecture Notes in Computer Science.Springer International Publishing, pp. 131–146.
doi: 10.1007/978-3-030-16711-0_9.
The implementation is done assuming minimization instead of maximization, as in the paper.
"""

from Graph import Graph
import numpy as np
from CliqueConfiguration import *

from PX import * # PX class defined according with the problem

sf = None # list of tuples

# get a binary array from an integer b with n_bits representation
def getBinaryArray(b, n_bits):
    if n_bits == 0:
        return []
    return [int(i) for i in np.binary_repr(b, n_bits)]

# convert a binary array to the corresponding int
def binArrayToInt(bin_array):
    val = 0
    for b in bin_array:
        val = (val << 1) | b
    return val

# returns the recombination graph
def createRecombinationGraph(sub_funcs):
    rec_graph = Graph()

    for sf in sub_funcs:
        f_len = len(sf)
        if(f_len > 1):

            for i in range(f_len-1):
                for j in range(i+1, f_len):
                    rec_graph.add_edge(sf[i], sf[j])
        else:
            rec_graph.add_node(sf[0]) # assumindo que é um tuplo com apenas um elemento

    return rec_graph

# given a configuration for all the variables in the parent (separator + residue), return the configuration for the corresponding separator variables in the child, as a binary array
def getChildConfigFromParent(child_separator, total_vars, total_decisions):

    bin_array = np.zeros(len(child_separator), dtype="int")

    for v in range(len(total_vars)):
        if total_vars[v] in child_separator:
            bin_array[child_separator.index(total_vars[v])] = total_decisions[v]

    return bin_array

# Gets the decisions for each variable
# This function merges the decisions for the separator with the decisions for the residue
def getFullDecision(separator, x_s, residue, x_r):

    # concatenate variables of separator and
    variables = [s for s in separator]
    for r in residue:
        variables.append(r)

    bin_x_s = getBinaryArray(x_s, len(separator))
    bin_x_r = getBinaryArray(x_r, len(residue))

    decisions = [s for s in bin_x_s]
    for r in bin_x_r:
        decisions.append(r)

    return variables, decisions

# perform bfs on the clique tree to get the optimal choices
def bfsOptimalOffspring(clique, cliques, cliqueExplored, cliqueTree, cliqueConfigs, off_variables, off_decisions, off_value):
    # the argument 'clique' corresponds to the root
    id = cliqueTree.nodes[clique]['id']
    parent_separator = cliqueConfigs[id].getSeparator()
    parent_residue = cliqueConfigs[id].getResidue()
    x_s = 0

    """
    Get the residue combination of the separator combination.
    The parent node does not have variables in the separator.
    """
    x_r = cliqueConfigs[id].getVariables(x_s)

    # The objective value for (empty) separator config. x_s with config. x_r.
    off_value += cliqueConfigs[id].getValue(x_s)

    # Remember: off_variables and off_decisions are returned in the arguments
    off_variables.extend(parent_residue) # add the residue's variable
    off_decisions.extend(getBinaryArray(x_r, len(parent_residue))) # add the corresponding decisions for each variable

    # merge the variables in the separator and residue for <this> clique, as well as the corresponding decisions
    # Maybe we don't need to use this function at this stage.
    parent_vars, parent_decisions = getFullDecision(parent_separator, x_s, parent_residue, x_r)

    cliqueExplored[id] = True

    queue = [(clique, parent_vars, parent_decisions)]

    while(len(queue)>0):
        clique, parent_vars, parent_decisions = queue.pop(0)

        # go through all of this clique's neighbours, in the clique tree
        for c in list(cliqueTree.neighbors(clique)):
            id = cliqueTree.nodes[c]['id']
            if(not cliqueExplored[id]):
                separator = cliqueConfigs[id].getSeparator()
                residue = cliqueConfigs[id].getResidue()

                # get the choices for this clique's separator variables according to the choices for these same variables in the parent (separator + residue)
                # Note: The separator's variables are the ones both parent and child have in common
                bin_arr_x_s = getChildConfigFromParent(separator, parent_vars, parent_decisions)


                x_s = binArrayToInt(bin_arr_x_s)
                x_r = cliqueConfigs[id].getVariables(x_s) # get the combination in the residue given the combination in the separator (called getVariables because in the paper the array that stores the choices is called 'variable')

                bin_arr_x_r = getBinaryArray(x_r, len(residue))

                # add the variables and corresponding decisions to the lists to be returned
                off_variables.extend(residue)
                off_decisions.extend(bin_arr_x_r)


                total_vars, total_decisions = getFullDecision(separator, x_s, residue, x_r)

                queue.append((c, total_vars, total_decisions))


                cliqueExplored[id] = True

    return off_value
"""
This function returns the full decisions, for all variables.
It begins by selection the best (and only) combination for the variable in the root of the tree and traverses the clique tree in the reverse post-order

"""
def getCompleteDecisions(cliques, cliqueConfigs, cliqueTree):
    # cliques are ordered in post-order, so we begin from the end, which corresponds to the root of the tree
    off_decisions = []
    off_variables = [] # we want to know the order in which the variables were considered
    off_value = 0
    cliqueExplored = [False]*len(cliques)
    cliques.reverse() # cliques has the cliques ordered in post-order. Now we want to do the inverse of that to start from the root

    for i in range(len(cliques)): # Note: maybe we do not need a for cycle
        c = cliques[i]
        id = cliqueTree.nodes[c]['id']
        if(not cliqueExplored[id]):
            off_value = bfsOptimalOffspring(c, cliques, cliqueExplored, cliqueTree, cliqueConfigs, off_variables, off_decisions, off_value)

    return off_decisions, off_variables, off_value


# get the objective value for the sub-functions (tuples) in the clique, given the choices for its variables
# 'total_vars' have the clique's separator and residue variables; 'total_decisions' have the corresponding decisions, where the value in each position corresponds to the variable in the same position in 'total_vars'.
def getPartialObjectiveValue(rec_graph, clique, total_vars, total_decisions):
    aux = 0
    sub_funcs = rec_graph.getCliqueSubFunctions(clique) # get the sub-functions assigned to this clique

    # In decisions_aux, the index corresponds to the variable and the value is the decision
    decisions_aux = [-1]*(rec_graph.getMaxNodeValue()+1) # TO_IMPROVE

    for i in range(len(total_vars)):
        decisions_aux[total_vars[i]] = total_decisions[i]


    # call the 'evaluate' function, defined in the PX class for each sub-function
    for sf_ix in sub_funcs:
        t = tuple([decisions_aux[i] for i in sf[sf_ix]]) # create the tuple for sub-function sf_ix
        aux += px.evaluate(sf_ix, t)

    return aux

"""
Get the objective value of all the clique's children (already evaluated)
"""
def getCliqueChildrenEvaluation(aux, total_vars, total_decisions, clique, rec_graph, evaluatedCliques, cliqueConfigs):
    aux = 0
    cliqueTree = rec_graph.getCliqueTree()

    # since we traverse the clique tree in post-order, if a clique's neighbour is not evaluated, then it is not a children of the clique
    children = [c for c in list(cliqueTree.neighbors(clique)) if evaluatedCliques[cliqueTree.nodes[c]['id']] == True]

    for c in children:
        id = cliqueTree.nodes[c]['id']

        child_separator = cliqueConfigs[id].getSeparator()

        # get the choices for this clique's separator variables according to the choices for these same variables in the parent (separator + residue)
        # Note: The separator's variables are the ones both parent and child have in common
        bin_array = getChildConfigFromParent(child_separator, total_vars, total_decisions)

        x_c = binArrayToInt(bin_array)

        aux += cliqueConfigs[id].getValue(x_c) # get the best value for the x_c choices of the separator

    return aux


# the dynamic programming algorithm that decides how the offspring should be constructed

def doOptimalRecombination(rec_graph):

    cliques = rec_graph.getCliqueTreePostOrder() # get the cliques in the clique tree in post-order
    clique_tree = rec_graph.getCliqueTree() # get the clique tree
    evaluatedCliques = [False]*len(cliques)

    # List of instances of the CliqueConfiguration class. One for each clique.
    cliqueConfigs = [[]]*len(cliques)

    # create instances of the CliqueConfiguration class for each clique and initialize 'evaluatedCliques'
    for c in cliques:
        id = clique_tree.nodes[c]["id"]
        evaluatedCliques[id] = False # clique was not evaluated
        separator = rec_graph.getCliqueSeparator(c)
        residue = rec_graph.getCliqueResidue(c)
        cliqueConfigs[id] = CliqueConfiguration(id, id, c, separator, residue)

    # the cliques list has the cliques in post-order
    for clique in cliques:
        clique_id =clique_tree.nodes[clique]["id"]

        separator = rec_graph.getCliqueSeparator(clique)
        residue = rec_graph.getCliqueResidue(clique)

        sep_len = len(separator)
        res_len = len(residue)

        for x_s in range((2**sep_len)): # test all combinations of values for the variables in this clique's separator

            for x_r in range((2**res_len)): # test all combinations of values for the variables in this clique's residue

                # merge the variables, and corresponding decisions, in the separator and residue, for evaluation
                total_vars, total_decisions = getFullDecision(separator, x_s, residue, x_r)

                # get the objective value for this combination of choices in the separator and residue
                aux = getPartialObjectiveValue(rec_graph, clique, total_vars, total_decisions)

                aux += getCliqueChildrenEvaluation(aux, total_vars, total_decisions, clique, rec_graph, evaluatedCliques, cliqueConfigs)

                if aux < cliqueConfigs[clique_id].getValue(x_s): # we are minimizing, instead
                    cliqueConfigs[clique_id].setValue(x_s, aux)
                    cliqueConfigs[clique_id].setVariables(x_s, x_r)

        evaluatedCliques[clique_id] = True # set this clique as evaluated


    # get the final decisions for each variable (component)
    off_decisions, off_variables, off_value = getCompleteDecisions(cliques, cliqueConfigs, clique_tree)


    # sort the decisions so that they are arranged in increasing order according to the associated component (variable).
    # In t, each position represents a component and its value is the associated parent choice.
    t = [-1]*len(off_variables)
    for i in range(len(off_variables)):
        t[off_variables[i]] = off_decisions[i]

    return tuple(t) # return in tuple form


def parentsAreEqual(p1, p2):
    for i in range(len(p1)):
        if(p1[i] != p2[i]):
            return False

    return True


def recombine(p1, p2):
    global sf
    global px

    # if both parents are equal, just return one of the parents
    if(parentsAreEqual(p1, p2)):
        return p1

    # instanciate the classe PX, defined according with the problem
    px = PX(p1, p2)

    # get the sub-functions resulted from the union of the parents in PX
    sf = px.subfunctions()

    # creates the recombination graph, the clique tree, and everything needed in between
    rec_graph = createRecombinationGraph(sf)

    # assign the sub-functions to the clique tree created from the recombination graph
    rec_graph.assignSubFuncs(sf)

    # perform the optimal recombination
    t = doOptimalRecombination(rec_graph)
    return px.offspring(t) # return the offspring according with the choices in t
