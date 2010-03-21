'''
Describes the states of the Travelling Salesman
problem and the operations on them

Problem
-------
A salesman must visit each of n cities. There is a road between each pair of 
cities.  Starting at city #1. Find the route of minimal distance that visits each of 
the cities only once and returns to city #1.
'''

import sys, math, copy, decimal, solver_astar

# Map nodes
A, B, C, D, E = range(ord('E') - ord('A') + 1)
cities = [A, B, C, D, E]
edges = { (A,B):7, (A,C):6,  (A,D):10, (A,E):13,
          (B,C):7, (B,D):10, (B,E):10,
          (C,D):5, (C,E):9, 
          (D,E):6 }  

def otherCity(edge, current_city):
    'Return the city other than current_city in the edge 2-tuple'
    assert(current_city in edge)
    return edge[{False:0, True:1}[edge[0]==current_city]]
    
def getEdgeDistance(city1, city2):
    'Return distance between city1 and city2'
    if city1 == city2:
        print 'city1 == city ==', city1
    assert(city1 != city2)
    keys = [key for key in edges.keys() if city1 in key and city2 in key]
    return edges[key] 
    
def getCurrentCity(state):
    'Returns the current city for state'
    if len(state._cities_visited) == 0:
        current_city = A
    else:
        current_city = state._cities_visited[-1]
    return current_city
    
class State:
    ''' Travelling salesman state.
        List of all cities visited excluding A
    '''
    
    def __init__(self, cities_visited):
        self._cities_visited = copy.deepcopy(cities_visited)
               
    def __eq__(self, state):
        return self._cities_visited == state._cities_visited 
        
    def validMove_(self, move, current_city):
        other_city = otherCity(move, current_city)
        if A in move and len(self._cities_visited) != 0 and len(self._cities_visited) != len(cities) - 1:
            return False
        for city in self._cities_visited:
            if other_city == city:
                return False
        return True
        
    def allowedMoves(self):
        current_city = getCurrentCity(self)
        possible_moves = [e for e in edges.keys() if current_city in e] 
      #  print 'possible_moves', current_city, ':', str(possible_moves)
     #   print 'possible_cities', current_city, ':', str([otherCity(e, current_city) for e in possible_moves])
        valid_moves = [e for e in possible_moves if self.validMove_(e, current_city)]
        #Sprint 'allowedMoves', current_city, ':', str(valid_moves)
        return valid_moves
        
    def applyMove(self, move):
        return apply(move, self)
        
    def isValid(self):
        'A state is valid if it contains no duplicates'
        return len(set(self._cities_visited)) == len(self._cities_visited)
        
    def describe(self):
        return str(self._cities_visited)
        
        
def apply(move, state):
    'Apply move to state'
    assert(getCurrentCity(state) in move)
    new_state = State(state._cities_visited)
    new_state._cities_visited.append(otherCity(move, getCurrentCity(state)))
  #  print 'apply', str(move), state.describe(), ' ->', new_state.describe()
    return new_state
        
def isTargetState(state):
    'Test for final state'
    return set(cities).issubset(state._cities_visited)
    
def g(state):
    'Path-cost function'
    last_city = A
    distance = 0
    if len(state._cities_visited) > 0:
        for city in state._cities_visited:
            distance += getEdgeDistance(last_city, city)
            last_city = city
  #  print 'g =', state.describe(), '=', distance
    return distance
     
def h(state):
    'Heuristic function'
    if len(state._cities_visited) == 0 or len(state._cities_visited) == len(cities):
        return 0
    current_city = getCurrentCity(state)
    allowed_moves = state.allowedMoves()
  #  print 'allowed_moves =', allowed_moves
    allowed_cities = [getCurrentCity(apply(move, state)) for move in allowed_moves if getCurrentCity(apply(move, state)) != current_city]
  #  print 'current_city =', current_city, 'allowed_cities =', allowed_cities  
    distance = min([getEdgeDistance(city, current_city) for city in allowed_cities])
  #  print 'h =', state.describe(), '=', distance
    return distance
 
if __name__ == '__main__':
    starting_state = State([])
    target_state = State([B, C, D, E])
    print '---------------------------------'
    print 'starting_state =', starting_state.describe()
    print 'target_state   =', target_state.describe()

    print '---------------------------------'
    node = solver_astar.solve(starting_state, isTargetState, g, h, 13, True)
    print '---------------------------------'
    if node:
        print 'Solution =', node.describe()
    else:
        print 'No solution'
        
 


