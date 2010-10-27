"""
Problem:
    
    A grid is traversed in the following order
    
        5 6 7
        4 3 8
        1 2 9
    
    Given the distance travelled, give the current x and y coordinates
    
    Write your program to read the distance from the command line and write
    it x and y coordinates to stdout
    
    Your program should work on arbitrarily large integers
     
Created on 27/10/2010

@author: peter
"""
import  sys, math

def getXY(dist):
    width = int(math.ceil(math.sqrt(dist)))
    outside = dist - (width - 1)**2
    side1 = min(width, outside)
    side2 = width - (outside - side1)
    return (side1,side2) if width % 2 else (side2,side1) 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python chessboard <distance>'
        exit()
    x,y = getXY(int(sys.argv[1]))
    print x,y

