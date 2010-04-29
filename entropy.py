'''

                        
Created on 28/04/2010

@author: peter
'''
import copy, decimal
from math import *
    
def my_round(x, d):
    return str(decimal.Decimal(str(d*round(x/d)))) # d*round(x/d)
    
def my_r(x):
    return my_round(x, 0.01) 
    
def clean(m):
    return [my_round(x, 0.01) for x in p]

def entropy(p):
    assert(abs(sum(p) - 1.0) < 1e-6) 
    return -sum(map(lambda x: x* log(x,2), p))
    

def ff(i):
    return 1 - (i%2)*2
    
def test(dm, p):
    e =  entropy(p)
    n = len(p)
    print n, my_r(dm), ')', clean(p), ':', my_r(e), my_r(2.0 **e), my_r((2.0 **e)/n)

            
if __name__ == '__main__':
    p1 = [0.1, 0.9]
    p2 = [0.5, 0.5]
    n = 10
    p3 = [1.0/n for i in range(n)]
    
    for p in [p1, p2, p3]:
        test(0, p)
     
    for n in range(1, 11):
        p = [1.0/n for i in range(n)]
        test(0, p)
     
      
    for d in (0.1, 0.2, 0.5):
        for n in range(2, 9, 2):
            m = 1.0/n
            dm = d*m
            p = [m + ff(i)*dm  for i in range(n)]
            test(dm, p)
    