#it is the node which store each state of puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h

    def f(self):
        return self.g + self.h