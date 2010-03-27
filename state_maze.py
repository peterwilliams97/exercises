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
        
    def __init__(self, x, y):
        self._x = x
        self._y = y
        
    def __eq__(self, state):
        return self._x == state._x and self._y == state._y
        
    def allowedMoves(self):
        return possibleMoves(self)
        
    def applyMove(self, move):
        return apply(move, self)
         
    def isValid(self):
        return validState(self)
        
    def isValidMove(self, move):
        return validMove(self, move)
        
    def describe(self) :
        return '[' + str(self._x+1) + ',' + str(self._y+1) + ']'      
            
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
barriers = set([(Vertical, 1,2), (Horizontal, 1,1), (Horizontal, 2,1)])

# Map of edges a move could run into
# Direction: (Edge type, dx, dy)
edge_delta_table = { 
    Left: (Vertical,   0, 0),
    Right:(Vertical,   1, 0),
    Down: (Horizontal, 0, 0),
    Up:   (Horizontal, 0, 1)
}

def validMove(state, move):
    'Returns True if move is valid'
    delta = edge_delta_table[move._direction]
    edge = (delta[0], state._x + delta[1], state._y + delta[2])
    return edge not in barriers
 
move_table = { 
    Left: (-1,  0),
    Right:( 1,  0),
    Down: ( 0, -1),
    Up:   ( 0,  1)
} 
    
def apply(move, state):
    'Apply a move to a state and return the resulting state'
    delta = move_table[move._direction]
    return State(state._x + delta[0], state._y + delta[1])
            
    
def possibleMoves(state):
    'Return list of all possible moves for state, some of which may be invalid'
    moves = []
    if state._x > 0:
        moves.append(Move(Left))
    if state._x < grid_width -1:
        moves.append(Move(Right))
    if state._y > 0:
        moves.append(Move(Down))
    if state._y < grid_height -1:
        moves.append(Move(Up))
    #print 'possibleMoves for', state.describe(), '=', [m.describe() for m in moves] 
    return moves

 
def isTargetState(state):
    return state == target_state 
    
def g(state):
    'Path-cost function. Returns step cost for last state'
    return 1
     
def h(state):
    'Heuristic function'
    return sqrt((state._x-target_state._x)**2 + (state._y-target_state._y)**2) 
    #return (state._x-target_state._x)*(state._x-target_state._x) + (state._y-target_state._y)*(state._y-target_state._y) 
 
def drawNode(node):
    'Draw as a 3x3 grid with numbers showing order in which squares were visited'
    ancestors = node.ancestorStates() + [node._state]
    for y in range(grid_height-1, -1, -1):
        line = ''
        for x in range(grid_width):
            s = ' '
            for i in range(len(ancestors)):
                state = ancestors[i]
                if x == state._x and y == state._y:
                    s = str(i)
                    break
            line = line + s + ','
        print line
                                                                                  
if __name__ == '__main__':
    starting_state = State(2, 2)
    target_state = State(2, 0)
    print "starting_state =", starting_state.describe()
    print "target_state =", target_state.describe()
    if True:
        tgstring = {False:'tree search', True:'graph search'}
        for graph_search in (False, True):
            print '---------------------------------', 'A*', tgstring[graph_search]
            node = solver_astar.solve(starting_state, isTargetState, g, h, graph_search, 20, True)
            print '  ---------------------------------'
            if node:
                print 'Solution =', node.describe()
            else:
                print 'No solution'
            print '---------------------------------'
    if False:
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


 


