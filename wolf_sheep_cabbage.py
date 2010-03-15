import sys, math, copy, decimal

# Data types
Wolf, Rabbit, Cabbage = range(3)
Orig, Dest = range(2)


# Set of all players
all_things = set([Wolf, Rabbit, Cabbage])

# Possible outcomes of a search. 
# MovesLeft: there are moves left to make so keep searching
# NoMovesLeft: there are no moves left to make so give up
# FoundTarget: success    
MovesLeft, NoMovesLeft, FoundTarget = range(3)
result_map = { MovesLeft:'partial', NoMovesLeft:'dead-end', FoundTarget:'TARGET!' }

def describeResult(result):
    if result == MovesLeft:
        return 'partial'
    elif result == NoMovesLeft:
        return 'dead-end'
    elif result == FoundTarget:
        return 'TARGET'

class State:
    """Wolf Rabbit Cabbage state.
        _things_at_dest is set of these that have arrived at destination side
        _boat_at_dest is boat location """
    _things_at_dest = set([])
    _boat_at_dest = Orig
    def __init__(self, things_at_dest, boat):
        self._things_at_dest = things_at_dest
        self._boat_at_dest = boat
    def thingsOnSide(self, side):
        return (side == Orig) and all_things.difference(self._things_at_dest) or self._things_at_dest
    def dist(self):
        return len(self._things_at_dest)
    def describe(self) :
        return str(list(self._things_at_dest)) + ":" + str(self._boat_at_dest)

class Node:
    """Node in the Wolf Rabbit Cabbage graph"""
    _state = State(set([]), Orig)
    _parent = False
    _children = []
   # _visited = False
    def __init__(self, parent, state):
    #    print "new node:", self.describe()
        self._state = state
        self._parent = parent
        self. _children = []
        self._result = MovesLeft
       # self._visited = False
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
        return anc # list.reverse(anc) # anc.reverse()
    def describeAncestors(self):
        description = "ancestors: "
        for a in self.ancestorStates():
            description += a.describe() + ", "
        return description
    def describeNode(self):
        description = "node: "
        for a in self.ancestorStates():
            description += a.describe() + ", "
        description += self._state.describe() + " " + describeResult(self._result)
        return description
    def ancestorsContain(self, state):
        "Returns true if ancestorStates contain state"
        for a in self.ancestorStates():
            if a._things_at_dest == state._things_at_dest and a._boat_at_dest == state._boat_at_dest:
                return True
        return False
            
class Move:
    """A possible move. Has 1 or 2 passengers and a direction
        Direction is starting point of journey (from Orig or from Dest)"""
    _passengers = set([])
    _direction = Orig
    def __init__(self, passengers, direction):
        self._passengers = passengers
        self._direction = direction

def safeCombo(things):
    return things != set([Wolf, Rabbit]) and things != set([Rabbit, Cabbage]) 
    
def validState(state):
    """Tests for a valid move
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
        #print "    before:", new_state.describe()
        new_state._boat_at_dest = Orig
        #print "    after:", new_state.describe()
        for p in move._passengers:
            new_state._things_at_dest.remove(p)
   # print "   apply:", list(move._passengers), move._direction, " to", state.describe(), " ->", new_state.describe()
    return new_state
            
def subsetsOf(passengers):
    "Return list of all 1 and 2 element subsets of passengers"
    subsets = []
    p = list(passengers)
    for i in range(len(p)):
        subsets.append(set([p[i]]))
    for i in range(len(p)):
       for j in range(i+1, len(p)):
            subsets.append(set([p[i],p[j]]))
    return subsets
    
def possibleMoves(state):
    "Return list of all possible moves for state, some of which may be invalid"
    candidates = state.thingsOnSide(state._boat_at_dest)
   # print "  candidates =", list(candidates)
    moves = [Move(ss, state._boat_at_dest) for ss in subsetsOf(candidates)]
    return moves
    
def validMoves(moves):
    "Return list of valid moves in 'moves'"
    return [m for m in moves if safeCombo(m._passengers)]
    


 
def explore(node, target_state):
    """Given an node with a state that is otherwise empty, create child nodes for all viable moves from that state
       Return MovesLeft, NoMovesLeft or FoundTarget """
    result = NoMovesLeft
  #  print " explore:", node.describe()
    moves2 = possibleMoves(node._state)
    moves = validMoves(moves2)
   # for m in moves: print "  move =", list(m._passengers), m._direction
    for move in moves:
        new_state = apply(move, node._state)
        if validState(new_state) and not node.ancestorsContain(new_state):
            #print "** ", new_state.describe(), ":", node.describeAncestors()
            result = MovesLeft
            new_node = Node(node, new_state)
            print new_node.describeNode()
            node._children.append(new_node)
            if new_state._things_at_dest == target_state._things_at_dest:
                result = FoundTarget
                new_node._result = result
               # print new_node.describeNode()
                print "Found target ***"
                break
    node._result = result
    #print node.describeNode()
    # for c in node._children: print "   child =", c.describe()
    return result

max_depth = 4 
 
def search(G, node, target_state, depth):
    "Recursive function for depth first search of G, called for node"
    if depth > max_depth:
        return NoMovesLeft 
    #print "search:", node._state.describe(), " - ", node.describeAncestors()
    result = explore(node, target_state)
    if result == MovesLeft:
        result = NoMovesLeft
        for n in node._children:
            res = search(G, n, target_state, depth+1)
            if res == FoundTarget:
                result = FoundTarget
                break
            elif res == MovesLeft:
                result = MovesLeft 
    return result
    
    
def display(node, depth):
    "Recursively display a graph."
   # print "  " * depth, "node._state =", node._state.describe()
   # print "  " * depth, sorted(node._state)
    for c in node._children:
        display(c, depth + 1)
 
                       
def solve(starting_state, target_state):    
    G = Node(False, starting_state)
    search(G, G, target_state, 0)
   # display(G, 0)
 
def h(s):
    "Heuristic function"
    return s.dist()
    
def g(s):
    "Distance travelled"
    return h(s)
                            

        
   
    
if __name__ == '__main__':
    starting_state = State(set([]), Orig)
    target_state = State(set([Wolf, Rabbit, Cabbage]), Dest)
    print "starting_state =", starting_state.describe()
    print "starting_state.dist() =", starting_state.dist()
    print "target_state =", target_state.describe()
    print "target_state.dist() =", target_state.dist()
    solve(starting_state, target_state)
    
 


