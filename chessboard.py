"""
Problem:
    
    A grid is traversed in the following order
    
        5 6 7
        4 3 8
        1 2 9
    
    Given the distance travelled, return the current x and y coordinates
    
    Write a program to read the distance from the command line and write
    its x and y coordinates to stdout
    
    Your program should work on distances of up to 1,000,000
     
Created on 27/10/2010

@author: peter
"""
import  sys, math

def getXY(distance):
    """ Given the distance travelled along a grid in the order described above, return the x,y coordinates """
    width = int(math.ceil(math.sqrt(distance)))
    outside = distance - (width - 1)**2
    side1 = min(width, outside)
    side2 = width - (outside - side1)
    return (side1,side2) if width % 2 else (side2,side1) 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python', sys.argv[0],'<distance>'
        exit()

    distance = int(sys.argv[1])
    if distance < 1:
        print 'distance must be a positive integer'
        exit()

    x,y = getXY(distance)
    print x,y

