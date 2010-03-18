'''
Simple perceptron solver
'''

import sys, math, copy, random


def readCsv(filename):
    'Read a CSV file into a 2D array. 2D array is a list of lists of float, one list of float per CSV line'
    return map(lambda x: map(float, x.strip().split(',')) , file(filename).read().strip().split('\n'))

def writeCsv(filename, matrix):
    'Write a @D to a CSV file. 2D array is a list of lists of float, one list of float per CSV line'
    file(filename, 'w').write('\n'.join(map(lambda row: ','.join(map(str,row)), matrix)) + '\n')
    
class Matrix:
    '''2D Matrix class following conventions of http://en.wikipedia.org/wiki/Matrix_multiplication'''
    
    def __init__(self, height = 1, width = 1, value = 0):
        self._width = width
        self._height = height
        self._data = [[value for x in range(width)] for y in range(height)]
      
    def get(self, y, x):
        return self._data[y][x]
        
    def put(self, y, x, value):
        self._data[y][x] = value
        
    def getRow(self, r):
        row = Matrix(width = self._width)
        row._data[0] = copy.deepcopy(self._data[r])
        return row
    
    def getCol(self, c):
        col = Matrix(height = self._height)
        for r in range(col._height):
            col._data[r][0] = self._data[c][r]
        return col
        
    def isZero(self):
        iszero = True
        for row in self._data:
            for value in row:
                if value != 0:
                    iszero = False
                    break
        return iszero
        
    def applyFunc(self, func):
        self._data = map(lambda row: map(func, row), self._data)
                
    def read(self, fn):
        self._data = readCsv(fn)
        self._width = len(self._data[0])
        self._height = len(self._data)
        
    def write(self, filename):
        writeCsv(filename, self._data)
        
    def describe(self):
        return '\n'.join(map(lambda row: ', '.join(map(str,row)), self._data))
               

def transpose(A):
    T = Matrix(height = A._width, width = A._height)
    for y in range(A._height):
        for x in range(A._width):
            T._data[x][y] = A._data[y][x]
    return T
    
def add(A,B):
    assert(A._width == B._width and A._height == B._height)
    C = Matrix(A._height, A._width, 0)
    for y in range(C._height):
        for x in range(C._width):
            C._data[y][x] = A._data[y][x] + B._data[y][x]
    return C
    
def sub(A,B):
    assert(A._width == B._width and A._height == B._height)
    C = Matrix(A._height, A._width, 0)
    for y in range(C._height):
        for x in range(C._width):
            C._data[y][x] = A._data[y][x] - B._data[y][x]
    return C
                            
def mul(A, B):
    assert(A._width == B._height)
    C = Matrix(A._height, B._width, 0)
    for y in range(C._height):
        for x in range(C._width):
            for i in range(A._width):
                C._data[y][x] += A._data[y][i]*B._data[i][x]
    return C

def mapMat(func, A):
    B = copy.deepcopy(A)
    B.applyFunc(func)
    return B
    
def booleanize(n):
    if n > 0:
        return 1
    else:
        return 0
        
def solve(X, Y, max_rounds, decay):
    "Returns W: X*W'=Y by a Perceptron solver"
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
              
def solveForFiles0(x_name, y_name, w_name):
    ''' x_name and y_name are csv files containing matrices X and Y
        This function finds W: X*W'=Y by a Perceptron solver'''
    
    X = Matrix()
    Y = Matrix()
    X.read(x_name)
    Y.read(y_name)
    assert(X._height == Y._height)
    
    W = Matrix(height=1, width = X._width, value = 1.0/X._width)
    print X.describe()
    print Y.describe()
    print W.describe()
    
    W.write(w_name)
    
    epoch = X._height
    print 'epoch', epoch
    decay = 0.99
    multiplier = 1.0
    
    for round in range(10):
        print 'round =', round, '============================='
        matches = 0
        for r in range(epoch):
            print 'r =', r, ' -----------------------', multiplier
            row = X.getRow(r)
            Wt = transpose(W)
            Yr = mul(row, Wt)
            #print 'Yr', Yr.describe()
            Yc = mapMat(booleanize, Yr)
            E = sub(Y.getRow(r), Yc)
            Em = mul(E, Matrix(1,1,multiplier))
            W = add(W, mul(Em, row))
            if E.isZero():
                matches = matches + 1
            W.write(w_name)
            print 'E', E.describe()
            print 'W', W.describe()
        if matches == epoch:
            print 'MATCH! after', round, 'rounds'
            print 'W', W.describe()
            print "X*W'" 
            print mul(X, transpose(W)).describe() 
            break
        print 'matches', matches, 'of', epoch
        multiplier = multiplier * decay
   
                            
if __name__ == '__main__':
    if False:
        if len(sys.argv) != 4:  
            sys.exit("Specicify X and Y csv file names")
        print "X = argv[1] = ", sys.argv[1]
        print "Y = argv[2] = ", sys.argv[2]
        print "W = argv[2] = ", sys.argv[3]
        solveForFiles(sys.argv[1], sys.argv[2], sys.argv[3])
    if True:
        n = 4
        rounds = 5 * n
        w = (0, 1, 1)
        X, Y = makeTestData(n, w)
        if n < 20:
            print X.describe()
            print Y.describe()
            print '-------------------------------------'
        W, matches, epoch = solve(X, Y, rounds, 0.9999) 
        print 'w =', w, ', n=', n
        print 'matches =', matches, 'of', epoch, 'rounds =', rounds, 'W ='
        print W.describe()
        if n < 20:
            print '-------------------------------------'
            print "X*W'" 
            print mul(X, transpose(W)).describe() 

        
 


