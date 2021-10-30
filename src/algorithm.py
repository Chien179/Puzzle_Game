import numpy
from copy import deepcopy
from node import Node

#direction matrix
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}


def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return row, current_state[row].index(element)


def getBestNode(openSet):
    firstIter = True
    bestNode = None
    bestF = None

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


class AStar:
    def __init__(self, puzzle, size):
        self.__open_set = {}
        self.__closed_set = {}
        self.__size = size
        self.__puzzle = puzzle
        end = [i for i in range(1, self.__size**2 + 1)]
        self.__goal = numpy.reshape(end, (self.__size, self.__size)).tolist()

    #main function of node
    def solve(self):
        self.__open_set = {str(self.__puzzle): Node(self.__puzzle, self.__puzzle, 0, self.__euclidianCost(self.__puzzle))}

        while True:
            test_node = getBestNode(self.__open_set)
            self.__closed_set[str(test_node.current_node)] = test_node

            if test_node.current_node == self.__goal:
                return self.__buildPath(self.__closed_set)

            adj_node = self.__getAdjNode(test_node)
            for node in adj_node:
                if str(node.current_node) in self.__closed_set.keys() \
                        or str(node.current_node) in self.__open_set.keys() \
                        and self.__open_set[str(node.current_node)].f() < node.f():
                    continue
                self.__open_set[str(node.current_node)] = node

            del self.__open_set[str(test_node.current_node)]

    #it is a distance calculation algo
    def __euclidianCost(self, current_state):
        cost = 0
        for row in range(len(current_state)):
            for col in range(len(current_state[0])):
                pos = get_pos(self.__goal, current_state[row][col])
                cost += abs(row - pos[0]) + abs(col - pos[1])
        return cost

    #get adjucent Nodes
    def __getAdjNode(self, node):
        listNode = []
        emptyPos = get_pos(node.current_node, self.__size**2)

        for dir in DIRECTIONS.keys():
            newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
            if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
                newState = deepcopy(node.current_node)
                newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
                newState[newPos[0]][newPos[1]] = self.__size**2
                listNode.append(Node(newState, node.current_node, node.g + 1, self.__euclidianCost(newState)))

        return listNode

    #get the best node available among nodes

    #this functionn create the smallest path
    def __buildPath(self, closedSet):
        node = closedSet[str(self.__goal)]
        branch = []

        while node.g:
            branch.append(node.current_node)
            node = closedSet[str(node.previous_node)]
        branch.append(node.current_node)
        branch.reverse()

        return branch
