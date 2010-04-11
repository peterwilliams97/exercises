'''
Describes the states of the Travelling Salesman
problem and the operations on them

Problem
-------
A salesman must visit each of n cities. There is a road between each pair of 
cities.  Starting at city #1. Find the route of minimal distance that visits each of 
the cities only once and returns to city #1.

References
    http://en.wikipedia.org/wiki/Travelling_salesman_problem
'''

import  math, copy, solver_astar, solver_backtrack

# Map nodes
A, B, C, D, E = range(ord('E') - ord('A') + 1)
cities = [A, B, C, D, E]
edges = { (A,B):7, (A,C):6,  (A,D):10, (A,E):13,
          (B,C):7, (B,D):10, (B,E):10,
          (C,D):5, (C,E):9, 
          (D,E):6 }  

def otherCity(edge, current_city):
    "Return the city other than current_city in the edge 2-tuple"
    assert(current_city in edge)
    return edge[{False:0, True:1}[edge[0]==current_city]]
    
def getEdgeDistance(city1, city2):
    "Return distance between city1 and city2"
    assert(city1 != city2)
    for key in edges.keys():
        if city1 in key and city2 in key:
            return edges[key]
    raise NameError('Non-existent edge requested')
    
class State:
    ''' Travelling salesman state.
        List of all cities visited excluding A
    '''
    
    def __init__(self, cities_visited):
        self._cities_visited = cities_visited[:]
        
    def signature(self):
        "Returns hashable object encompassing all state of State"
        return tuple(self._cities_visited)
               
    def __eq__(self, state):
        return self.signature() == state.signature() 
        
    def getCurrentCity(self):
        "Returns the current city for state, that is the last city visited"
        return len(self._cities_visited) > 0 and self._cities_visited[-1] or A 
    
    def validMove_(self, move, current_city):
        "Returns True if move is not to a city already visited"
        other_city = otherCity(move, current_city)
        if A in move and len(self._cities_visited) != 0 and len(self._cities_visited) != len(cities) - 1:
            return False
        return other_city not in self._cities_visited
         
    def allowedMoves(self):
        "Returns list of all moves allowed from current state"
        current_city = self.getCurrentCity()
        possible_moves = [e for e in edges.keys() if current_city in e] 
        return [Move(e) for e in possible_moves if self.validMove_(e, current_city)]
        
    def applyMove(self, move):
        "Returns State created by applying move to current state"
        return apply(move, self)
        
    def isValidMove(self, move):
        "Move is valid if state moved to contains no duplicates"
        new_state = apply(move, self)
        return len(set(new_state._cities_visited)) == len(new_state._cities_visited)    
        
    def describe(self):
        return 'A' + ''.join(map(lambda c: chr(c+ord('A')), self._cities_visited)) + ':' + str(gpath(self))
   
        
class Move:
    ''' Travelling salesman move.
        A graph edge.
    '''
    def __init__(self, edge):
        self._edge = edge
        
    def describe(self):
        return ''.join(map(lambda c: chr(c+ord('A')), self._edge))
      
        
def apply(move, state):
    "Apply move to state"
    assert(state.getCurrentCity() in move._edge)
    new_state = State(state._cities_visited)
    new_state._cities_visited.append(otherCity(move._edge, new_state.getCurrentCity()))
    return new_state
        
def isTargetState(state):
    "Test for final state"
    return set(cities).issubset(state._cities_visited)
    
def gpath(state):
    "Path cost function"
    last_city = A
    distance = 0
    if len(state._cities_visited) > 0:
        for city in state._cities_visited:
            distance += getEdgeDistance(last_city, city)
            last_city = city
    return distance
     
def h(state):
    "Heuristic function. Shortest path with city not currently in path"
    if len(state._cities_visited) == 0 or len(state._cities_visited) == len(cities):
        return 0
    current_city = state.getCurrentCity()
    allowed_moves = state.allowedMoves()
    allowed_cities = [apply(move, state).getCurrentCity() for move in allowed_moves if apply(move, state).getCurrentCity() != current_city]
    return min([getEdgeDistance(city, current_city) for city in allowed_cities])
  
 
if __name__ == '__main__':
    starting_state = State([])
    target_state = State([B, C, D, E])
    print '---------------------------------'
    print 'starting_state =', starting_state.describe()
    print 'target_state   =', target_state.describe()

    if True:
        tgstring = {False:'tree search', True:'graph search'}
        for graph_search in (False, True):
            print '---------------------------------', 'A*', tgstring[graph_search]
            node = solver_astar.solve(starting_state, isTargetState, None, h, graph_search, 20, True, gpath)
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
            node = solver_backtrack.solve(starting_state, isTargetState, gpath, h, 20, True, use_heuristic)
            print '---------------------------------'
            if node:
                print 'Solution =', node.describe()
            else:
                print 'No solution'
            print '---------------------------------'


        
 


