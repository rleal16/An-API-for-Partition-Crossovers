
import instance
class PX:

    def __init__(self, p1, p2):

        self.p1 = p1
        self.p2 = p2
        self.original_subfunctions = instance.instance.getSubFunctions()
        self.createSubfunctions()


    """
    Helper functions
    """

    # Identify common and different variables between the parents
    def findCommonVariables(self):
        self.commonVars = [] # list of common variables
        self.diffVars = [] # list of the different variables that will compose the new sub-functions sent to the algorithm

        for i in range(len(self.p1)):
            if(self.p1[i] != self.p2[i]):
                self.diffVars.append(i)
            else:
                self.commonVars.append(i)

        self.diffVars.sort()
        self.commonVars.sort()

        self.varsMap = {} # mapping original variables *to* new variable (index)
        self.varsMapInv = {} # inverse mapping of self.varsMap

        # Create a mapping for diffVars so that the corresponding variables in the new sub-functions are numbered consecutively
        for ix in range(len(self.diffVars)):
            v = self.diffVars[ix]
            self.varsMap[v] = ix
            self.varsMapInv[ix] = v


    # create the new sub-functions, by removing the variables with values in common in the original sub-functions
    # the arguments (variables) in the new sub-functions (tuples) are determined according with self.varsMap

    def createSubfunctions(self):
        self.sfs = [] # list of tuples, the new sub-functions
        self.sfsMapping = {} # Create a mapping of sub-function indices from the original sub-function to the new one. This is needed to take into account original sub-functions whose variables have the same value in both parents and, as such, there are no remaining variables to create a new sub-function
        self.sfsMappingInv = {} # inverse of self.sfsMapping

        # search for common variables (and different)
        self.findCommonVariables()

        for s in range(len(self.original_subfunctions)):
            sf = self.original_subfunctions[s]
            n_sf = [] # the new subFunction

            # create the new sub-function from sf with only variables with different values in both parents
            for v in sf:
                if(v in self.diffVars):
                    n_sf.append(self.varsMap[v])

            if(len(n_sf)>0):
                self.sfsMapping[s] = len(self.sfs)
                self.sfsMappingInv[self.sfsMapping[s]] = s
                self.sfs.append(tuple(n_sf))





    """
    API Functions
    """

    def components(self):
        return len(self.diffVars) # the number of components corresponds to the number of variables that are different in both parents

    # returns tuples that represent the new sub-functions
    def subfunctions(self):
        return self.sfs

    def evaluate(self, i, t):

        orig_sf = self.original_subfunctions[self.sfsMappingInv[i]]

        n_sf = self.sfs[i]

        map = {}

        for v in orig_sf:
            map[v] = -1 # initialize the mapping for all variable in orig_sf (a super-set of n_sf)

        # Create a mapping of each choice for each variable in the new, modified component, without variables with common values in both parents
        # This must be done because the variables in n_sf might not be consective in orig_sf. We need varsMapInv turn the variables in n_sf to the real variable that each represents.
        for v in range(len(n_sf)):
            var = self.varsMapInv[n_sf[v]] # get the variable in the original sub-function
            if(t[v] == 0):
                map[var] = self.p1[var]
            else:
                map[var] = self.p2[var]

        # the reaming variables, without an assignment are those that have the same value in both parents.
        for v in map.keys():
            if(map[v] == -1):
                map[v] = self.p1[v] # if no value was assigned is because this variable has the same value in both parents

        new_t = tuple([map[v] for v in orig_sf]) # construct the new tuple with all the variables, considering the order they appear in the original sub-function

        # negate the objective value of the sub-function, because the implementation of the DPX assumes minimization
        return -1*instance.instance.getSFObjectiveValue(self.sfsMappingInv[i], new_t)

    # construct the offsring given the choices in t (a tuple), where a value of 0 corresponds to self.p1 and 1 to self.p2
    def offspring(self, t):

        # each index, i, in t represents the variable i, as it was sent to the algorithm in the sub-functions, according to varsMap
        off = [-1]*len(self.p1)

        for v in range(len(t)):
            real_v = self.varsMapInv[v]
            if(t[v] == 0):
                off[real_v] = self.p1[real_v]
            else:
                off[real_v] = self.p2[real_v]

        # add the common values
        for v in self.commonVars:
            off[v] = self.p1[v]

        return off
