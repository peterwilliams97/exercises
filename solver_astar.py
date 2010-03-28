'''
 A* solver

 Searches a graph based on the Node class.
 Based on http://brandon.sternefamily.net/files/astar.txt
 
 See http://en.wikipedia.org/wiki/A*_search_algorithm
'''    
from heapq import *

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
        'Create a node with parent and state. g() is step-cost function. h() is path heuristic'
        self._state = state
        self._parent = parent
        self._children = []
        self._unique_id = getUniqueNodeId()
        self._g_val = g(state)
        self._h_val = h(state)
        
    def g_(self):
        'Path cost = sum of step costs'
        return sum(map(lambda x: x._g_val, self.ancestors()))
        
    def f(self):
        'f() in the A* algo'
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
        return map(lambda x: x._state, self.ancestors())
        
    def depth(self):
        'Returns depth of node in graph'
        return len(self.ancestors())
        
    def ancestorsContain(self, state):
        'Returns True if ancestorStates() contain state'
        for a in self.ancestorStates():
            if a == state:
                return True
        return False
           
    def describeAstar_(self):
        'Returns string describing A* values f = g + h'
        return '(' + pretty(self.g_()) + ' + ' + pretty(self._h_val) + ' = ' + pretty(self.f()) + ')'
        
    def describe(self):
        'Returns description of a node including ancestors and outcome'
        return 'node(' + str(self._unique_id) + '):' + ', '.join(map(lambda x: x.describe(), self.ancestorStates())) \
                      + self._state.describe() + ' ' + self.describeAstar_() + ' ' + str(self.depth())
         
def getChildNodes(node, g, h):
    'Given a node with a state that is otherwise empty, return child nodes for all viable moves from that state'
    child_nodes = []
    for move in node._state.allowedMoves():
        if node._state.isValidMove(move):
            new_state = node._state.applyMove(move)
            if not node.ancestorsContain(new_state):
                child_nodes.append(Node(node, new_state, g, h))
    return child_nodes
         
def solve(starting_state, isTargetState, g, h, graph_search, max_depth, verbose):
    '''Find A* solution to path from starting_state to state:isTargetState(state) returns Treu with path-cost function g()
       and heuristic function h()
       graph_search: False => tree search, True => graph search
       max_depth: max tree depth to search to
       verbose: set True for richer logging
    '''
    priority_queue = []         # priority queue to store nodes
    heapify(priority_queue)
    visited = set([])           # set to store previously visited nodes (the 'closed' set)
    closed_set = []             # same as visited but stores whole nodes instead of only unique_id
    
    heappush(priority_queue, Node(None, starting_state, g, h))  # put the initial node on the queue ('open' set)

    while len(priority_queue) > 0:
        if verbose:
            print '    open set   =', [(n._state.describe(), pretty(n.f())) for n in priority_queue] 
            print '    closed set =', [(n._state.describe(), pretty(n.f())) for n in closed_set]
                
        node = heappop(priority_queue)
        if node._unique_id not in visited:
            closed_set.append(node)
        if graph_search or node._unique_id not in visited:
            visited = visited | set([node._unique_id])
            if verbose:
                print node.describe()
            if isTargetState(node._state):
                return node
            elif node.depth() < max_depth:
                map(lambda n: heappush(priority_queue, n), getChildNodes(node, g, h))    
                priority_queue.sort(key = lambda n: n.f())  # keep less costly nodes at the front
    return None             # entire tree searched, no goal state found
    