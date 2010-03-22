'''
Describes the states of the Travelling Salesman
problem and the operations on them

Problem
-------
A salesman must visit each of n cities. There is a road between each pair of 
cities.  Starting at city #1. Find the route of minimal distance that visits each of 
the cities only once and returns to city #1.
'''

import sys, math,  random

# Map nodes
num_cities = ord('E') - ord('A') + 1
A, B, C, D, E = range(num_cities)   # All cities
free_cities = [B, C, D, E]          # Cities whose order of visiting may be changed
edges = { (A,B):7, (A,C):6,  (A,D):10, (A,E):13,
          (B,C):7, (B,D):10, (B,E):10,
          (C,D):5, (C,E):9, 
          (D,E):6 }  
          
# Path = [A, all free cities, A], A is implied first and last city
num_free_cities = len(free_cities)
    
def getEdgeDistance(city1, city2):
    'Return distance between city1 and city2'
    assert(city1 != city2)
    keys = [key for key in edges.keys() if city1 in key and city2 in key]
    return edges[keys[0]] 

def pathLength(path):
    'Path-cost function'
    full_path = [A] + path + [A]
    return sum([getEdgeDistance(full_path[i-1],full_path[i]) for i in range(1, len(full_path))])
  
def describe(path):
    return ''.join(map(lambda c: chr(c+ord('A')), path)) + ':' + str(pathLength(path))
    
def doSwap(path, i, j):
    'Returns copy of path with ith and jth elements swapped'
    copy = path[:]
    copy[i],copy[j] = copy[j],copy[i]
    return copy
    
def allSwaps(path):
    'Returns list of possible swappings on path'
    r = range(num_free_cities)
    #r = [2,3,1,0] 
    #r = [3,2,0,1]
    return [doSwap(path,i,j) for j in r for i in r if i > j]
    #for i in range(num_free_cities):
    #    for j in range(i+1, num_free_cities):
    #        yield doSwap(path, i, j)
            
def bestNeighboringPath(path):
    'Returns shortest path that is one swap away from path'
    shortest_path = path
    shortest_distance = pathLength(path)
    all_swaps = allSwaps(path)
    for swap in all_swaps:
        distance = pathLength(swap)
        # print ' swap =', describe(swap)
        if distance < shortest_distance:
            shortest_path = swap
            shortest_distance = distance
    return shortest_path
    
            
def hillclimb(start_path, max_iterations):
    'Finds shortest path by hill climibing and returns shortest path and number of rounds to find it'
    assert(len(start_path) == num_free_cities)
    path = start_path
    for i in range(max_iterations):
        new_path = bestNeighboringPath(path)
        if new_path == path:        # top of hill
            break
        path = new_path
        #print 'path =', describe(path), ', iterations =', i
    return (path, i)
   
minimum_temperature = 0.1    
determinsitic = True

def prob(current_val, val, temperature):
    'Returns probability of accepting val given current_val and temperature'
    assert(temperature >= minimum_temperature)
    if val < current_val:
        return 1.0
    elif temperature < minimum_temperature:
        return 0.0
    else:
        #print '$$$', current_val, val, temperature
        if determinsitic:
            return 0.0
        else:
            return math.exp(-abs(val-current_val)/temperature) 
        
def isGoodEnough(current_val, val, temperature, probFunc):
    p = probFunc(current_val, val, temperature)
    return random.random() < p
        
def cool(temperature, alpha):
    return max(temperature*alpha, minimum_temperature)
    
def goodNeighboringPath(path, temperature):
    'Returns shortest path that is one swap away from path'
    shortest_path = path
    shortest_distance = pathLength(path)
    all_swaps = allSwaps(path)
    for swap in all_swaps:
        distance = pathLength(swap)
        # print ' swap =', describe(swap)
        if determinsitic:
            assert(isGoodEnough(shortest_distance, distance, temperature, prob) == (distance < shortest_distance))
        if isGoodEnough(shortest_distance, distance, temperature, prob):
            shortest_path = swap
            shortest_distance = distance
    return shortest_path    
   
def anneal(start_path, max_iterations, start_temp, alpha):
    'Finds shortest path by simulated annealing and returns shortest path and number of rounds to find it'
    assert(len(start_path) == num_free_cities)
    path = start_path
    temp = start_temp
    for i in range(max_iterations):
        assert(temp >= minimum_temperature)
        new_path = goodNeighboringPath(path, temp)
        if determinsitic:
            new_path2 = bestNeighboringPath(path)
            if new_path != new_path2:
                print new_path2, new_path
            assert(new_path2 == new_path)
        if new_path == path:        # top of hill
            break
        path = new_path
        temp = cool(temp, alpha)
        #print 'path =', describe(path), ', iterations =', i
    return (path, i)             
            
def allPaths():   
    'Returns list of all possible paths'
    all_paths = [[city] for city in free_cities]
    for i in range(len(free_cities) - 1):
        new_paths = []
        for path in all_paths:
            for city in free_cities:
                if city not in path:
                    p = path[:]
                    p.append(city)
                    new_paths.append(p)
        all_paths = new_paths[:]
    all_paths.sort(cmp = lambda p1, p2: pathLength(p1) - pathLength(p2))
    return all_paths
    
 
if __name__ == '__main__':
    determinsitic = False
    if False:
        for i in range(10):
            print i, random.random()
        for current_val in range(1, 4):
            for val in range(1,4):
                tf = isGoodEnough(current_val, val, 4, prob)
                print 'isGoodEnough', current_val, val, '=', tf, ' =', val < current_val
                if determinsitic:
                    assert(tf == (val < current_val))

    max_iterations = 10
    all_paths = allPaths()
    if True:
        print '------------------ Complete List of Paths ------------------'
        for path in all_paths:
            print describe(path)
        
    if True:
        print '------------------ Testing All Starting Paths ------------------'
        total_rounds = 0
        for path in all_paths:
            best_path, rounds = hillclimb(path, max_iterations)
            total_rounds += rounds
            print describe(path), '--', describe(best_path), 'in', str(rounds), 'rounds'
        print 'Average rounds', float(total_rounds)/float(len(all_paths))
            
    if False:
        print '------------------ Testing Simulated Annealing Params ------------------'
        start_path = all_paths[-1]  # longest path
        for start_temp in [0, 2, 3, 4, 10, 20, 30, 40, 100, 200]:
            start_temp = max(start_temp, minimum_temperature)
            for a in range(1, 5):
                alpha = 1 - 0.02*a
                best_path, rounds = anneal(start_path, max_iterations, start_temp, alpha)
                print 'start_temp', start_temp, 'alpha', alpha, describe(start_path), '--', describe(best_path), 'in', str(rounds), 'rounds'

    if True:
        print '------------------ Testing Simulated Annealing Params ------------------'
        start_path = all_paths[-1]  # longest path
        temp_values = [0.0+float(x)/10.0 for x in range(30)] + range(3, 10)  + range(10, 100, 10) + range(100, 1000, 100)
        
        results = []
        summary_results = []
        for start_temp in temp_values:
            start_temp = max(start_temp, minimum_temperature)
            for a in range(1, 21):
                alpha = 1 - 0.01*a
                param_results = []
                for start_path in all_paths:
                    best_path, rounds = anneal(start_path, max_iterations, start_temp, alpha)
                    #print 'start_temp', start_temp, 'alpha', alpha, describe(start_path), '--', describe(best_path), 'in', str(rounds), 'rounds'
                    result = (pathLength(best_path), best_path, rounds, start_temp, alpha)
                    results.append(result)
                    param_results.append(result)
                num_paths = float(len(all_paths))
                summary = [float(sum(map(lambda e: e[i], param_results)))/num_paths for i in [0, 2]]
                summary += [start_temp, alpha]
                summary_results.append(summary)
               # print start_temp, alpha, map(str, summary)
        
        def sortFunc(s1):
            return (s1[0], s1[1], 1000.0 - s1[2], 1000.0 - s1[3])
                    
        summary_results.sort(key = sortFunc)
        for summary in summary_results:
            print map(str, summary)
        
 


