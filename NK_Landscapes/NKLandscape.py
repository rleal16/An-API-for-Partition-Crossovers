import numpy as np
import random as rnd
#from utils import *
from collections import defaultdict

def getBinaryArray(b, n_bits):
    if n_bits == 0:
        return []
    return [int(i) for i in np.binary_repr(b, n_bits)]

def binArrayToInt(bin_array):
    val = 0
    for b in bin_array:
        val = (val << 1) | b
    return val


class NKLandscape:

    """
    n is the number of variables
    m is the number of sub-functions
    k is the maximum number of variables per function (and the exact, in this case, for simplicity)
    """
    def __init__(self, m, k, n):

        if(m > n):
            print("The number of sub-functions can not be greater than the number of variables")
            exit(0)
        if(n>m*k):
            print("The total number of variables exceeds the total number of variables in the functions")
            exit(0)

        self.n = n
        self.k = k
        self.m = m
        self.vars = [i for i in range(self.n)]
        self.createSubfunctions()
        self.setSubFunctionsValues()

    # Create the sub-functions for this instance
    def createSubfunctions(self):

        self.subFunctions = []

        sf_mx = np.zeros((self.m, self.n)) # matrix of m sub-functions by n variables, that coresponds to the adjacency matrix of VIG
        vars = [i for i in range(self.n)]

        rnd.shuffle(vars) # shuffle the variables

        vars_per_sf = np.zeros(self.m) # the number of variables in each sub-function

        # add each variables to one sub-function (make sure every variable is in at least one sub-function)
        sf = 0
        while(len(vars) > 0):
            v = vars.pop(0)
            sf_mx[sf][v] = 1 # add variable v to sub-function sf
            vars_per_sf[sf] += 1
            sf = (sf+1)%self.m # loop through all (potential) sub-functions until all variables are in a sub-function


        # complete the sub-functions until every one has k variables
        vars = [i for i in range(self.n)]
        rnd.shuffle(vars)
        sf = 0
        while(sf < self.m):

            # skip functions that already have k variables
            while(sf < self.m and vars_per_sf[sf] == self.k):
                sf+=1

            # fill the sub-function until it has k variables
            rnd.shuffle(vars)
            v_ix = 0
            while(sf < self.m and vars_per_sf[sf] < self.k):

                while(v_ix < self.n and sf_mx[sf][vars[v_ix]] == 1):
                    v_ix+=1

                if(v_ix < self.n):
                    sf_mx[sf][vars[v_ix]] = 1
                    vars_per_sf[sf] += 1

            sf += 1 # skip this sub-function

        # convert the sub-functions to tuples
        for sf in range(self.m):
            self.subFunctions.append(tuple(sorted([i for i in range(len(sf_mx[sf])) if sf_mx[sf][i] == 1])))


    # for each sub-function, for each combination of values in its variables, assign a random real number as its objective value
    def setSubFunctionsValues(self):

        # first key is the index of the sub-function in self.subFunctions; second key is a combination of values between its variables; value is a float
        self.sFuncsValues = defaultdict(lambda : defaultdict(float))

        for i in range(len(self.subFunctions)):
            nVars = len(self.subFunctions[i]) # to support sub-functions with < k variables
            for a in range(nVars**2-1):
                bin_tuple = tuple(getBinaryArray(a, nVars)) # here we are considering the ordering of the variables in self.subFunctions
                self.sFuncsValues[i][bin_tuple] = rnd.randint(5, 50)


    # get the objective value of a sub-function sf_ix, givena tuple of values for its variables, t
    def getSFObjectiveValue(self, sf_ix, t):
        return self.sFuncsValues[sf_ix][t]

    def getSubFunctionsEvals(self):
        return self.sFuncsValues

    def getSubFunctions(self):
        return self.subFunctions

    def getNumOfVariables(self):
        return self.n
