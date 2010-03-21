'''
 A* solver

 Searches a graph based on the Node class.
 Based on http://brandon.sternefamily.net/files/astar.txt
'''    
import sys, math, copy, decimal
from heapq import *

verbose = False
    
unique_node_id = 0
def getUniqueNodeId():
    "Return a unique id"
    global unique_node_id
    unique_node_id = unique_node_id + 1
    return unique_node_id
    
class Node:
    """Node in the Wolf Rabbit Cabbage graph"""
    def __init__(self, parent, state, g, h):
        self._state = state
        self._parent = parent
        self._children = []
        self._is_target = False
        self._unique_id = getUniqueNodeId()
        self._g_val = g(state)
        self._h_val = h(state)
         
    def f(self):
        "f() in the A* algo"
        return self._g_val + self._h_val
        
    def _describe(self):
        return self._state.describe() + ' - c = ' + str(len(self._children)) # + " " + str(self._visited) 
        
    def ancestorStates(self):
        "Return list of states of this node's ancestors not including itself"
        ancestors = []
        node = self._parent
        while node:
            ancestors.append(node._state)
            node = node._parent
        ancestors.reverse()
        return ancestors 
        
    def depth(self):
        return len(self.ancestorStates())
        
    def ancestorsContain(self, state):
        "Returns true if ancestorStates() contain state"
        for a in self.ancestorStates():
            if a == state:
                return True
        return False
           
    def nodeResult(self):   
        node_type = ''
        if len(self._children) == 0:
            node_type = 'dead-end'
        elif self._is_target:
            node_type = 'TARGET!'
        return node_type
        
    def astarResult(self):
        return '(' + str(self._g_val) + ' + ' + str(self._h_val) + ' = ' + str(self.f()) + ')'
        
    def describe(self):
        "Returns description of a node including ancestors and outcome"
        description = "node(" + str(self._unique_id) + "):"
        for state in self.ancestorStates():
            description += state.describe() + ', '
        description += self._state.describe() + ' ' + self.astarResult() + ' ' + str(len(self.ancestorStates()))
        return description
                    
def getChildNodes(node, g, h):
    '''Given a node with a state that is otherwise empty, return child nodes for all viable moves from that state'''
    child_nodes = []
    for move in node._state.allowedMoves():
        new_state = node._state.applyMove(move)
        if new_state.isValid() and not node.ancestorsContain(new_state):
            new_node = Node(node, new_state, g, h)
            child_nodes.append(new_node)
    # print 'child_nodes', [(n._unique_id, n._state.describe()) for n in child_nodes]
    return child_nodes
         
def sortFunc(node):
    return node.f()

def solve(starting_state, isTargetState, g, h, max_depth, verb):
    '''Find A* solution to path from starting_state to target_state with path-cost function g()
       and heuristic function h()'''
    
    verbose = verb
    priority_queue = []         # priority queue to store nodes
    heapify(priority_queue)
    visited = set([])           # set to store previously visited nodes

    heappush(priority_queue, Node(None, starting_state, g, h))  # put the initial node on the queue
 #   priority_queue.sort(key = sortFunc)  

    while (len(priority_queue) > 0):
        if verbose:
            print 'priority_queue', [(n._unique_id, n.f()) for n in priority_queue]
        node = heappop(priority_queue)
        if node._unique_id not in visited:
            if verbose:
                print node.describe()
            if isTargetState(node._state):
                return node
            elif node.depth() < max_depth:
                children = getChildNodes(node, g, h)
                #print 'children', [n._unique_id for n in children]
                for child in children:
                    child._parent = node
                    heappush(priority_queue, child)
                    visited = visited | set([node._unique_id])
                   # print '--priority_queue', [n._unique_id for n in priority_queue]
                priority_queue.sort(key = sortFunc)  # keep less costly nodes at the front
                     
    return None             # entire tree searched, no goal state found

  


