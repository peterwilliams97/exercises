'''
Simple perceptron solver
'''

import sys, math, copy


def read_csv(filename):
    'Read a CSV file into a 2D array'
    return map(lambda x: map(float, x.strip().split(',')) , file(filename).read().strip().split('\n'))

def write_csv(filename, matrix):
    'Write a @D to a CSV file'
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
        self._data = read_csv(fn)
        self._width = len(self._data[0])
        self._height = len(self._data)
        
    def write(self, filename):
        write_csv(filename, self._data)
        
    def describe(self):
        description = ''
        for row in self._data:
            for value in row:
                description += str(value) + ', '
            description += '\n'
        return description.strip()

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
        
        
def solve(x_name, y_name, w_name):
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
    if len(sys.argv) != 4:  
        sys.exit("Specicify X and Y csv file names")
    print "X = argv[1] = ", sys.argv[1]
    print "Y = argv[2] = ", sys.argv[2]
    print "W = argv[2] = ", sys.argv[3]
    solve(sys.argv[1], sys.argv[2], sys.argv[3])
        
 


