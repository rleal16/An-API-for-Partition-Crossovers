"""
Searches for all possible offspring that could result from the recombination of two parents, and returns the set of offsprings with the optimal objective value.
Used for testing.
"""

import instance
import numpy as np


def getBinaryArray(b, n_bits):
    if n_bits == 0:
        return []
    return [int(i) for i in np.binary_repr(b, n_bits)]

def binArrayToInt(bin_array):
    val = 0
    for b in bin_array:
        val = (val << 1) | b
    return val

# create an offspring with the choices for diffVars (variables with different values in the parents) and adding the values of the variables with the same value in both parents, from one of the parents.
def createAnOffspring(p, diffVars, choices):
    off = [i for i in p]
    for i, ch in zip(diffVars, choices):
        off[i] = ch
    return off

# Create a set of offsprings given a set of partial solutions (choices for the variables where the exhaustive search was made)
def createAllOffsprings(p, diffVars, partial_sols):
    offs = []
    for choices in partial_sols:
        off = [i for i in p]
        for i, ch in zip(diffVars, choices):
            off[i] = ch
        offs.append(off)

    return offs

def getObjectiveValue(p, diffVars, choices):
    off = createAnOffspring(p, diffVars, choices) # create the offspring by add

    inst = instance.instance
    sfs = inst.getSubFunctions()
    obj = 0
    for s in range(len(sfs)):
        sf = sfs[s]
        t = tuple([off[i] for i in sf])
        obj += inst.getSFObjectiveValue(s, t)
    return abs(obj)


# Identifies variables with different values in both parents. The exhaustive search will be made in these variables.
def findDiffVars(p1, p2):
    diffVars = []
    for i, (v1, v2) in enumerate(zip(p1, p2)):
        if(v1 != v2):
            diffVars.append(i)

    return diffVars

def doExhaustiveRecombination(p1, p2):
    nk_inst = instance.instance

    bestSols = []
    bestVal = -1

    # Identify variables with different values in both parents
    diffVars = findDiffVars(p1, p2)
    n = len(diffVars)

    # perform exhaustive search in diffVars
    for i in range((2**n)):
        sol = getBinaryArray(i, n) # transform i into a binary array
        objVal = getObjectiveValue(p1, diffVars, sol) # get the objective value of the full solution

        if(objVal > bestVal):
            bestVal = objVal
            bestSols = [sol]
        elif(objVal == bestVal):
            bestSols.append(sol) # add to the list of best solutions (so far)

    return createAllOffsprings(p1, diffVars, bestSols) # create a return all the offspring, for all the choices in bestSols
