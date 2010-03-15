import sys, math, copy, decimal

################################################################################
## First part of this file describes the states of the Wolf Rabbit Cabbage 
## problem and the operations on them
################################################################################
# Data types
Wolf, Rabbit, Cabbage = range(3)
Orig, Dest = range(2)

# Set of all things
all_things = set([Wolf, Rabbit, Cabbage])

class State:
    """Wolf Rabbit Cabbage state.
        _things_at_dest is set of these that have arrived at destination side
        _boat_at_dest is boat location """
    def __init__(self, things_at_dest, boat):
        self._things_at_dest = things_at_dest
        self._boat_at_dest = boat
    def thingsOnSide(self, side):
        if side == Orig:
            return all_things.difference(self._things_at_dest)
        else:
            return self._things_at_dest
    def describe(self) :
        return str(list(self._things_at_dest)) + ":" + str(self._boat_at_dest)
            
class Move:
    """A possible move. Has 1 or 2 passengers and a direction
        _starting_point is starting point of journey (from Orig or from Dest)"""
    def __init__(self, passengers, starting_point):
        self._passengers = passengers
        self._starting_point = starting_point

def safeCombo(things):
    "Safe combinations of things - where no thing will eat another thing"
    return things != set([Wolf, Rabbit]) and things != set([Rabbit, Cabbage]) 
    
def validState(state):
    """Tests for a valid state
    Returns True if both sides of the river are safe"""
    if state._boat_at_dest:
        return safeCombo(state.thingsOnSide(Orig))
    else: 
        return safeCombo(state.thingsOnSide(Dest))
    
def apply(move, state):
    "Apply a move to a state and return the resulting state"
    new_state = copy.deepcopy(state)
    if state._boat_at_dest == Orig:
        new_state._boat_at_dest = Dest
        for p in move._passengers:
            new_state._things_at_dest.add(p)
    else:
        new_state._boat_at_dest = Orig
        for p in move._passengers:
            new_state._things_at_dest.remove(p)
    return new_state
            
def subsetsOf(passengers):
    "Return list of all 0 and 1 element subsets of passengers"
    subsets = [set([])]
    p = list(passengers)
    for i in range(len(p)):
        subsets.append(set([p[i]]))
    return subsets
    
def possibleMoves(state):
    "Return list of all possible moves for state, some of which may be invalid"
    candidates = state.thingsOnSide(state._boat_at_dest)
    moves = [Move(ss, state._boat_at_dest) for ss in subsetsOf(candidates)]
    return moves
    
def validMoves(moves):
    "Return list of valid moves in 'moves'"
    return [m for m in moves if safeCombo(m._passengers)]
    
################################################################################
## Second part of this file describes a search graph based on the Node class.
################################################################################    
    
unique_node_id = 0
def getUniqueNodeId():
    global unique_node_id
    unique_node_id = unique_node_id + 1
    return unique_node_id
    
class Node:
    """Node in the Wolf Rabbit Cabbage graph"""
    def __init__(self, parent, state):
        self._state = state
        self._parent = parent
        self. _children = []
        self._is_target = False
        self._unique_id = getUniqueNodeId()
    def describe(self):
        return self._state.describe() + " - c = " + str(len(self._children)) # + " " + str(self._visited)
    def ancestorStates(self):
        "Return list of states of this node's ancestors not including itself"
        anc = []
        node = self._parent
        while node:
            anc.append(node._state)
            node = node._parent
        anc.reverse()
        return anc 
    def ancestorsContain(self, state):
        "Returns true if ancestorStates contain state"
        for a in self.ancestorStates():
            if a._things_at_dest == state._things_at_dest and a._boat_at_dest == state._boat_at_dest:
                return True
        return False
    def describeAncestors(self):
        description = "ancestors: "
        for a in self.ancestorStates():
            description += a.describe() + ", "
        return description
    def nodeResult(self):   
        node_type = ''
        if self._is_target:
            node_type = 'TARGET!'
        elif len(self._children) == 0:
            node_type = 'dead-end'
        return node_type
    def describeNode(self):
        "Returns description of a node including ancestors and outcome"
        description = "node(" + str(self._unique_id) + "):"
        for a in self.ancestorStates():
            description += a.describe() + ', '
        description += self._state.describe() + ' ' +  self.nodeResult() + ' ' + str(len(self.ancestorStates()))
        return description
        
def addChildNodes(node, target_state):
    """Given a node with a state that is otherwise empty, create child nodes for all viable moves from that state
       and detects target nodes """
    for move in validMoves(possibleMoves(node._state)):
        new_state = apply(move, node._state)
        if validState(new_state) and not node.ancestorsContain(new_state):
            new_node = Node(node, new_state)
            node._children.append(new_node)
            new_node._is_target = (new_state._things_at_dest == target_state._things_at_dest)

max_depth = 10 
 
def search(G, node, target_state, depth):
    "Search for target_state in node. Called recursively for depth-first search of G"
    if depth <= max_depth and not node._is_target:
        addChildNodes(node, target_state)
        for n in node._children:
            search(G, n, target_state, depth+1)
                        
def appendNode(node_list, node):
    "Append node and all its children to node_list"
    node_list.append(node)
    for c in node._children:
        appendNode(node_list, c)

def gatherNodes(G):
    "Gather all nodes in graph G into a list and return that list"
    node_list = []
    appendNode(node_list, G)
    return node_list
 
def solve(starting_state, target_state): 
    "Find paths from starting_state to target_state"
    G = Node(False, starting_state)
    search(G, G, target_state, 0)
    node_list = gatherNodes(G)
    print '=================================== All nodes'
    for node in node_list:
        print node.describeNode()
    print '=================================== Solution nodes'
    for node in  filter(lambda node: node._is_target, node_list):
        print node.describeNode()
   
 
def h(s):
    "Heuristic function"
    return s.dist()
    
def g(s):
    "Path-cost function"
    return h(s)
                            
if __name__ == '__main__':
    starting_state = State(set([]), Orig)
    target_state = State(set([Wolf, Rabbit, Cabbage]), Dest)
    print "starting_state =", starting_state.describe()
    print "target_state =", target_state.describe()
    solve(starting_state, target_state)
    
 


