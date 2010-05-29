'''
Naive Bayes Classifier 
    
Created on 8/05/2010

@author: peter
'''
 
from math import *

weka_data =  '''        
pregnant
  mean              3.4234   4.9795
  std. dev.         3.0166   3.6827
  weight sum           500      268
  precision         1.0625   1.0625

plasma_glucose
  mean            109.9541 141.2581
  std. dev.        26.1114  31.8728
  weight sum           500      268
  precision         1.4741   1.4741

blood_pressure
  mean             68.1397   70.718
  std. dev.        17.9834  21.4094
  weight sum           500      268
  precision         2.6522   2.6522

triceps_skin
  mean             19.8356  22.2824
  std. dev.        14.8974  17.6992
  weight sum           500      268
  precision           1.98     1.98

insulin
  mean             68.8507 100.2812
  std. dev.         98.828 138.4883
  weight sum           500      268
  precision          4.573    4.573

bmi
  mean             30.3009  35.1475
  std. dev.         7.6833   7.2537
  weight sum           500      268
  precision         0.2717   0.2717

pedigree
  mean              0.4297   0.5504
  std. dev.         0.2986   0.3715
  weight sum           500      268
  precision         0.0045   0.0045

age
  mean             31.2494  37.0808
  std. dev.        11.6059  10.9146
  weight sum           500      268
  precision         1.1765   1.1765   
'''  
    
new_case = '''
pregnant  7
plasma_glucose  110
blood_pressure  80
bmi  40
age  35
pedigree  0.5
'''    
    
def gaussian(x, u, a):
    "Returns guassian probability density of x for mean u and std dev a"
    v = (x-u)/a
    return  exp(-(v**2)/2.0)/sqrt(2.0)/pi/a


def rnd(x):
    "Returns x rounded to nearest multiple of 1/100"
    return round(x*100.0)/100.0

def rnd3(x):
    "Returns x rounded to nearest multiple of 1/1000"
    return round(x*1000.0)/1000.0

def stats(x, var, g, i):
    "Returns string with stats on value x of variable var class i"
    u = var['mean'][i]
    a = var['std. dev.'][i]
    v = (x-u)/a
    return '%6.2f, %5.2f, %5.2f, %5.3f' % (rnd(u), rnd(a), rnd(v), rnd3(g[i]))

def classRatio(x, var, key):
    '''Returns probability ratio of 2 Weka distributions at x. 
       var is variable in distribution, key is name of varible'''
    u = var['mean']
    a = var['std. dev.']
    g = [gaussian(x, u[i], a[i]) for i in range(2)]
    print '%16s: %6.2f, %28s, %28s => %5.2f' % (key, x, stats(x, var, g, 0), stats(x, var, g, 1), rnd(g[1]/g[0]))
    return g[1]/g[0]

def classify(cal_set, point):
    "Classify point based on cal_set. Return True/False"
    print 'cal_set =', cal_set.keys()
    print '  point =', point.keys()
    assert(point.keys() <= cal_set.keys())
    log_ratio = 0.0
    print
    print '%16s: %6s, %28s, %28s => %5s' % ('key', 'x', 'no', 'yes', 'yes/no')
    for key in point.keys(): 
        log_ratio += log(classRatio(point[key], cal_set[key], key))
    print 'log_ratio =', rnd3(log_ratio)
    print '    ratio =', rnd(exp(log_ratio))
    return log_ratio > 0.0
        
                       
def parseWeka(data):
    lines = data.strip().split('\n')
    cal_set = dict()
    for l in lines:
        if len(l) > 0 and l[0] not in ' \t\n\r':
            key = l
            d = dict()
            cal_set[key] = d
        elif len(l) > 0 and l[0] in ' \t':
            # print 'l =', l
            s = [m for m in l.strip().split(' ') if len(m) > 0]
            if len(s) > 3:
                ll = ' '.join(s[:2])
                s = [ll] + s[2:]
            #print 's =', s
            assert(len(s) == 3)
            d[s[0]] = (float(s[1]), float(s[2]))
        else:
            d = None
    return cal_set

def parsePoint(data):
    lines = [l.strip() for l in data.strip().split('\n')]
    point = dict()
    for l in lines:
        s = [m for m in l.strip().split(' ') if len(m) > 0]
        if len(s) > 2:
            ll = ' '.join(s[:2])
            s = [ll] + s[2:]
        assert(len(s) == 2)
        point[s[0]] = float(s[1])
    return point

            
if __name__ == '__main__':
    cal_set = parseWeka(weka_data)
    point = parsePoint(new_case)
    classification = classify(cal_set, point)
    print 'Class =', classification
  
