'''
 A* solver

 Searches a graph based on the Node class.
 Based on  http://en.wikipedia.org/wiki/A*_search_algorithm
 See also
    http://en.wikipedia.org/wiki/Consistent_heuristic
    http://en.wikipedia.org/wiki/Admissible_heuristic
'''    
from heapq import *

unique_node_id = 0
def getUniqueNodeId():
    'Returns a unique id'
    global unique_node_id
    unique_node_id = unique_node_id + 1
    return unique_node_id
 
def resetUniqueId():
    global unique_node_id
    unique_node_id = 0

def pretty(n):
    'Pretty string for number n'
    return str(round(n, 2))
    
class Node:
    'Node in the search graph'
    def __init__(self, parent, state, g, h, gpath):
        'Create a node with parent and state. g() is step-cost function. h() is path heuristic'
        self._state = state
        self._parent = parent
        self._children = []
        self._using_gpath = gpath != None
        assert((g==None) != (gpath==None))
        if gpath:
            self._g_path_val = gpath(state)
        else:
            self._g_step_val = g(state)
        self._h_path_val = h(state)
        self._unique_id = getUniqueNodeId()
        
    def __eq__(self, node):
        return self._state == node._state
        
    def g_(self):
        'Path cost = sum of step costs'
        if self._using_gpath:
            return self._g_path_val
        else:
            return sum(map(lambda x: x._g_step_val, self.ancestors())) + self._g_step_val
        
    def f(self):
        'f() in the A* algo'
        return self.g_() + self._h_path_val
        
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
        return '(' + pretty(self.g_()) + ' + ' + pretty(self._h_path_val) + ' = ' + pretty(self.f()) + ')'
        
    def describe(self):
        'Returns description of a node including ancestors and outcome'
        return 'node(' + str(self._unique_id) + '):' + ', '.join(map(lambda x: x.describe(), self.ancestorStates())) \
                      + ', ' + self._state.describe() + ' ' + self.describeAstar_() + ' ' + str(self.depth())
                    
         
def getNeighborNodes(node, g, h, gpath):
    'Given a node with a state that is otherwise empty, return neighbor nodes for all viable moves from that state'
    child_nodes = []
    for move in node._state.allowedMoves():
        if node._state.isValidMove(move):
            new_state = node._state.applyMove(move)
            if not node.ancestorsContain(new_state):
                child_nodes.append(Node(node, new_state, g, h, gpath))
    return child_nodes
         
def printNodesInList(name, alist, max_displayed): 
    print name + ':', len(alist), [(n._unique_id, n._state.describe(), pretty(n.f())) for i,n in enumerate(alist) if i < max_displayed], '+', max(len(alist) - max_displayed, 0), 'others'
    
def solve(starting_state, isTargetState, g, h, graph_search, max_depth, verbose, gpath = None):
    '''Find A* solution to path from starting_state to state:isTargetState(state) 
        g(): step cost function g(state) where state is described below
        gpath(): path cost function gpath(state). Exactly one of g and gpath must be specified
        h(): path cost heuristic h(state)
        graph_search: False => tree search, True => graph search t
        max_depth: max tree depth to search to
        verbose: set True for richer logging
       
        state is of class State where 
            members  __eq__(self, state), allowedMoves(self), isValidMove(self, move), applyMove(self, move). describe(self)
        move is of class Move move where
            members describe(self)
    '''
    assert((g==None) != (gpath==None))
    resetUniqueId()
    
    open_set = []           # priority queue to store nodes (the 'open' set)
    heapify(open_set)
    if graph_search:
        visited = set([])   # set to store previously visited node signatures (effficient version of the 'closed' set)
        closed_set = []     # same as visited but stores whole nodes instead of only signatures
        
    heappush(open_set, Node(None, starting_state, g, h, gpath))  # put the initial node on the queue 
  
    while len(open_set) > 0:
        if verbose:
            printNodesInList('open set  ', open_set, 5)
            if graph_search:
                printNodesInList('closed set', closed_set, 5)
     
        node = heappop(open_set)
        if verbose:
            print '     ' * (node.depth() + 1), node.describe()
        if isTargetState(node._state):      
            return node                     # Return goal state if found
        elif node.depth() < max_depth:
            if graph_search:
                visited = visited | set([node._state.signature()])
                closed_set.append(node)
                for neighbor in getNeighborNodes(node, g, h, gpath):
                    if neighbor._state.signature() not in visited:
                        if not neighbor in open_set:
                            heappush(open_set, neighbor)
                            assert(neighbor.f() >= node.f()) # http://en.wikipedia.org/wiki/Consistent_heuristic
            else:
                for neighbor in getNeighborNodes(node, g, h, gpath):
                    heappush(open_set, neighbor) 
                    assert(neighbor.f() >= node.f()) # http://en.wikipedia.org/wiki/Consistent_heuristic
            open_set.sort(key = lambda n: n.f())    # keep less costly nodes at the front
    return None                                     # Entire tree searched, goal state not found    
    