'''
Describes the states of the Wolf Rabbit Cabbage 
problem and the operations on them
'''

import sys, math, copy, decimal, solver_astar, solver_backtrack

# Data types
Wolf, Rabbit, Cabbage = range(3)
Orig, Dest = range(2)

# Set of all things
all_things = set([Wolf, Rabbit, Cabbage])

# string for reporting 
names = { Wolf:'Wolf', Rabbit:'Rabbit', Cabbage:'Cabbage'}
boat_name = { False:'', True:' |Boat'}
direction_name = { False:'Orig->Dest', True:'Dest->Orig'}

class State:
    '''Wolf Rabbit Cabbage state.
        _things_at_dest is set of these that have arrived at destination side
        _boat_at_dest is boat location '''
        
    def __init__(self, things_at_dest, boat):
        self._things_at_dest = things_at_dest
        self._boat_at_dest = boat
        
    def signature(self):
        "Returns hashable object encompassing all state of State"
        return (frozenset(self._things_at_dest), self._boat_at_dest)
        
    def __eq__(self, state):
        return self.signature() == state.signature()
        
    def thingsOnSide(self, side):
        if side == Orig:
            return all_things.difference(self._things_at_dest)
        else:
            return self._things_at_dest
            
    def numThingsLeft(self):
        return len(self.thingsOnSide(Orig))
        
    def allowedMoves(self):
        return validMoves(possibleMoves(self))
        
    def applyMove(self, move):
        return apply(move, self)
        
    def isValidMove(self, move):
        return validState(apply(move, self))
        
    def describe(self):
        return '[' + ' '.join(map(lambda x: names[x], self.thingsOnSide(Dest))) +  boat_name[self._boat_at_dest] + ']'      
            
class Move:
    '''A possible move. Has 1 or 2 passengers and a direction
        _starting_point is starting point of journey (from Orig or from Dest)'''
    def __init__(self, passengers, starting_point):
        self._passengers = passengers
        self._starting_point = starting_point
        
    def describe(self):
        return '(' +  direction_name[self._starting_point] + ':' + ' '.join(map(lambda x: names[x], self._passengers)) + ')'

def safeCombo(things):
    'Safe combinations of things - where no thing will eat another thing'
    return things != set([Wolf, Rabbit]) and things != set([Rabbit, Cabbage]) 
    
def validState(state):
    'Tests for a valid state.  Returns True if both sides of the river are safe'
    if state._boat_at_dest:
        return safeCombo(state.thingsOnSide(Orig))
    else: 
        return safeCombo(state.thingsOnSide(Dest))
    
def apply(move, state):
    'Apply a move to a state and return the resulting state'
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
    "Return list of all 0 and 1 element subsets of passengers. These are the allowed combinations of passengers"
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
    'Return list of valid moves in "moves"'
    return [m for m in moves if safeCombo(m._passengers)]
 
def isTargetState(state):
    return state == target_state 
    
def g(state):
    "Step cost function"
    return 0
     
def h(state):
    "Heuristic function"
    #return 0  # http://en.wikipedia.org/wiki/Consistent_heuristic
    return state.numThingsLeft()  
                            
if __name__ == '__main__':
    starting_state = State(set([]), Orig)
    target_state = State(set([Wolf, Rabbit, Cabbage]), Dest)
    print "starting_state =", starting_state.describe()
    print "target_state =", target_state.describe()
    if False:
        tgstring = {False:'tree search', True:'graph search'}
        for graph_search in (False, True):
            print '---------------------------------', 'A*', tgstring[graph_search]
            node = solver_astar.solve(starting_state, isTargetState, None, h, graph_search, 20, True, g)
            print '  ---------------------------------'
            if node:
                print 'Solution =', node.describe()
            else:
                print 'No solution'
            print '---------------------------------'
    if True:
        hstring = {False:'without heuristic', True:'with heuristic'}
        for use_heuristic in (True, False):
            print '---------------------------------', 'Back tracking', hstring[use_heuristic]
            node = solver_backtrack.solve(starting_state, isTargetState, g, h, 20, True, use_heuristic)
            print '---------------------------------'
            if node:
                print 'Solution =', node.describe()
            else:
                print 'No solution'
            print '---------------------------------'

 


