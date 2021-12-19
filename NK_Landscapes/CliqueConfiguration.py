"""
Stores information about a given clique, in particular its best residue choices for each separator choices.

Note: 'value' and 'variables' were chosen to mean the same as in the reference paper: Chicano, F., Ochoa, G., Whitley, D. and Tinós, R. (2019) ‘Quasi-Optimal Recombination Operator’, Lecture Notes in Computer Science.Springer International Publishing, pp. 131–146.
doi: 10.1007/978-3-030-16711-0_9.
"""

from Graph import Graph
import numpy as np
class CliqueConfiguration:
    def __init__(self, id, clique_id, cliqueVariables, separator, residue):
        self.id = id
        self.clique_id = clique_id
        self.clique = cliqueVariables
        self.separator = separator
        self.residue = residue
        self.resConfiguration = None
        self.sepConfiguration = None
        self.value = np.full(2**len(separator), np.inf)
        self.variables = np.full(2**len(separator), 0)

    # Return the objective value associated with the choices, x_s, for each of the separator's variables, that corresponds to a given set of choices in the residue's variables.
    def getValue(self, x_s):
        return self.value[x_s]

    # Set the objective value associated with the choices, sep, for each of the separator's variables, that corresponds to a given set of choices in the residue's variables.
    def setValue(self, sep, val):
        self.value[sep] = val

    # Assign binary choices for the residue, in x_r, to a given set o binary choices in the separator x_s
    # Note: self.variables and self.value should match. Where sep = x_s and the value must correspond to objective value of x_s with x_r
    def setVariables(self, x_s, x_r):
        self.variables[x_s] = x_r

    def getVariables(self, x_s):
        return self.variables[x_s]

    def getResidue(self):
        return self.residue

    def getSeparator(self):
        return self.separator

    def getAllValues(self):
        return self.value
