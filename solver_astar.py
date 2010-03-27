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
    'Returns a unique id'
    global unique_node_id
    unique_node_id = unique_node_id + 1
    return unique_node_id
    
def pretty(n):
    'Pretty string for number n'
    return str(round(n, 2))
    
class Node:
    'Node in the search graph'
    def __init__(self, parent, state, g, h):
        self._state = state
        self._parent = parent
        self._children = []
        self._is_target = False
        self._unique_id = getUniqueNodeId()
        self._g_val = g(state)
        self._h_val = h(state)
        
    def g_(self):
        return sum(map(lambda x: x._g_val, self.ancestors()))
        
    def f(self):
        'f() in the A* algo'
       # return self._g_val + self._h_val
        return self.g_() + self._h_val
        
    def _describe(self):
        'Returns string description of node. Assumes state has describe() function that does same'
        return self._state.describe() + ' - c = ' + str(len(self._children)) # + " " + str(self._visited) 
     
    def ancestors(self):
        "Returns list of this node's ancestors not including itself"
        ancestors = []
        node = self._parent
        while node:
            ancestors.append(node)
            node = node._parent
        ancestors.reverse()
        return ancestors 
        
    def ancestorStates(self):
        "Returns list of states of this node's ancestors not including itself"
        ancestors = []
        node = self._parent
        while node:
            ancestors.append(node._state)
            node = node._parent
        ancestors.reverse()
        return ancestors 
        # return map(lambda x: x._state, self.ancestors())
        
    def depth(self):
        'Returns depth of node in graph'
        return len(self.ancestorStates())
        
    def ancestorsContain(self, state):
        'Returns True if ancestorStates() contain state'
        for a in self.ancestorStates():
            if a == state:
                return True
        return False
           
    #def describeResult_(self):   
    #    'Returns string describing result'
    #    node_type = ''
    #    if len(self._children) == 0:
    #        node_type = 'dead-end'
    #    elif self._is_target:
    #        node_type = 'TARGET!'
    #    return node_type
    
    def describeAstar_(self):
        'Returns string describing A* values f = g + h'
        return '(' + pretty(self.g_()) + ' + ' + pretty(self._h_val) + ' = ' + pretty(self.f()) + ')'
        
    def describe(self):
        'Returns description of a node including ancestors and outcome'
        description = "node(" + str(self._unique_id) + "):"
        for state in self.ancestorStates():
            description += state.describe() + ', '
        description += self._state.describe() + ' ' + self.describeAstar_() + ' ' + str(len(self.ancestorStates()))
        return description
                    
def getChildNodes(node, g, h):
    'Given a node with a state that is otherwise empty, return child nodes for all viable moves from that state'
    child_nodes = []
   # print 'allowed moves =', [move.describe() for  move in node._state.allowedMoves()]
    for move in node._state.allowedMoves():
        if node._state.isValidMove(move):
            new_state = node._state.applyMove(move)
            if  not node.ancestorsContain(new_state):
                new_node = Node(node, new_state, g, h)
                child_nodes.append(new_node)
    # print 'child_nodes', [(n._unique_id, n._state.describe()) for n in child_nodes]
    return child_nodes
         
def sortFunc(node):
    return node.f()

def solve(starting_state, isTargetState, g, h, max_depth, verbose):
    '''Find A* solution to path from starting_state to target_state with path-cost function g()
       and heuristic function h()'''
    
    priority_queue = []         # priority queue to store nodes
    heapify(priority_queue)
    visited = set([])           # set to store previously visited nodes

    heappush(priority_queue, Node(None, starting_state, g, h))  # put the initial node on the queue
 #   priority_queue.sort(key = sortFunc)  

    while (len(priority_queue) > 0):
        if verbose and False:
            print '   priority_queue =', [(n._state.describe(), pretty(n.f())) for n in priority_queue]
        node = heappop(priority_queue)
        if node._unique_id not in visited:
            if verbose:
                print node.describe()
            if isTargetState(node._state):
                return node
            elif node.depth() < max_depth:
                children = getChildNodes(node, g, h)
                #print 'children =', [n._state.describe()  for n in children]
                for child in children:
                    child._parent = node
                    heappush(priority_queue, child)
                    visited = visited | set([node._unique_id])
                   # print '--priority_queue', [n._unique_id for n in priority_queue]
                priority_queue.sort(key = sortFunc)  # keep less costly nodes at the front
                     
    return None             # entire tree searched, no goal state found

  


