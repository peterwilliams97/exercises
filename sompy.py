from __future__ import division
"""

http://www.cis.hut.fi/projects/somtoolbox/theory/somalgorithm.shtml
http://www.cis.hut.fi/research/som_lvq_pak.shtml

Initialize nodes with PCA cpts p0, p1, p2 in 0 
    0 <= x < W
    0 <= y < H
    fx = x/(W-1) fy = y(H-1)
    node[y,x] = (1-fy-fx)p0 + fy*p1 + fx*p2
 => node[0,0] = p0
    node[H,0] = p1
    node[0,W] = p2
    node[H,W] = -p0 + p1 + p2

Kyle Dickerson
kyle.dickerson@gmail.com
Jan 15, 2008

Self-organizing map using scipy
This code is licensed and released under the GNU GPL

This code uses a square grid rather than hexagonal grid, as scipy allows for fast square grid computation.
I designed sompy for speed, so attempting to read the code may not be very intuitive.
If you're trying to learn how SOMs work, I would suggest starting with Paras Chopras SOMPython code:
 http://www.paraschopra.com/sourcecode/SOM/index.php
It has a more intuitive structure for those unfamiliar with scipy, however it is much slower.

If you do use this code for something, please let me know, I'd like to know if has been useful to anyone.

    FV = feature vector
    
"""
from random import *
from math import *
import sys
import scipy

seed(0)

def myRnd(x):
    return float(int(x*100.0))/100.0

def rnd(x):
    return str(myRnd(x)) 

def getLength(v):
    """ Returns length of vector v"""
    return sqrt(sum([x**2 for x in v]))

def getNormalizedArray(num_elements):
    """ Returns a normalized array with num_elements elements """
    l = 0.0
    while l < float(num_elements)*0.1:
        v = [random() for i in range(num_elements)]
        l = getLength(v)
    return [x/l for x in v]

class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[getNormalizedArray(FV_size) for x in range(width)] for y in range(height)])
        self.node_matches = [[ [] for x in range(width)] for y in range(height)]
        self.unmatched = []
    
    def train(self, iterations=1000, input_train_vector=[[]]):
        """  train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
             train vector may be a list, will be converted to a list of scipy arrays
             FVi is a feature vector
        """
        raw_train_vector = [scipy.array(v) for v in input_train_vector]  
        train_vector_lengths = [getLength(v) for v in raw_train_vector]
        max_length = max(train_vector_lengths)
        threshold = max_length/100.0
        n = len(raw_train_vector)
        train_vector = [raw_train_vector[i]/train_vector_lengths[i] for i in range(n) if train_vector_lengths[i] > threshold]   
            
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        
        print 'training:', 'height', self.height, 'width', self.width, 'radius', self.radius, 'learning rate', self.learning_rate
        
        for i in range(1, iterations+1):
            delta_nodes.fill(0)
            radius_decaying = self.radius*exp(-1.0*i/time_constant)
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying = self.learning_rate * exp(-1.0*i/time_constant)
            if i % int((iterations+99)/100) == 0 or i == iterations:
                sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations) 
                                 + ", rad dec = " + rnd(radius_decaying) + ", rad div = " + rnd(rad_div_val) + ", lr decay = " + rnd(learning_rate_decaying))
            
            for j in range(len(train_vector)):
                best = self.best_match(train_vector[j])
                for loc in self.find_neighborhood(best, radius_decaying):
                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    inf_lrd = influence * learning_rate_decaying
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
                    
            self.nodes += delta_nodes
        sys.stdout.write('\n')
        
        print '----------- Nodes --------------'
        for y in range(self.height):
            for x in range(self.width):
                print y, ',', x, self.nodes[y,x]
        # Find the input vectors matching the normalized vectors and place them in the appropriate 
        # cluster bins
        j = 0
        for i in range(len(input_train_vector)):
            if train_vector_lengths[i] > threshold:
                y,x = self.best_match(train_vector[j])
                print 'best match', (i, j), ',', (y,  x), train_vector_lengths[i], input_train_vector[i], train_vector[j], self.nodes[y,x]
                self.node_matches[y][x].append(input_train_vector[i])
                j += 1
            else:
                self.unmatched.append(input_train_vector[i])
        print '----------- Clusters --------------'
        for y in range(self.height):
            for x in range(self.width):
                if len(self.node_matches[y][x]) > 0:
                    print 'Cluster', (y, x), len(self.node_matches[y][x]), 'elements', self.nodes[y,x]
                    for m in self.node_matches[y][x]:
                        print '  ', m
        print 'Unmatched:', len(self.unmatched), 'elements'
        for m in self.unmatched:
            print '  ', m         
            
    
    def find_neighborhood(self, pt, dist):
        """ Returns a list of points which live within 'dist' of 'pt'
            Uses the Chessboard distance
            pt is (row, column)
        """
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors
    
    def best_match(self, target_FV):
        """ Returns y,x location of node that best matches target_FV,
            Uses Euclidean distance
            target_FV is a scipy array
        """
        loc = scipy.argmin((((self.nodes - target_FV)**2).sum(axis=2))**0.5)
        x = loc
        y = 0
        while x >= self.width:
            x -= self.width
            y += 1
        return (y, x)

    def FV_distance(self, FV_1, FV_2):
        """ Returns the Euclidean distance between two Feature Vectors
            FV_1, FV_2 are scipy arrays
        """
        return (sum((FV_1 - FV_2)**2))**0.5

if __name__ == "__main__":
    print 'Initialization...'
    colors = [ [0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    colors = [[0, 0,   0], 
              [0, 20, 20],      [30, 0, 30],
              [0, 120, 120],   [130, 0, 130],
              [0, 220, 220],   [230, 0, 230],
              [0, 20, 21],      [30, 0, 31],
              [0, 20, 22],      [30, 0, 32],
              [0, 20, 23],      [30, 0, 33],
              [0, 20, 25],      [30, 0, 35],
              [0, 20, 40],   [30, 0, 60],
              [0, 40, 20],   [60, 0, 30],
              [100, 100, 0], [20, 20, 0],  [20, 20, 0], [200, 200, 0],
              [0, 0, 255], [0, 255, 0], [255, 0, 0],
              [0, 0, 200], [0, 201, 0], [202, 0, 0],
              [0, 0, 120], [0, 150, 0], [160, 0, 0],
              [0, 0,  55], [0,  55, 0], [ 55, 0, 0]  ]
  
    
    width = 12 # 32
    height = 12 # 32
    color_som = SOM(width,height,3,0.05)
    print 'Training colors...'
    color_som.train(2000, colors)
    try:
        from PIL import Image
        print 'Saving Image: sompy_test_colors.png...'
        img = Image.new('RGB', (width, height))
        for y in range(height):
            for x in range(width):
                img.putpixel((x,y), (int(color_som.nodes[y,x,0]), int(color_som.nodes[y,x,1]), int(color_som.nodes[y,x,2])))
        img = img.resize((width*10, height*10),Image.NEAREST)
        img.save('sompy_test_colors.png')
    except:
        print 'Error saving the image, do you have PIL (Python Imaging Library) installed?'