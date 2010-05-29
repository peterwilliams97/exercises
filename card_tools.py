'''
Created on 18/05/2010

@author: peter
'''
from math import *
import copy

def stripBlanks(s):
    parts = s.strip().split(' ')
    return ''.join(parts)
    
def bitMask64(n, m, val):
    "Return a bit mask with bits n-m set 0<=n<=m<=31"
    assert(0<=n)
    assert(n<=m)
    assert(m<=63)
    bits = 0
    for i in range(n,m+1):
        bits = bits | 2**i
    r = (bits & val) / (2 ** n)
   # print '  ',  n, m, hex(bits),(2 ** n),val,r, 
    return r
      
def test(ss, closest):
    n = int(ss,16)
    n2 = ~n
    c = int(closest,16)
    diff = c-value
    if abs(n-value) < abs(c-value):
        closest = copy.deepcopy(ss)
        diff = n-value
    if abs(n2-value) < abs(c-value):
        closest = copy.deepcopy(ss) 
        diff = n2-value
    if n2 == value:
        print '*** !!'   
    return diff, closest

          
def findMatch1(value, s, closest):    
    r = s[::-1]        
    print s, r, len(s)/2, 'bytes'
    print int(s, 16), int(r, 16)
    diff, closest = test(r, closest) 
    for i in range(0,len(s)+1, 2):
        for j in range(i+2, len(s)+1, 2):
            #print i,j, ':',
            tf = s[i:j+1]
            tr = r[i:j+1]
            #print tf, '=', int(tf, 16),
            #print tr, '=', int(tr, 16), len(tf)/2, 'bytes'
            diff, closest = test(tf, closest) 
            diff, closest = test(tr, closest) 
            if int(tf, 16) == value:
                #print i, j, tf, value
                break
            if int(tr, 16) == value:
                #print i, j, tr, value
                break
    
    print 'closest', closest, len(closest)/2.0, 'bytes' 
    print '  ', int(closest, 16)
    print '  ', value
    print '  ',  diff, log(abs(diff), 2)
    
    return closest, diff

def test2(ss, closest, n, m):
    v = int(ss,16)
    v1 = bitMask64(n, m, v)
    v2 = ~v1
    c = int(closest,16)
    diff = c-value
    if abs(v1-value) < abs(c-value):
        closest = copy.deepcopy(ss)
        diff = v1-value
    if abs(v2-value) < abs(c-value):
        closest = copy.deepcopy(ss) 
        diff = v2-value  
    return diff, closest

def findMatch2(value, s, closest): 
    r = s[::-1]        
    diff, closest = test(r, closest) 
    print s, r, len(s)/2, 'bytes'
    print int(s, 16), int(r, 16)
    n_best = -1
    m_best = -1
    for m in range(64):
        for n in range(m+1):
            diff_1, closest = test2(s, closest, n, m) 
            if abs(diff_1) < abs(diff):
                n_best = n
                m_best = m
                diff = diff_1
            diff_1, closest = test2(r, closest, n, m) 
            if abs(diff_1) < abs(diff):
                n_best = n
                m_best = m
                diff = diff_1
            if diff == 0:
                print 'Match!'
                break
    print 'closest', closest, len(closest)/2.0, 'bytes, n =', 64-n_best, 'm =', 64-m_best
    v = int(closest,16)
    v1 = bitMask64(n_best, m_best, v)
    print '  ', v1
    print '  ', value
    print '  ',  diff, log(abs(diff), 2)
    return closest, diff
                           
def baseTest(value, s):
    print 'baseTest', value, s
    closest_in = s
    closest_in, diff = findMatch1(value, s, closest_in)
    if diff == 0:
        print 'Done !!!'
    is_pow2 = False
    if not diff == 0: 
        l2 = log(abs(diff),2)
        is_pow2 = abs(floor(l2) - l2) < 1.0e-3
    if is_pow2:
        print 'Power of 2 difference!!!'
    return diff, is_pow2

def reverseBytes32(s): 
    "Reverse byte order in each 32 bit word"
    n = len(s)
    assert(n%4 == 0)
    a = [c for c in s]
    for i in range(0, n-7, 8):   
        for j in range(0, 2, 1):
            c0 = a[i+2*j]
            c1 = a[i+2*j+1]
            a[i+2*j]  = a[i+2*(3-j)]
            a[i+2*j+1]= a[i+2*(3-j)+1]
            a[i+2*(3-j)] = c0
            a[i+2*(3-j)+1] = c1
    return ''.join(a) 
    
            
def mainTest(value, s_in):
    print value
    print s_in
    s = stripBlanks(s_in)
    diff, is_pow2 = baseTest(value, s)
    
    if False:
        for i in range(256):
            if is_pow2 or diff == 0:
                break
            p = hex(i)[2:]
            print p
            s_1 =  s + p
            diff_1, is_pow2 = baseTest(value, s_1)
            if abs(diff_1) < abs(diff):
                diff = diff_1
                print '******************'
            print 'Best diff', diff
        
    if len(s) % 4 != 0:        s_1 = s + '00'
    else:       s_1 = s 

    s_2 = reverseBytes32(s_1)
    print s, s[:8], s[8:]
    print s_1, s_1[:8], s_1[8:]
    print s_2, s_2[:8], s_2[8:]        
    diff, is_pow2 = baseTest(value, s_2)
        
    if True:
        findMatch2(value, s, s)
        if len(s) % 4 != 0:        s_1 = s + '00'
        else:       s_1 = s 
        
        s_2 = reverseBytes32(s_1)
        findMatch2(value, s_2, s_2)
        
    if False:
        v = int(s,16)
        v = 512
        print v
        for m in range(10):
            for n in range(m+1):
                v1 = bitMask64(n, m, v)
                print ',  %2d %2d %d %d' % (n,m,v,v1)
    print '========================================'   
                
if __name__ == '__main__':
    cases = [(      26, '3B 05 00 00 12 00 34'),    # 26*2 = 0x34
             (   22469, '3B 06 00 00 A1 4A AF 8A'),  # 1-17 right most bits
             (   34339, '3B 05 00 03 6F 0C 46'),     # 34339 * 2 = 10C46
             (     174, '3B 05 00 00 2E 01 5C'),      # 0x015C/2 = 174, site 0x2E
             (     175, '3B 05 00 00 2E 01 5F'),      # 0x015F/2 = 175, site 0x2E
             (     282, '3B 05 00 00 06 81 1A'),      # 282 = 0x11A site 0x1A x 4 = 0x68
             (     283, '3B 05 00 00 06 81 1B'),      # 283 = 0x11B site 0x1A x 4 = 0x68
             
             (2015, '3A03934E'),
             ( 101, '640065'),     # # 101 = 0x65
             ( 102, '640066'),     # # 102 = 0x66
             (1681, '1E21A186'),
 
             ]
    c = cases[1]
    value = c[0]
    mainTest(value, c[1])   
    
   
    m = 63
    n = m - 16
    s = stripBlanks(c[1])
    v1 = bitMask64(n, m, int(s,16))
    print '%2d %2d' % (n,m), value, hex(v1)             