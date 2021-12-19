"""
Given an instance file in the format of the instances in https://maxsat-evaluations.github.io, this code performs the recombination of two randomly generated parents
"""

import numpy as np
import sys
import instance
import random as rnd
import MAXSAT
from OptimalRecombination import recombine

def evaluateOffpsring(off):

    inst = instance.instance
    sfs = inst.getSubFunctions()
    obj = 0
    for s in range(len(sfs)):
        sf = sfs[s]
        t = tuple([off[i] for i in sf])
        obj += inst.evaluate(s, t)
    return abs(obj)


if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Usage: {0} <instance>".format(sys.argv[0]))
        exit(0)

    instance.init(sys.argv[1])
    inst = instance.instance
    n = inst.getNumberOfVariables()

    p1 = np.random.randint(2, size=n)
    p2 = np.random.randint(2, size=n)
    print("Parent 1: {0} ".format(p1))
    print("Parent 2: {0} ".format(p2))
    print("\nRecombining...")
    dpx_off = recombine(p1, p2)
    print("Offspring: {0}".format(dpx_off))
    print("Objective Value: {0}".format(evaluateOffpsring(dpx_off)))
