'''
Simple perceptron solver

See http://www.ibm.com/developerworks/library/l-neural/
'''

import sys, math, copy, random

random.seed(0)

def readCsv(filename):
    'Read a CSV file into a 2D array. 2D array is a list of lists of float, one list of float per CSV line'
    return map(lambda x: map(float, x.strip().split(',')) , file(filename).read().strip().split('\n'))

def writeCsv(filename, data):
    'Write a 2D array to a CSV file. 2D array is a list of lists of float, one list of float per CSV line'
    file(filename, 'w').write('\n'.join(map(lambda row: ','.join(map(str,row)), data)) + '\n')
    
class Matrix:
    '''2D Matrix class following conventions of http://en.wikipedia.org/wiki/Matrix_multiplication'''
    
    def __init__(self, height = 1, width = 1, value = 0, func = False):
        self._width = width
        self._height = height
        if func:
            self._data = [[func(y,x) for x in range(self._width)] for y in range(self._height)] 
        else:
            self._data = [[value for x in range(width)] for y in range(height)]
     
    def get(self, y, x):
        return self._data[y][x]
        
    def put(self, y, x, value):
        self._data[y][x] = value
        
    def getRow(self, r):
        return Matrix(height = 1, width = self._width, func = lambda y,x: self._data[r][x])
    
    def getCol(self, c):
        return Matrix(height = self._height, width = 1, func = lambda y,x: self._data[y][c])
              
    def isZero(self):
        for row in self._data:
            for value in row:
                if value != 0:
                    return False
        return True
                        
    def read(self, fn):
        'Read matrix from a CSV file. Inverse of write()'
        self._data = readCsv(fn)
        self._width = len(self._data[0])
        self._height = len(self._data)
        
    def write(self, filename):
        'Write matrix to a CSV file. Inverse of read()'
        writeCsv(filename, self._data)
        
    def describe(self):
        'String representation of matrix'
        return '\n'.join(map(lambda row: ', '.join(map(str,row)), self._data))
               
# 
# Operations on matrices
#
def transpose(A):
    'Returns transpose of A'
    return Matrix(height = A._width, width = A._height, func = lambda y,x: A._data[x][y])
    
def add(A, B):
    'Returns A+B'
    assert(A._width == B._width and A._height == B._height)
    return Matrix(height = A._height, width = A._width, func = lambda y,x: A._data[y][x] + B._data[y][x])
    
def sub(A, B):
    'Returns A-B'
    assert(A._width == B._width and A._height == B._height)
    return Matrix(height = A._height, width = A._width, func = lambda y,x: A._data[y][x] - B._data[y][x])

def sumProds(a, b):
    'Return a[i]*b[i] summed over i'
    assert(len(a)==len(b))
    return sum(map(lambda z: z[0]*z[1], zip(a,b)))
                                                      
def mul(A, B):
    'Return A*B'
    assert(A._width == B._height)
    return Matrix(A._height, B._width, func = lambda y,x: sumProds([A._data[y][i] for i in range(A._width)], [B._data[i][x] for i in range(B._height)]))
  
def mapMat(f, A):
    'Applies f(z) to all elements z = _data[y][x] of matrix A and returns resulting matrix'
    return Matrix(A._height, A._width, func = lambda y,x: f(A._data[y][x]))
    
def booleanize(n):
    'Returns 1 if n > 0, 0 otherwise'
    return {False:0, True:1}[n>0]
        
def solve(X, Y, max_rounds, decay):
    "Returns W,matches, epoch where W: X*W'=Y is caluculated with a Perceptron solver"
    assert(X._height == Y._height)
    assert(max_rounds >= 2)
    assert(decay <= 1.0)
    W = Matrix(height=1, width = X._width, value = 1.0/X._width)
    epoch = X._height
    multiplier = 1.0
    for round in range(max_rounds):
        matches = 0
        for r in range(epoch):
            row = X.getRow(r)
            Ycalc = mapMat(booleanize, mul(row, transpose(W)))
            E = sub(Y.getRow(r), Ycalc)
            if E.isZero():
                matches = matches + 1
            else:
                W = add(W, mul(mul(E, Matrix(1,1,multiplier)), row))
                print '** ', W.describe(), ' - ', row.describe()
        if matches == epoch:
             break
    return (W, matches, epoch)

def solveForFiles(x_name, y_name, w_name):
    ''' x_name and y_name are csv files containing matrices X and Y
        This function finds W: X*W'=Y by a Perceptron solver'''
    X = Matrix()
    Y = Matrix()
    X.read(x_name)
    Y.read(y_name)
    print X.describe()
    print Y.describe()
    W, matches, epoch = solve(X, Y, 100, 0.99) 
    print 'matches =', matches, 'of', epoch, 'W ='
    print W.describe()
    print "X*W'" 
    print mul(X, transpose(W)).describe() 
    W.write(w_name)
  
def makeTestData(number_points, w):
    'Create test matrices X,Y for a weights vector w and number_points points'
    print 'w =', w
    corners = ((1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1))
    calcY = lambda x: w[0]*x[0]+w[1]*x[1]+w[2]*x[2]
    yvals = map(calcY, corners)
    ymin = min(yvals)
    ymax = max(yvals)
    print 'ymin ymax =', ymin, ymax
    assert(ymin < ymax)
    xmin = (-ymin-1.0)/(ymax-ymin)
    xmax = xmin + 2.0/(ymax - ymin)
    print 'xmin xmax =', xmin, xmax
    assert(xmin < xmax)
    acorners = ((1, xmin, xmin), (1,xmin, xmax), (1, xmax, xmin), (1, xmax, xmax))
    print 'adjusted Y', map(lambda c: str(calcY(c)), acorners)
    
    X = Matrix(number_points, 3)
    Y = Matrix(number_points, 1)
    for r in range(number_points):
        flipflop = (r % 2 == 0)
        while True:
            x = (1, random.uniform(xmin, xmax), random.uniform(xmin, xmax)) 
            y = booleanize(calcY(x))
            if y == flipflop:
                break
        for j in (0, 1, 2) : 
            X.put(r, j, x[j])
        Y.put(r, 0, y)
    return (X, Y)
 
def runTest(number_points, w, rounds):   
    'Run a test for a weights vector w,  number_points points and rounds calibration rounds'
    X, Y = makeTestData(number_points, w)
    if number_points < 20:
        print X.describe()
        print Y.describe()
        print '-------------------------------------'
    W, matches, epoch = solve(X, Y, rounds, 0.9999) 
    print 'w =', w, ', number_points=', number_points
    print 'matches =', matches, 'of', epoch, 'rounds =', rounds, 'W ='
    print W.describe()
    if number_points < 20:
        print '-------------------------------------'
        print "X*W'" 
        print mul(X, transpose(W)).describe()                      
                            
if __name__ == '__main__':
    if True:
        if len(sys.argv) != 4:  
            sys.exit("Specicify X and Y csv file names")
        print "X = argv[1] = ", sys.argv[1]
        print "Y = argv[2] = ", sys.argv[2]
        print "W = argv[2] = ", sys.argv[3]
        solveForFiles(sys.argv[1], sys.argv[2], sys.argv[3])
    if False:
        number_points = 5
        rounds = 4 * number_points
        runTest(number_points, (0, 1, 1), rounds)
       

        
 


