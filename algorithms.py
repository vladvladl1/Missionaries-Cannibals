# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import itertools
import copy
import util
import math

class cannibalsProblem:
    # three difficulties are available: 0 - easy, 1 - medium, 2 - hard
    def __init__(self, difficulty):
        if difficulty == 0:
            self.boatSize = 2
            self.nrIndividuals = 3
        elif difficulty == 1:
            self.boatSize = 3
            self.nrIndividuals = 5
        elif difficulty == 2:
            self.boatSize = 4
            self.nrIndividuals = 8
        else:
            self.boatSize = 2
            self.nrIndividuals = 3


        # at the beginning all individuals, along with the boat are on the left side of the river
        self.startState = [self.nrIndividuals, self.nrIndividuals, 0, 0, 's']

        # all the possible actions in the given problem scenario
        self.possibleActions = list(itertools.combinations_with_replacement(['c', 'm', '/'], self.boatSize))
        self.possibleActions.remove(tuple(['/' for i in range(self.boatSize)]))

    def getStartState(self):
        return self.startState

    # the goal state is defined by all individuals being on the right side of the river
    def isGoalState(self, state):
        return state[2] == self.nrIndividuals and state[3] == self.nrIndividuals

    def getBoatSize(self):
        return self.boatSize

    def getNrIndividuals(self):
        return self.nrIndividuals

    # expands a current state(node) and receives all its valid children, among with actions taken
    def expand(self, state):
        children = []

        for action in self.getActions(state):
            children.append((self.getNextState(state, action), state, action))

        return children

    # returns a list of all valid actions starting from a given space
    def getActions(self, state):
        validActions = []

        for action in self.possibleActions:
            movedCannibals = action.count('c')
            movedMissionaries = action.count('m')

            # in case the boat is on the left
            if state[len(state) - 1] == 's':
                # checks whether there are enough cannibals/ missionaries to take in te boat
                if movedMissionaries <= state[1] and movedCannibals <= state[0]:
                    # checks whether on the current flank the number of missionaries would be
                    # overwhelmed by the number of cannibals
                    if state[1] - movedMissionaries >= state[0] - movedCannibals or state[1] - movedMissionaries == 0:
                        #checks whether on the opposite flank the number of missionaries would be
                        #overwhelmed by the number of cannibals
                        if state[3] + movedMissionaries >= state[2] + movedCannibals or state[3] - movedMissionaries== 0:
                            validActions.append(action + ('>',))
            # similar, in case th boat is on the right
            else:
                if movedMissionaries <= state[3] and movedCannibals <= state[2]:
                    if state[3] - movedMissionaries >= state[2] - movedCannibals or state[3] - movedMissionaries == 0:
                        if state[1] + movedMissionaries >= state[0] + movedCannibals or state[1] == 0:
                            validActions.append(action + ('<',))

        return validActions

    # gets the next state based on a previous state and an action
    def getNextState(self, state, action):
        newState = copy.deepcopy(state)
        movedMissionaries = action.count('m')
        movedCannibals = action.count('c')

        # if the movement of the boat is left to right ('>' = boat moving right, '<' = boat moving left)
        if action[len(action) - 1] == '>':
            # the new state will find the boat on the opposite side of the previous one
            newState[len(newState) - 1] = 'd'
            # updates number of missionaries and cannibals
            newState[1] -= movedMissionaries
            newState[3] += movedMissionaries
            newState[0] -= movedCannibals
            newState[2] += movedCannibals
        else:
            # similar, in case the boat moves from right to left
            newState[len(newState) - 1] = 's'
            newState[3] -= movedMissionaries
            newState[1] += movedMissionaries
            newState[2] -= movedCannibals
            newState[0] += movedCannibals

        return newState


class aStarNode:
    def __init__(self, state, parent, action, g, h, f):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = f

    def __str__(self):
        return "State: %s, parent: %r, action taken: %s, g: %s, h: %s, f: %s " % (
        self.state, self.parent, self.action, self.g, self.h, self.f)

    def getState(self):
        return self.state

    def getAction(self):
        return self.action

    def getParent(self):
        return self.parent

    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def getF(self):
        return self.f


# the custom node pushed to the Queue
class CustomNode:

    # the state, the parent node, action taken from parent and the total path cost are stored
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):
        return "State: %s, parent: %r, action taken: %s, path cost: %s" %(self.state, self.parent, self.action, self.path_cost)

    def getState(self):
        return self.state

    def getAction(self):
        return self.action

    def getParent(self):
        return self.parent

    def getCost(self):
        return self.path_cost

# uses the BFS algorithm to find the shortest path
def breadthFirstSearch(problem):

    solution = []
    visited_states = []
    nodesExpanded = 0
    queue = util.Queue()
    extracted = None

    # pushing the root into the queue
    queue.push(CustomNode(problem.getStartState(), None, None, 0))

    while not queue.isEmpty():
        extracted = queue.pop()
        crt = extracted.getState()

        if problem.isGoalState(crt):
            print("Cost: ", extracted.getCost(), " Nodes expanded: ", nodesExpanded)
            break

        if crt in visited_states:
            continue

        # adds node to territory and expands it
        visited_states.append(crt)
        succ = problem.expand(crt)
        nodesExpanded += 1

        # adds new nodes to the frontier
        for i in succ:
            if i[0] not in visited_states:
                queue.push(CustomNode(i[0], extracted, i[2], extracted.getCost() + 1))

    # creates the solution by iterating backwards through that branch of the tree
    while extracted.getParent() is not None:
        solution.append(extracted.getAction())
        extracted = extracted.getParent()

    solution.reverse()

    return solution


def depthFirstSearch(problem):

    solution = []
    visited_states = []
    nodesExpanded = 0
    stack = util.Stack()
    extracted = None

    # pushing the root into the queue
    stack.push(CustomNode(problem.getStartState(), None, None, 0))

    while not stack.isEmpty():
        extracted = stack.pop()
        crt = extracted.getState()

        if problem.isGoalState(crt):
            print("Cost: ", extracted.getCost(), " Nodes expanded: ", nodesExpanded)
            break

        if crt in visited_states:
            continue

        # adds node to territory and expands it
        visited_states.append(crt)
        succ = problem.expand(crt)
        nodesExpanded += 1

        # adds new nodes to the frontier
        for i in succ:
            if i[0] not in visited_states:
                stack.push(CustomNode(i[0], extracted, i[2], extracted.getCost() + 1))

    # creates the solution by iterating backwards through that branch of the tree
    while extracted.getParent() is not None:
        solution.append(extracted.getAction())
        extracted = extracted.getParent()

    solution.reverse()
    return solution

def uniformCostSearch(problem):

    solution = []
    visited_states = []
    nodesExpanded = 0
    pque = util.PriorityQueue()
    extracted = None

    # pushing the root into the queue
    pque.push(CustomNode(problem.getStartState(), None, None, 0), 0)

    while not pque.isEmpty():
        extracted = pque.pop()
        crt = extracted.getState()

        if problem.isGoalState(crt):
            print("Cost: ", extracted.getCost(), " Nodes expanded: ", nodesExpanded)
            break

        if crt in visited_states:
            continue

        # adds node to territory and expands it
        visited_states.append(crt)
        succ = problem.expand(crt)
        nodesExpanded += 1

        # adds new nodes to the frontier
        for i in succ:
            if i[0] not in visited_states:
                pque.push(CustomNode(i[0], extracted, i[2], extracted.getCost() + 1),
                          CustomNode(i[0], extracted, i[2], extracted.getCost() + 1).getCost() )

    # creates the solution by iterating backwards through that branch of the tree
    while extracted.getParent() is not None:
        solution.append(extracted.getAction())
        extracted = extracted.getParent()

    solution.reverse()

    return solution


def heuristic(node, problem):
    return 2 * math.ceil((node[0] + node[1] ) / (problem.getBoatSize()))

def aStarSearch(problem):
    solution = []

    start_node = problem.getStartState()
    start_heuristic = heuristic(start_node, problem)
    visited_nodes = []
    pque = util.PriorityQueue()
    extracted = None
    pque.push(aStarNode(start_node, None, None, 0, start_heuristic, start_heuristic), start_heuristic)
    actions = []

    nodesExpanded = 0
    while not pque.isEmpty():
        extracted = pque.pop()
        crt = extracted.getState()

        if problem.isGoalState(crt):
            print("Cost: ", extracted.getG(), " Nodes expanded: ", nodesExpanded)
            break

        if crt in visited_nodes:
            continue

        visited_nodes.append(crt)
        nodesExpanded += 1

        for nextstate, state, action in problem.expand(crt):
            if nextstate not in visited_nodes:
                # Get cost so far
                cost_actions = extracted.getG()+1;
                get_heuristic = heuristic(nextstate, problem)
                pque.push(aStarNode(nextstate, extracted, action, cost_actions, get_heuristic,cost_actions+get_heuristic ),get_heuristic)


    while extracted.getParent() is not None:
        solution.append(extracted.getAction())
        extracted = extracted.getParent()

    solution.reverse()
    return solution

if __name__ == '__main__':
    problema = cannibalsProblem(2)
    print(breadthFirstSearch(problema))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
