
class SubFunction:

    def __init__(self, weigth, variables):
        self.weigth = weigth # weight of the sub-function

        # variables: a list of integers (positive or negative) where the '-' sign indicates the negation of the variable
        self.variables = tuple([int(i) for i in variables])

        # in this tuple, the variables start at 0 to be compatible with everything else.
        # The same positions in both 'variables' and 'sub_function' correspond to the same variable
        self.sub_function = tuple([abs(i)-1 for i in variables]) # the respective sub-function, with variables without the indication of negation -- the parameters of the sub-function

    # t is a tuple of choices for each variable. t is assumed to have the sabe order as in self.sub_function and variables
    def evaluate(self, t):
        result = 0

        for i in range(len(t)):
            if(self.variables[i] < 0):
                result = result or (t[i]+1)%2 # if the variable is negated, flip its value
            else:
                result = result or t[i]

        return self.weigth*result # multiply the result of the sub-function by its weight

    # returns the tuple corresponding to the sub-function
    def getTuple(self):
        return self.sub_function

    def getNumberOfVariables(self):
        return len(self.variables)
