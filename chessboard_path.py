import math

''' A path is made along a chessboard in the following order.
    Given the distance traveled return the coordinates
    
   16 15 14 13 
    5  6  7 12 
    4  3  8 11
    1  2  9 10
    '''
    
def getCoords(distance):
    width = int(math.ceil(math.sqrt(distance)))
    outer = distance - (width - 1)**2
    side1 = min(width, outer)
    side2 = min(width, 2*width - outer)
    return width % 2 and (side1, side2) or (side2, side1)
    
def test(width):
    results = dict((getCoords(d), d) for d in range(1, width**2+1))
    for y in range(width, 0, -1):
        print ' '.join([str('%3s'%results[(x,y)]) for x in range(1, width+1)])
    
if __name__ == '__main__':
    test(10)
    



