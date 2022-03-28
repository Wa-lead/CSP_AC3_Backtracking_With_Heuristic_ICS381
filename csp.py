from copy import deepcopy
class GraphColorCSP(object):

    def __init__(self, variables, colors, adjacency):
        self.variables = variables
        self.colors = colors
        self.adjacency = adjacency

    def diff_satisfied(self, var1, color1, var2, color2):
        if(not self.is_neighbor(var1, var2)):
            return True
        elif color1 != color2:
            return True
        else:
            return False

    def is_goal(self, assignment):
        if assignment is not None:
            if len(assignment) == len(self.variables):  # is it complete?
                for assign in assignment.keys():
                    for neighbor in self.adjacency[assign]:
                        if(not self.diff_satisfied(assign, assignment[assign], neighbor, assignment[neighbor])):
                            return False
                return True
        return False

    def check_partial_assignment(self, assignment):
        for assign in assignment.keys():
            for neighbor in self.adjacency[assign]:
                if(assignment.get(neighbor)):
                    if(not self.diff_satisfied(assign, assignment[assign], neighbor, assignment[neighbor])):
                        return False
        return True

    def is_neighbor(self, var1, var2):
        return var2 in self.adjacency[var1]

# ----------------------------------- AC3 --------------------------------
def ac3(graphcolorcsp, arcs_queue=None, current_domains=None, assignment=None):
    
    if(arcs_queue == None):
        arcs_queue = formArcQueue(graphcolorcsp)
    if(current_domains == None):
        current_domains = formCurrentDomain(graphcolorcsp)

    arcs_queue = set(arcs_queue)
    updated_domains = deepcopy(current_domains)
    while arcs_queue:
        xi, xj = arcs_queue.pop()
        if revise(graphcolorcsp, xi, xj, updated_domains):
            if len(updated_domains[xi]) == 0:
                return False, updated_domains
            for xk in (list(set(graphcolorcsp.adjacency[xi]) - {xj})):
                if xk not in assignment:
                    arcs_queue.add((xk, xi))

    return True, updated_domains

def revise(graphcolorcsp, xi, xj, updated_domains):
    revised = False
    for color in updated_domains[xi].copy():
        possible = canSatisfy(graphcolorcsp, xi, color,
                              xj, updated_domains[xj])
        if possible == False:
            updated_domains[xi].remove(color)
            revised = True
    return revised

# ------- AC3 helper functions --------------------------------


def canSatisfy(graphcolorcsp, xi, color, xj, colorsOfxj):
    return True in [graphcolorcsp.diff_satisfied(xi, color, xj, color2) for color2 in colorsOfxj]

def formArcQueue(graphcolorcsp):
    arcs_queue = set({})
    for vertex in graphcolorcsp.adjacency:
        for neighbor in graphcolorcsp.adjacency[vertex]:
            arcs_queue.add((neighbor, vertex))
    return arcs_queue

def formCurrentDomain(graphcolorcsp):
    return {var: list(graphcolorcsp.colors) for var in graphcolorcsp.variables}

# ----------------------------------- backtracking functions --------------------------------


def backtracking(graphcolorcsp):
    current_domains = formCurrentDomain(graphcolorcsp)
    return backtracking_helper(graphcolorcsp, {}, current_domains)

def backtracking_helper(graphcolorcsp, assignment={}, current_domains=None):
    if len(assignment) == len(graphcolorcsp.variables):
        return assignment
    variable = selection_heuristic(graphcolorcsp,assignment,current_domains)
    for color in LCV(graphcolorcsp,current_domains,variable,assignment):
        if isConsistentWithAssignment(graphcolorcsp, assignment, variable, color):
            assignment.setdefault(variable, color)
            current_domains[variable] = set([color]) #enforce the domain ##In normal cases I should've done this on a copy and modify it back if the inference fails so it can go to the other colors, but my LCV returns the whole domain which is a seperate list
            inference, updated_domains = ac3(graphcolorcsp, formArcQueueBacktracking(
                graphcolorcsp, variable), current_domains, assignment)
            if inference:
                result = backtracking_helper(graphcolorcsp,deepcopy(assignment), deepcopy(updated_domains))
                if result is not None: return result
            assignment.pop(variable)
        ## should've modified it back to original domain if LCV did not return a seperate list and only modified the reference.
    return None
            


# ------- backtracking helper functions --------------------------------
def selection_heuristic(graphcolorcsp, assignment,current_domains):
    vars = set(graphcolorcsp.variables)
    assignments = set(assignment.keys())
    available_vars = (vars - assignments)
    MRV_DEG = {}
    for var in available_vars: # create a dictionary that holds the MRV and DEG of every avaliable variable
        MRV = len(current_domains[var])
        DEG = len(set(graphcolorcsp.adjacency[var]) - set(assignment.keys()))
        MRV_DEG.setdefault(var,((1/MRV),DEG)) ## it is stored this way for sortig puproses (lowestMRV+HighestDegree)
        
    chosenVar = sorted(MRV_DEG, key=lambda x: (MRV_DEG[x][0],MRV_DEG[x][1]),reverse=True)[0]
    return chosenVar

def isConsistentWithAssignment(graphcolorcsp, assignment, variable, color):
    for a in assignment:
        if not graphcolorcsp.diff_satisfied(variable, color, a, assignment[a]):
            return False
    return True

def formArcQueueBacktracking(graphcolorcsp, variable):
    arcs_queue = set({})
    for neighbor in graphcolorcsp.adjacency[variable]:
        arcs_queue.add((neighbor, variable))
    return arcs_queue

def LCV (graphcolorcsp,current_domains,variable,assignment):
    highestLCV = []
    for color in current_domains[variable]:
        totalChoices = 0
        for neighbor in list(set(graphcolorcsp.adjacency[variable]) - set(assignment.keys())):
            totalChoices += len(set(current_domains[neighbor])-{color})
        highestLCV.append((color,totalChoices))
    highestLCV = sorted(highestLCV, key=lambda x: x[1],reverse=True)
    return [color[0] for color in highestLCV] 