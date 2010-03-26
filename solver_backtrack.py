'''
 A* solver

 Searches a graph based on the Node class.
 Based on http://brandon.sternefamily.net/files/astar.txt
'''    
import sys, math, copy

    
unique_node_id = 0
def getUniqueNodeId():
    'Returns a unique id'
    global unique_node_id
    unique_node_id = unique_node_id + 1
    return unique_node_id
    
class Node:
    'Node in the search graph'
    def __init__(self, parent, state, move, g, h):
        self._parent = parent
        self._state = state
        self._move = move
        self._g_val = g(state)
        self._h_val = h(state)
        self._children = []
        self._is_target = False
        self._unique_id = getUniqueNodeId()
          
    def f(self):
        'f() in the A* algo'
        return self._g_val + self._h_val
    
    def describeState(self):
         return self._state.describe()
    
    def _describe(self):
        'Returns gtring description of node. Assumes state has describe() function that does same'
        return self._state.describe() + ' - c = ' + str(len(self._children)) # + " " + str(self._visited) 
        
    def ancestorStates(self):
        "Returns list of states of this node's ancestors not including itself"
        ancestors = []
        node = self._parent
        while node:
            ancestors.append(node._state)
            node = node._parent
        ancestors.reverse()
        return ancestors 
        
    def depth(self):
        'Returns depth of node in graph'
        return len(self.ancestorStates())
        
    def ancestorsContain(self, state):
        'Returns true if ancestorStates() contain state'
        for a in self.ancestorStates():
            if a == state:
                return True
        return False
    
    def describeH(self):
        'Returns string describing heuristic value'
        return str(self.f()) 
        
    def describeMove(self):
        if self._move:
            return self._move.describe()
        else:
            return 'none'
            
    def describe(self):
        'Returns description of a node including ancestors and outcome'
        description = 'node(' + str(self._unique_id) + '):'
        description = ''
        for state in self.ancestorStates():
            description += state.describe() + ', '
        description += self._state.describe() + '' + self.describeH() # + ' ' + str(len(self.ancestorStates()))
        return description
  
def sortFunc(node):
    return node.f()
    
def sortFuncBad(node):
    return -node.f()    
                                          
def getChildNodes(node, g, h, useHeuristic):
    'Given a node with a state that is otherwise empty, return child nodes for all viable moves from that state'
    child_nodes = []
    for move in node._state.allowedMoves():
        if node._state.isValidMove(move):
            new_state = node._state.applyMove(move)
            child_nodes.append(Node(node, new_state, move, g, h))
    if useHeuristic:
        child_nodes.sort(key = sortFunc)
    else:
        child_nodes.sort(key = sortFuncBad)
    return child_nodes
  
def isAncestorState(parent, node): 
    'Return True iff nodd state is the same as an ancestor state'
    return parent and parent.ancestorsContain(node._state)
 
def report(spacer, outcome):
    print spacer, '*', outcome
                 
def solveNode(node, isTargetState, g, h, max_depth, verbose, useHeuristic):
    'Find backtracking solution to path from node to isTargetState() with path-cost/heuristic function g()'
    one_space = '     ' 
    spacer = one_space * node.depth()
    if verbose:
        print spacer, node.describeState() 
        
    if isTargetState(node._state):
        report(spacer, 'Target!')
        return node
    elif isAncestorState(node._parent, node):
        report(spacer, 'Previous state')
    elif node.depth() >= max_depth:
        report(spacer, 'Max depth')
    else:
        children = getChildNodes(node, g, h, useHeuristic)
        if len(children) == 0:
            report(spacer, 'Dead-end')
        else:
            possibles = 'Possible moves = ' + ', '.join(map(lambda x: x.describeMove() + '=>' + x.describeState() + x.describeH(), children))
            print spacer + one_space, possibles
            for child in children:
                child._parent = node
                new_node = solveNode(child, isTargetState, g, h, max_depth, verbose, useHeuristic)
                if new_node:
                    return new_node
    return None                                                      

def solve(starting_state, isTargetState, g, h, max_depth, verbose, useHeuristic):
    node = Node(None, starting_state, False, g, h)
    return solveNode(node, isTargetState, g, h, max_depth, verbose, useHeuristic)
    
