import sys, math, copy, decimal


def my_round(x, d):
    return str(decimal.Decimal(str(d*round(x/d)))) # d*round(x/d)
    
def show_mat(name, mat):
    print "------------", name, "------------"
    m = [[my_round(x, 0.1) for x in line] for line in mat]
    for line in m:
        print line
 
def sub_mat(mat, subt):
    "Subtract a 1D matrix subt from all lines of a 2D matrix mat"
    w = len(mat[0])
    h = len(mat)
    diff = copy.deepcopy(mat)
    for col in range(w):
        for row in range(h):
            diff[row][col] -= subt[col]
    return diff    
     
def get_mean(mat):
    w = len(mat[0])
    h = len(mat)
    total = [0 for n in range(w)]
    for col in range(w):
        for row in range(h):
            total[col] += mat[row][col]
        total[col] /= h
    return total
    
def get_var(mat):
    w = len(mat[0])
    h = len(mat)
    total = [0 for n in range(w)]
    for col in range(w):
        for row in range(h):
            total[col] += mat[row][col] * mat[row][col]
        total[col] /= h
    return total
    

def cov_mat(mat):
    w = len(mat[0])
    h = len(mat)
    prod = [[0 for i in range(w)] for j in range(w)]
    for col in range(w):
        for row in range(w):
            for i in range(h):
                prod[row][col] += mat[i][row] * mat[i][col]
            prod[row][col] /= h
    return prod
    
def corr_mat(cov, var):
    "Calculate corrletion maxtrix from covariance matrix and vector of stddev's"
    w = len(var)
    corr = copy.deepcopy(cov)
    for col in range(w):
        for row in range(w):
            corr[row][col] /= math.sqrt(var[col]*var[row])
    return corr    
                
def parse_line(line):
    'Read a comma separated line into an array of floats'
    return map(float, line.strip().split(','))
    #return [float(n) for n in line.strip().split(',')]
    
def read_csv(filename):
    "Read a CSV file into a 2D array"
  #  return map(parse_line, file(filename).read().strip().split('\n'))
    return map(lambda x: map(float, x.strip().split(',')) , file(filename).read().strip().split('\n'))
   # return [parse_line(line) for line in file(filename).read().strip().split('\n')]
    
def read_csv2(filename): return [[float(n) for n in line.strip().split(',')] for line in file(filename).read().strip().split('\n')]

def write_line(row):
    return ','.join(row)
    
def write_csv(filename, matrix):
   # lines = [','.join(map(str,row)) for row in matrix]
    '''
    lines = map(lambda row: ','.join(map(str,row)), matrix)
    all_lines = '\n'.join(lines) + '\n'
    file(filename, 'w').write(all_lines)
    '''
    file(filename, 'w').write('\n'.join(map(lambda row: ','.join(map(str,row)), matrix)) + '\n')
    
if __name__ == '__main__':
    if len(sys.argv) != 2:  
        sys.exit("Specicify a csv file")
    print "argv[1] = ", sys.argv[1]
    mat = read_csv2(sys.argv[1])
    show_mat("input", mat)  # print "mat = ", mat
    mean = get_mean(mat)
    show_mat("mean", [mean]) #[[line] for line in mean]) #  print "mean = ", mean
    centered = sub_mat(mat, mean)
    show_mat("centered", centered) # print "centered = ", centered
    var = get_var(centered)
    show_mat("var", [var])
    cov = cov_mat(centered)
    show_mat("cov", cov)#   print "cov = ", cov
    corr = corr_mat(cov, var)
    show_mat("corr", corr)
  # prod = mul_mat(mat)
  #  print "prod = ", prod
  #  print "mat = ", mat



