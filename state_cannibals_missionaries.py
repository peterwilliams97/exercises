'''
Describes the states of the Cannibals and Missionaries
problem and the operations on them

Problem
-------
Three missionaries and three cannibals come to a river. There is a boat on 
their side of the river that can be used either by one or two persons. How 
should they use this boat to cross the river in such a way that cannibals never 
outnumber missionaries on either side of the river? 
'''

import  solver_astar, solver_backtrack

# Data types
Cannibals, Missionaries = range(2)
Orig, Dest = range(2)
location_map = {Orig:'O', Dest:'D'}
number_of_each = 3

class State:
    ''' Cannibals and Missionaries state.
        _cannibals_at_dest is # cannibals that have arrived at destination side
        _missionaries_at_dest is # missionaries that have arrived at destination side
        _boat_at_dest is boat location '''
        
    def __init__(self, cannibals_at_dest, missionaries_at_dest, boat_location):
        self._cannibals_at_dest = cannibals_at_dest
        self._missionaries_at_dest = missionaries_at_dest
        self._boat_location = boat_location
       
    def signature(self):
        "Returns hashable object encompassing all state of State"
        return (self._cannibals_at_dest, self._missionaries_at_dest, self._boat_location)     
           
    def __eq__(self, state):
        return self.signature() == state.signature()
              
    def peopleOnSide(self, side):
        result = (self._cannibals_at_dest, self._missionaries_at_dest)
        if (side == Orig): 
            result = map(lambda x: number_of_each - x, result)
        return result
            
    def allowedMoves(self):
        return validMoves(possibleMoves(self), self)
        
    def applyMove(self, move):
        return apply(move, self)
        
    def isValidMove(self, move):
        return validState(apply(move, self))
        
    def describe(self) :
        return str(self._cannibals_at_dest) + 'C:' + str(self._missionaries_at_dest) + 'M:' + location_map[self._boat_location]
            
class Move:
    '''A possible move. Has 1 or 2 passengers each of whom can be a M or a C and a direction
        _starting_point is starting point of journey (from Orig or from Dest)'''
    def __init__(self, cannibals, missionaries, starting_point):
        self._cannibals = cannibals
        self._missionaries = missionaries
        self._starting_point = starting_point
        
    def describe(self):
        return str(self._cannibals) + 'C:' + str(self._missionaries) + 'M:' + location_map[self._starting_point] 

def safeCombo(cannibals_misionaries):
    "Safe combinations of cannibals and missionaries"
    cannibals, missionaries = cannibals_misionaries
    return 0 <= cannibals and cannibals <= 3 and 0 <= missionaries and missionaries <= 3 and \
            cannibals <= missionaries or cannibals == 0 or missionaries == 0
    
def validState(state):
    '''Tests for a valid state
    Returns True if both sides of the river are safe'''
    return safeCombo(state.peopleOnSide(Orig)) and safeCombo(state.peopleOnSide(Dest))
    
def apply(move, state):
    "Apply a move to a state and return the resulting state"
    if state._boat_location == Orig:
        new_state = State(state._cannibals_at_dest + move._cannibals, state._missionaries_at_dest + move._missionaries, Dest)
    else:
        new_state = State(state._cannibals_at_dest - move._cannibals, state._missionaries_at_dest - move._missionaries, Orig)
    return new_state
            
def subsetsOf(passengers):
    "Returns set of all 1 and 2 element subsets of passengers. These are the allowed combinations of passengeers"
    return ((0,1), (1,0), (0,2), (1,1), (2,0))
    
def possibleMoves(state):
    "Returns list of all possible moves for state, some of which may be invalid"
    candidates = state.peopleOnSide(state._boat_location)
    return [Move(ss[0], ss[1], state._boat_location) for ss in subsetsOf(candidates)]
    
def validMoves(moves, state):
    "Return list of valid moves in 'moves'"
    return  [m for m in moves if validState(apply(m, state))]
 
def isTargetState(state):
    return state == target_state
    
def g(state):
    "Step cost function"
    return 1 # sum(state.peopleOnSide(Orig))
     
def h(state):
    "Heuristic function"
    return sum(state.peopleOnSide(Orig))
   
def hbest(state):
    "Null heuristic function. Guaranateed to be admissable"
    return 0
                            
if __name__ == '__main__':
    starting_state = State(0, 0, Orig)
    target_state = State(number_of_each, number_of_each, Dest)
    if True:
        tgstring = {False:'tree search', True:'graph search'}
        for graph_search in (True, False):
            print '---------------------------------', 'A*', tgstring[graph_search]
            if graph_search:
                node = solver_astar.solve(starting_state, isTargetState, g, hbest, graph_search, 20, True)
            else:
                node = solver_astar.solve(starting_state, isTargetState, g, h, graph_search, 20, True)
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
        
 


