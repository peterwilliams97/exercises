'''
Created on 4/05/2010

@author: peter
'''
 
from math import *
    
def prod(v1, v2):
    "Returns dot product of vectors v1 and v2"
    return  sum(map(lambda x: x[0]*x[1], zip(v1,v2)))

def cross(v1, v2):
    "Returns outer product of vectors v1 and v2"
    return  [[x1*x2 for x1 in v1] for x2 in v2]

def sumCross(w1, w2):
    "Returns outer products summed over samples"
    assert(len(w1)==len(w2))
    for w in (w1, w2):
        for i in range(1, len(w)):
            assert(len(w[0]) == len(w[i]))
    s = cross(w1[0], w2[0])
    #showMat('s', s)
    for i in range(1, len(w1)):
        t = cross(w1[i], w2[i])
        for j in range(len(t)):
            for k in range(len(t[0])):
                s[j][k] = s[j][k] + t[j][k]
    return s

def energy (x, y, w): 
    assert(len(w) == len(y))
    assert(len(w[0])== len(x))
    p = [prod(x, v) for v in w] 
    s = prod(p,y)    
    return -s  

def minEnergy(w):  
    e = 0
    for v in w:
        for x in v:
            e += abs(x)
    return -e

def xfer(y, nety):
    if nety > 0: return 1
    if nety < 0: return -1
    return y

def prodCol(y, w, i):
    assert(len(y)==len(w))
    s = 0
    for j in range(len(y)):
        s += w[j][i] * y[j]   
    return s
      
def updateX (x, y, w):
     assert(len(w) == len(y))
     assert(len(w[0])== len(x))
     netx = [prodCol(y, w, i) for i in range(len(x))] 
     outx = [xfer(x[i], netx[i]) for i in range(len(x))]
     return (outx,y)
 
def updateY (x, y, w):
     assert(len(w) == len(y))
     assert(len(w[0])== len(x))
     nety = [prod(x, v) for v in w] 
     outy = [xfer(y[i], nety[i]) for i in range(len(y))]
     return (x,outy)
 
def  same(v1, v2):
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            return False
    return True

def findBest(x0, y0, w, y_first):
    assert(len(w) == len(y0))
    assert(len(w[0])== len(x0))
    x = x0
    y = y0
    while True:
        if y_first:
            x1, y1 = updateY(x, y, w)
            x2, y2 = updateX(x1, y1, w)
        else:
            x1, y1 = updateX(x, y, w)
            x2, y2 = updateY(x1, y1, w)
        if same(x, x2) and same(y, y2):
            return (x,y)
        x, y = (x2, y2)
    
    
def a2csv(array):
    "Convert array of objects to a comma separated string"
    return ','.join(map(str, array))
    
def aa2csv(array2):
    "Convert array of array of objects to lines of comma separated strings"
    return  '\n'.join(map(a2csv, array2))   

def showMat(name, array2):
    print name, '----------------------', len(array2), len(array2[0])
    print aa2csv(array2)
        
def l2(v1, v2):
    "Returns Euclidean distance between vectors v1 and v2"
    return sqrt(sum(map(lambda x: (x[0]-x[1])**2, zip(v1,v2))))

def doProblem(name, x0, y0, w0):
    print '*'
    print '********', name, '********'
    showMat('x0', [x0])
    showMat('y0', [y0])
    e = energy(x0, y0, w0)
    print 'energy(x0, y0, w0) =', e
    
    for y_first in (False, True):
        title = 'y first' if y_first else 'y first'
        print title, ' =============='
        xb, yb = findBest(x0, y0, w0, y_first)
        showMat('xb', [xb])
        showMat('yb', [yb])
        e = energy(xb, yb, w0)
        print 'energy(xb, yb, w0) =', e
        
        
def doProblem2(name, x0, w0):
    print '*'
    print '********', name, '********'
    showMat('x0', [x0])
    e = energy(x0, x0, w0)
    print 'energy(x0, y0, w0) =', e
    xb, _ = findBest(x0, x0, w0, False)
    showMat('xb', [xb])
    e = energy(xb, xb, w0)
    print 'energy(xb, yb, w0) =', e
        
def question1():
    x_in = [
        [1, -1, -1, 1, -1, 1, 1, -1, -1,  1],
        [1,  1,  1,-1, -1,-1, 1,  1, -1, -1 ]]
    y_in = [
        [1, -1, -1, -1, -1, 1],
        [1,  1,  1, 1, -1, -1]]
    
    showMat('x_in', x_in)
    showMat('y_in', y_in)
    w0 = sumCross(x_in, y_in)
 
    showMat('w0', w0)
    
    for i in [0, 1]:
        e = energy(x_in[i], y_in[i], w0)
        print 'energy(x_in['+ str(i) +'], y_in[' + str(i) + '], w0) =', e
    print 'min energy w0 =', minEnergy(w0)
    
    x0 = [-1, -1, -1, 1, -1, 1, 1, -1, -1, 1]
    y0 = [1, 1, 1, 1, -1, -1]
    doProblem('First', x0, y0, w0)
    
    x0 = [-1, 1, 1, -1, 1, 1, 1, -1, 1, -1]
    y0 = [-1, 1, -1, 1, -1, -1]
    doProblem('Second', x0, y0, w0)
    
    
def toPattern(v):
    return ''.join(map(lambda x: {0:'\219', 1:'\xb2'}[x],v)) 
   
def question2():
    "Auto-associative BAM"
    patterns = [
            [1, -1, -1,  1, -1,  1, -1, 1],
            [1,  1,  1, -1, -1, -1, -1, 1]]
    showMat('patterns', patterns)
    #print '0:', toPattern(patterns[0])
    #print '1:', toPattern(patterns[1])
    
    w0 = sumCross(patterns, patterns)
    showMat('w0', w0)
    
    x0 = [1, 1, 1, -1,  1, -1,  1, -1]
    x1 = [1, 1, 1,  1, -1,  1, -1,  1]
    print 'pattern =', len(patterns[0])
    print 'x0 =', len(x0)
    print 'x1 =', len(x1)
    
    doProblem2('Question 2a', x0, w0)
    doProblem2('Question 2b', x1, w0)
    
if __name__ == '__main__':
    if False:
        print 'Question 1 ++++++++++++++++++++++++++'
        question1()
    if True:
        print 'Question 2 ++++++++++++++++++++++++++'
        question2()
    
    
        
    
    