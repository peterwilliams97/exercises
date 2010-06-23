from __future__ import division
"""
Main
http://www.ensmp.fr/~moutarde/FAQs/Neuron-faq/FAQ.html#A_Kohonen

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

    Based on SOM by 
        Kyle Dickerson
        kyle.dickerson@gmail.com
        Jan 15, 2008

   FV = feature vector
    
"""
from random import *
from math import *
import sys, scipy, pca

seed(0)

def getLength(v):
    """ Returns length of vector v"""
    return sqrt(sum([x**2 for x in v]))

def myRnd(x):
    return float((round(x*1000.0)))/1000.0

def rnd(x):
    return str(myRnd(x)) 

def roundVector(v):
    return '[' + ','.join(['%+.2f' % x for x in v]) + ']'
   # return [myRnd(x) for x in v]   
         
def printNodes(nodes, height, width):
    print '----------- Nodes ', (height, width)
    for y in range(height):
        for x in range(width):
            print y, ',', x, roundVector(nodes[y,x]), myRnd(getLength(nodes[y,x]))
            
def printVectors(name, vectors):
    print '----------- Vectors ', name, len(vectors)
    for v in vectors:
        print roundVector(v), myRnd(getLength(v))

def getNormalizedArray(num_elements):
    """ Returns a normalized array with num_elements elements """
    l = 0.0
    while l < float(num_elements)*0.1:
        v = [random() for i in range(num_elements)]
        l = getLength(v)
    return [x/l for x in v]

def getInitNodes(vectors, height, width):
    """ Return starting nodes for a SOM with given training vectors
        vectors: array of training vectors
        h: height of SOM
        w: width of SOM
    """
    pca_cpts = pca.getPcaCpts(vectors, 3)
    assert(len(pca_cpts[0]) == len(vectors[0]))
    printVectors('pca cpts', pca_cpts)
    def getNode(y, x):
        """ node[0,0] = pca_cpts[0]
            node[h,0] = pca_cpts[1]
            node[0,w] = pca_cpts[2]
            node[h,w] = -pca_cpts[0] 
        """
        if False:
            fx = x/(width-1) 
            fy = y/(height-1)
            v = (1.0-fy-fx)*pca_cpts[0] + fy*(1.0-fx)*pca_cpts[1] + fx*(1.0-fy)*pca_cpts[1]
        else:
            fx = 1.0 - 2.0*x/(width-1) 
            fy = 1.0 - 2.0*y/(height-1) 
            z = (fx**2 + fy**2)**0.5
            if fx == 0.0 and abs(fy) < 1.0:
                fz = (1-fy)**2
            elif fy == 0.0 and abs(fx) < 1.0:
                fz = -(1-fx)**2
            else:
                fz = 0.0
            #fz = (1+z)**-4.0 if abs < 0.2 else 0.0
            v =  fy*pca_cpts[0] + fx*pca_cpts[1] + fz*pca_cpts[2]
        l = getLength(v)
        if l < 0.01:
            print 'PCA mixture too short', v, l
            getNormalizedArray(len(pca_cpts[0]))
        return [x/l for x in v]
    return scipy.array([[getNode(y,x) for x in range(width)] for y in range(height)]) 

def maxNode(nodes, height, width):
    """ Return node with largest length or None if no nodes have non-zero length"""
    biggest = 0.0
    max_node = None
    for y in range(height):
        for x in range(width):
            l = getLength(nodes[y,x])
            if l > biggest:
                biggest = l
                max_node = nodes[y,x]
    return max_node
           
           
    
class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        assert(height >= width)
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
        for v in input_train_vector:
            assert(len(v) == self.FV_size)
        #normalized_train_vectors = pca.normalizeMatrix(input_train_vector) 
              
        raw_train_vector = [scipy.array(v) for v in input_train_vector]  
        train_vector_lengths = [getLength(v) for v in raw_train_vector]
        max_length = max(train_vector_lengths)
        threshold = max_length/100.0
        n = len(raw_train_vector)
        train_vector = [raw_train_vector[i]/train_vector_lengths[i] for i in range(n) if train_vector_lengths[i] > threshold]   
        printVectors('train_vector', train_vector)
        
        self.nodes = getInitNodes(train_vector, self.height, self.width)   
        printNodes(self.nodes, self.height, self.width)
            
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0.0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        
        print 'training:', 'height', self.height, 'width', self.width, 'radius', self.radius, 'learning rate', self.learning_rate
        
        for i in range(1, iterations+1):
            delta_nodes.fill(0.0)
           # delta_nodes = scipy.array([[[0.0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
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
                    delta = inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
                    delta_nodes[loc[0],loc[1]] = delta_nodes[loc[0],loc[1]] + delta
                    # print delta_nodes[loc[0],loc[1]], delta # !@#$
                    #print '*', inf_lrd, train_vector[j], self.nodes[loc[0],loc[1]], train_vector[j]-self.nodes[loc[0],loc[1]]  # !@#$
                    #if getLength(delta_nodes[loc[0],loc[1]]) > 0.0:  # !@#$
                    #    print '!', delta_nodes[loc[0],loc[1]]
                    
            self.nodes += delta_nodes
            
            # !@#$ Nodes with that are far from data keep growing in size
            #      How can this be??
            if False:
                max_delta_node = maxNode(delta_nodes, self.height, self.width)
                if not max_delta_node == None:   # !@#$
                    if getLength(max_delta_node) > 1000.0:
                        print 'max delta node =', max_delta_node
        sys.stdout.write('\n')
        
        printNodes(self.nodes, self.height, self.width)
        
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
    colors0 = [ [0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    colors1 = [[0, 0,   0], 
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
    colors2 = [[0, 20, 20],      [30, 0, 30],
              [0, 220, 220],   [230, 0, 230],
              [0, 20, 40],   [30, 0, 60],
              [0, 40, 20],   [60, 0, 30],
              [100, 100, 0], [20, 20, 0],  [20, 20, 0], [200, 200, 0],
              [0, 0, 255], [0, 255, 0], [255, 0, 0]]
    
    colors3 = [
               
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
              
              [255, 20, 20],      [30, 255, 30],
              [255, 120, 120],   [130, 255, 130],
              [255, 220, 220],   [230, 255, 230],
              [255, 20, 21],      [30, 255, 31],
              [255, 20, 22],      [30, 255, 32],
              [255, 20, 23],      [30, 255, 33],
              [255, 20, 25],      [30, 255, 35],
              [255, 20, 40],   [30, 255, 60],
              [255, 40, 20],   [60, 255, 30],
              [100, 100, 255], [20, 20, 255],  [20, 20, 255], [200, 200, 255],
              
              [ 10, 20,  30], [ 20, 40,  60], [ 40, 80,  120], 
              [ 11, 21,  31], [ 21, 41,  60], [ 40, 81,  121], 
              
              [ 10, 20,  10], [ 20, 40,  20], [ 40, 80,  40], 
              [ 11, 21,  11], [ 21, 41,  20], [ 40, 81,  41], 
               
              [ 30, 0,  30], 
               [130, 0, 130],
              [230, 0, 230],
              [0,  20,  20],  
              [0, 120, 120],  
              [0, 220, 220],   
               [ 10, 10, 0],
               [110,110, 0],
              [210,210, 0],
               [ 10, 0, 0],
               [110,0, 0],
              [210,0, 0]
              ]
  
    colors = colors0 + colors1 + colors2 + colors3
    colors = colors3
    
    width = 5 # 32
    height = 5 # 32
    color_som = SOM(height,width,len(colors[0]),0.05)
    print 'Training colors...'
    color_som.train(1500, colors)
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