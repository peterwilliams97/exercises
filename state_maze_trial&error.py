'''
Describes the states of the Maze problem and the operations on them

Consider the simple maze presented below. 
3    S 
2    
1    G 
 1 2 3 
An agent is at the initial location S (3,3) and wishes to go to the final location G 
(1,3).  The agent can perform the following actions: Up, Down, Left and Right, 
which have their usual effect unless they are blocked by a wall (a thick line). 
The agent does NOT know where the walls are, and it cannot see the walls, even 
when standing next to them. So an action fails only when the agent bumps into a 
wall. 

'''

import sys, copy, solver_astar, solver_backtrack
from math import *

# Data types
Up, Down, Left, Right = range(4)
all_moves = set([Up, Down, Left, Right])
direction_names = { Up:'U', Down:'D', Left:'L', Right:'R' }

# Maze dimensions
grid_width = 3
grid_height = 3


class State:
    '''Maze state.
        x,y location and a direction '''
        
    def __init__(self, x, y, blocked = set([]), known_barriers = set([])):
        self._x = x
        self._y = y
        self._blocked = blocked
        self._known_barriers = known_barriers
        
    def __eq__(self, state):
        return self.signature() == state.signature()        
   
    def signature(self):
        return (self._x, self._y, len(self._blocked), len(self._known_barriers))
                 
    def allowedMoves(self):
        return possibleMoves(self)
        
    def applyMove(self, move):
        return apply(move, self)
               
    def isValidMove(self, move):
        "All moves are valid. Only find out after trying if they are invalid"
        return validMove(self, move, True)
        
    def describe(self) :
        return '[' + str(self._x+1) + ',' + str(self._y+1) + '|' + str(len(self._known_barriers)) + ']'      
            
class Move:
    '''A possible move. Has 1 or 2 passengers and a direction
        _starting_point is starting point of journey (from Orig or from Dest)'''
    def __init__(self, direction):
        self._direction = direction
       
    def describe(self):
        return direction_names[self._direction]

# Type of edge for a cell
Horizontal, Vertical = False, True

# List of all barriers
# Barrier element: x,y,vertical
#   x,y is the cell at the left, bottom of the edge
all_barriers = set([(Vertical, 1,2), (Horizontal, 1,1), (Horizontal, 2,1)])
known_barriers = set([])


# Map of edges a move could run into
# Direction: (Edge type, dx, dy)
edge_delta_table = { 
    Left: (Vertical,   0, 0),
    Right:(Vertical,   1, 0),
    Down: (Horizontal, 0, 0),
    Up:   (Horizontal, 0, 1)
}

def barrierForMove(state, move, known):
    if known:
        barriers = state._known_barriers
    else:
        barriers = all_barriers
    delta = edge_delta_table[move._direction]
    edge = (delta[0], state._x + delta[1], state._y + delta[2])
    if edge in barriers:
        return edge
    return None
    
def validMove(state, move, known):
    'Returns True if move is valid'
    return not barrierForMove(state, move, known)
 
move_table = { 
    Left: (-1,  0),
    Right:( 1,  0),
    Down: ( 0, -1),
    Up:   ( 0,  1)
} 
    
def apply(move, state):
    "Apply a move to a state and return the resulting state"
    barrier = barrierForMove(state, move, False)
    if barrier:
        new_state = State(state._x, state._y, state._blocked | set([move._direction]), state._known_barriers | set([barrier]))
    else:  
        delta = move_table[move._direction]  
        # Known barriers remain known
        new_state = State(state._x + delta[0], state._y + delta[1], known_barriers = state._known_barriers)
    return new_state
            
def possibleMoves(state):
    "Return list of all possible moves for state, some of which may be invalid"
    moves = []
    if state._y > 0:              moves.append(Move(Down))
    if state._x > 0:              moves.append(Move(Left))
    if state._x < grid_width - 1: moves.append(Move(Right))
    if state._y < grid_height -1: moves.append(Move(Up))
    moves.sort(key = lambda move: validMove(state, move, False) and not validMove(state, move, True) ) # Worst moves first  
    return moves

def isTargetState(state):
    return state == target_state 
    
def g(state):
    "Returns step cost for last state"
    return 1 + len(state._blocked)
     
def h(state):
    "Heuristic function"
    return abs(state._x-target_state._x) + abs(state._y-target_state._y)
     
def drawNode(node):
    "Draw as a 3x3 grid with numbers showing order in which squares were visited"
    ancestors = node.ancestorStates() + [node._state]
    def getIndex(x,y):
        s = ' '
        for i in [i for i,state in enumerate(ancestors) if state._x == x and state._y == y]:
            s = str(i)
            break
        return s
    for y in range(grid_height-1, -1, -1):
        print ','.join(map(lambda x: getIndex(x, y), range(grid_width)))
                                                                                  
if __name__ == '__main__':
    starting_state = State(2, 2)
    target_state = State(2, 0)
    print 'starting_state =', starting_state.describe()
    print 'target_state =', target_state.describe()
    if True:
        tgstring = {False:'tree search', True:'graph search'}
        for graph_search in (False, True):
            known_barriers = set([])
            print '---------------------------------', 'A*', tgstring[graph_search]
            node = solver_astar.solve(starting_state, isTargetState, g, h, graph_search, 20, True)
            print '---------------------------------'
            if node:
                print 'Solution =', node.describe()
                drawNode(node)
            else:
                print 'No solution'
            print '---------------------------------'
    if False:
        hstring = {False:'without heuristic', True:'with heuristic'}
        for use_heuristic in (True, False):
            known_barriers = set([])
            print '---------------------------------', 'Back tracking', hstring[use_heuristic]
            node = solver_backtrack.solve(starting_state, isTargetState, g, h, 20, True, use_heuristic)
            print '---------------------------------'
            if node:
                print 'Solution =', node.describe()
                drawNode(node)
            else:
                print 'No solution'
            print '---------------------------------'


 


