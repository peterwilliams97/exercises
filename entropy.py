"""

                        
Created on 28/04/2010

@author: peter
"""
import copy, decimal
from math import *
    
def my_round(x, d):
    "Returns string representation of x rounded to nearest multiple of d"
    return str(decimal.Decimal(str(d*round(x/d)))) # d*round(x/d)
    
def my_r(x):
    "Returns string representation of x rounded to nearest multiple of 0.01"
    return my_round(x, 0.01) 
    
def clean(p):
    "Returns array string representation of elements of p rounded to nearest multiple of 0.01"
    return [my_round(x, 0.01) for x in p]

epsilon = 1e-6

def entropy(p):
    "Returns entropy of a probability distribution. p = array of probs"
    for x in p:
        assert(0.0 <= x and x <= 1.0)
    assert(abs(sum(p) - 1.0) < epsilon) 
    return -sum(map(lambda x: x* log(x,2), p))
  
def entropy2(arr):
     s = float(sum(arr))
     p = [float(a)/s for a in arr]
     #print 'p =', p
     return entropy(p)    

def ff(i):
    return 1 - (i%2)*2
    
def test(dm, p):
    e =  entropy(p)
    n = len(p)
    print n, my_r(dm), ') probs=', clean(p), ': entropy =', my_r(e), ', 2.0**e =', my_r(2.0 **e), ', 2.0**e/n =',my_r((2.0 **e)/n)
   
def test1():    
    p0 = [0.5, 0.5]
    p1 = [0.1, 0.9]
    p2 = [0.01, 0.99]
    n = 10
    p3 = [1.0/n for i in range(n)]
    
    for p in [p0, p1, p2, p3]:
        test(0, p)
     
    for n in range(1, 11):
        p = [1.0/n for i in range(n)]
        test(0, p)
     
    num = 5
    for n in range(2, 9, 2):
        for i in range(num):
            d = (float(i)/float(num))**2
            m = 1.0/n
            dm = d*m
            p = [m + ff(i)*dm  for i in range(n)]
            test(dm, p)
    
def test2():
    no = False
    yes = True
    vals = {'(-inf-99.5]': (no, 197, 16),
            '(99.5-127.5]': (no, 264, 88),
            '(127.5-154.5]': (no, 110, 104),
            '(154.5-inf)': (yes, 122, 24)}
    
    vals_arr = [vals[k] for k in vals.keys()]
    no_tot = sum([v[2 if v[0] else 1] for v in vals_arr])
    yes_tot = sum([v[1 if v[0] else 2] for v in vals_arr])
    tot = no_tot + yes_tot
    print 'no =', no_tot, ' + yes =', yes_tot, ' =', no_tot + yes_tot  
    
    dist_all = (no_tot, yes_tot)
    print 'entropy all =', entropy2(dist_all)
    dist_split = [(v[1],v[2]) for v in vals_arr]
    dist_entropies = [entropy2(v) for v in dist_split]
    print 'dist_entropies =', dist_entropies
    dist_fracs = [float(sum(v))/tot for v in dist_split]
    print 'dist_fracs =', dist_fracs
    entropy_split = sum([v[0]*v[1] for v in zip(dist_entropies, dist_fracs)])
    print 'entropy split=', entropy_split
    
    for i in range(len(vals_arr)):
        vv = vals_arr[i]
        v = (vv[2],vv[1]) if vv[0] else (vv[1],vv[2])
        e = dist_entropies[i]
        f = dist_fracs[i]
        print v[0], ',', v[1], ',', e, ',', f
        
if __name__ == '__main__':
    test1()