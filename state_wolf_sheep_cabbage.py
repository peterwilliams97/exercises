################################################################################
## First part of this file describes the states of the Wolf Rabbit Cabbage 
## problem and the operations on them
################################################################################

import sys, math, copy, decimal, solver_astar

# Data types
Wolf, Rabbit, Cabbage = range(3)
Orig, Dest = range(2)

# Set of all things
all_things = set([Wolf, Rabbit, Cabbage])

class State:
    '''Wolf Rabbit Cabbage state.
        _things_at_dest is set of these that have arrived at destination side
        _boat_at_dest is boat location '''
        
    def __init__(self, things_at_dest, boat):
        self._things_at_dest = things_at_dest
        self._boat_at_dest = boat
        
    def __eq__(self, state):
        return self._things_at_dest == state._things_at_dest and self._boat_at_dest == state._boat_at_dest
        
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
        
    def isValid(self):
        return validState(self)
        
    def describe(self) :
        return str(list(self._things_at_dest)) + ":" + str(self._boat_at_dest)
            
class Move:
    '''A possible move. Has 1 or 2 passengers and a direction
        _starting_point is starting point of journey (from Orig or from Dest)'''
    def __init__(self, passengers, starting_point):
        self._passengers = passengers
        self._starting_point = starting_point

def safeCombo(things):
    'Safe combinations of things - where no thing will eat another thing'
    return things != set([Wolf, Rabbit]) and things != set([Rabbit, Cabbage]) 
    
def validState(state):
    '''Tests for a valid state
    Returns True if both sides of the river are safe'''
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
    'Return list of all 0 and 1 element subsets of passengers. These are the allowed combinations of passengeers'
    subsets = [set([])]
    p = list(passengers)
    for i in range(len(p)):
        subsets.append(set([p[i]]))
    return subsets
    
def possibleMoves(state):
    'Return list of all possible moves for state, some of which may be invalid'
    candidates = state.thingsOnSide(state._boat_at_dest)
    moves = [Move(ss, state._boat_at_dest) for ss in subsetsOf(candidates)]
    return moves
    
def validMoves(moves):
    'Return list of valid moves in "moves"'
    return [m for m in moves if safeCombo(m._passengers)]
 
    
def g(state):
    'Path-cost function'
    return state.numThingsLeft() 
     
def h(state):
    'Heuristic function'
    return 0 # node._state.numThingsLeft() # + 1 - node._state._boat_at_dest
 
                            
if __name__ == '__main__':
    starting_state = State(set([]), Orig)
    target_state = State(set([Wolf, Rabbit, Cabbage]), Dest)
    print "starting_state =", starting_state.describe()
    print "target_state =", target_state.describe()
    node = solver_astar.solve(starting_state, target_state, g, h)
    print '---------------------------------'
    if node:
        print 'Solution =', node.describeNode()
    else:
        print 'No solution'
    
 


