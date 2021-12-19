import numpy as np
import sys
import instance
import NKLandscape
from OptimalRecombination import recombine

def evaluateOffpsring(off):

    nk_inst = instance.instance
    sfs = nk_inst.getSubFunctions()
    obj = 0
    for s in range(len(sfs)):
        sf = sfs[s]
        t = tuple([off[i] for i in sf])
        obj += nk_inst.getSFObjectiveValue(s, t)
    return abs(obj)

if __name__ == "__main__":

    if(len(sys.argv) < 4):
        print("Usage: {0} <num. of sub-functions> <num. of vars per sub-function> <num. of variables>".format(sys.argv[0]))
        exit(0)
    m, k, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

    instance.init(m, k, n)


    p1 = np.random.randint(2, size=n)
    p2 = np.random.randint(2, size=n)
    print("Parent 1: {0} ".format(p1))
    print("Parent 2: {0} ".format(p2))
    print("\nRecombining...")
    dpx_off = recombine(p1, p2)
    print("Offspring: {0}".format(dpx_off))
    print("Objective Value: {0}".format(evaluateOffpsring(dpx_off)))
