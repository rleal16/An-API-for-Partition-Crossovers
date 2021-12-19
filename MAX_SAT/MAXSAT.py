"""
Constructs an MaxSAT instance according with the format for complete weighted instances in: https://maxsat-evaluations.github.io
"""


import numpy as np
import random as rnd
from collections import defaultdict
from SubFunction import *

class MAXSAT:

    def __init__(self, inst_file):

        self.sub_functions = []
        with open(inst_file, "r") as f:
            line = f.readline().split()
            while(line[0] != "p"):

                line = f.readline().split()
            # reads the number of variables and clauses (sub-functions)
            self.nvar, self.nclauses = int(line[2]), int(line[3])

            # constructs the sub-functions by reading each clause in the instance file
            # Each sub-function is an instance of the classe SubFunction
            line = f.readline().split()
            while(len(line) > 0):
                w = int(line[0])
                vars = [int(line[i]) for i in range(1, len(line)-1)] # exclude the first value (of the weight) and the last one (the 'stop sign' 0)
                self.sub_functions.append(SubFunction(w, vars))
                line = f.readline().split()

    def getSubFunctions(self):
        return [s.getTuple() for s in self.sub_functions]

    def evaluate(self, i, t):
        return self.sub_functions[i].evaluate(t)

    def getNumberOfVariables(self):
        return self.nvar

    def getNumberOfClauses(self):
        return self.nclauses
