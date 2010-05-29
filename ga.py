'''

Simple Genetic Algorithm example
                        
Created on 11/05/2010

@author: peter
'''
import copy, decimal, random
from math import *
      
answer = [0, 0, 1, 0, 1, 0]
def numDigits():
    return len(answer)

random.seed(0)
    
def numCorrect(guess):
    correct = [1 if x[0] == x[1] else 0 for x in zip(guess, answer)]
    return sum(correct)

def opposite(guess):
    return [1 if x == 0 else 0 for x in guess]

def mutate(guess):
    g = guess[:]
    n = random.randrange(numDigits())
    m = g[n]
    g[n] = 1 if g[n] == 0 else 0
    print 'mutate', n, guess, '=>', g, m, g[n]
    return g

def makeGuess(num_digits):
    return [random.choice([0,1]) for i in range(num_digits)]

def crossOver(guess1, guess2):
    assert(len(guess1) == numDigits())
    assert(len(guess2) == numDigits())
    n = random.randrange(numDigits())
    g1, g2 = guess1[:], guess2[:]
    g1[n], g2[n] = g2[n], g1[n]
    return (g1, g2)
             
def ga():
    global answer
    answer = makeGuess(20)
    p1 = makeGuess(numDigits())
    p2 = opposite(p1)
    print 'Answer  ', numDigits(), answer
    print 'Guess   ', [(numCorrect(p), p) for p in (p1, p2)]
    for i in range(numDigits()):
        c1, c2 = crossOver(p1, p2)
        population = [p1, p2, c1, c2]
        population.sort(key = lambda(x): -numCorrect(x))
        print i, [(numCorrect(p), p) for p in population[:2]]
        q1, q2 = population[0][:], population[1][:]
        if numCorrect(q1) == numDigits():
            print 'Solution', q1, numCorrect(q1)
            break
        if p1 == q1 and p2 == q2:
            q2 = mutate(q2)
        while q1 == q2:
            q1 = mutate(q1)
        p1, p2 = q1[:], q2[:]
    
if __name__ == '__main__':
    #simple()
    ga()
    
    
    