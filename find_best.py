"""
http://docs.python.org/library/subprocess.html
"""
import shlex, subprocess, os, time, random, copy, csv

random.seed(0)

def dumpEnv():
	for param in os.environ.keys():
		print "%20s %s" % (param,os.environ[param])
		
def getAccuracy(fn):	
	"Extract the accuracy from stdout save in file called fn"
	results = file(fn, 'r').read().strip().split('\n')
	found_cv = False
	for line in results:
		if line.find('Stratified cross-validation') >= 0:
			found_cv = True
			#print 'found_cv'
		if found_cv:
			if line.find('Correctly Classified Instances') >= 0:
				terms = [s.strip() for s in line.split(' ') if not s == '']
				if False:
					for i, s in enumerate(terms):
						print i, ':', s
				accuracy = float(terms[4])
	return accuracy


	
def preprocess():
	"Add headers and pre-process the data. This needs to be done once"
	header = makeHeader()
	data = readCsvRaw(raw_name)
    
	hdata = [header] + data
	assert(len(hdata)==len(data)+1)
	validateMatrix(hdata)

	#swapMatrixColumn(data, 3, -1)
	writeCsv(headered_name, hdata)
	h2data = readCsvRaw(headered_name)
    
	replaceMissingValues(hdata)
	writeCsv(headered_name_pp, hdata)
	
# Locations of Weka files on my computer. This will need to be customized
# for each computer that runs this program	
if True:
	
	weka_root = os.environ['WEKA_ROOT']	
	weka_jar = os.path.join(weka_root, 'weka.jar')
	weka_mlp = 'weka.classifiers.functions.MultilayerPerceptron'
	mlp_opts = ' -H "a,2" '
 	
	
def runMLP(in_fn, out_fn):
	""" Run the Weka MultilayerPerceptron with options mlp_opts on the data in in_fn
		Write data to file out_fn
	"""
	if not os.path.exists(weka_jar):
		print 'Weka jar', weka_jar, ' does not exist'
		exit()
	if not os.path.exists(in_fn):
		print 'Input file', in_fn, ' does not exist'
		exit()
	out = open(out_fn, 'w')		
	cmd = 'java -cp ' + weka_jar  + ' ' + weka_mlp + mlp_opts + ' -t ' + in_fn
	print cmd
	print '------------------------ 1'
	t1 = time.time()
	p = subprocess.Popen(cmd, stdout=out)
	print '------------------------ 2'		
	p.wait()
	t2 = time.time()
	print '------------------------ 3'
	accuracy = getAccuracy(out_fn)
	dt = t2-t1
	return (accuracy, dt)


def testMatrixMLP(matrix, columns):
	c_x = columns + [-1]
	sub_matrix = [[row[i] for i in c_x] for row in matrix]
	temp_base = csv.makeTempPath('subset'+('%03d'%len(columns))+'_')
	temp_csv = temp_base + '.csv'
	temp_results = temp_base + '.results'
	csv.writeCsv(temp_csv, sub_matrix)
	test = True
	if test:
		accuracy,dt = 1.0/float(sum([abs(x-5) for x in columns])), 0.1
	else:
		accuracy,dt = runMLP(temp_csv, temp_results)
	return (accuracy, temp_csv, temp_results, dt)

def spinRouletteWheel(roulette):
	"""	Find the roulette wheel winner
		roulette is a list of 2-tuples
			1st val is index
			2nd val is probabily of the index
		Return an index with probability proportional to one specified
	"""
	total = float(sum([x[1] for x in roulette]))
	v = random.randrange(total)
	#print 'v', v, 'total', total
	base = 0.0
	for x in roulette:
		top = base + x[1]
		#print x[0], [base, top], ';',
		if v < top:
			#print 'result =', x[0], 'v =', v
			return x[0]
		base = top

def testRouletteWheel():
	num_bins = 4
	roulette = [(i,i+1) for i in range(num_bins)]
	print 'roulette', roulette
	counts = [0 for i in range(num_bins)]
	for j in range(10000):
		k = spinRouletteWheel(roulette)
		counts[k] = counts[k] + 1
	print 'roulette', roulette
	print 'counts', counts
	ratios = [float(counts[i])/float(roulette[i][1]) for i in range(num_bins)]
	print 'ratios', ratios
	total = sum(ratios)
	print 'splits', [x/total for x in ratios]
		
	
def crossOver(c1, c2):
	"Swap half the elements in c1 and c2"
	assert(len(c1) == len(c2))
	n = len(c1)
	shuffle_list = random.sample(range(n), n/2)
	d1, d2 = c1[:], c2[:]
	# Find elements that are not in both lists
	d1.sort(key = lambda x: x not in d2)
	d2.sort(key = lambda x: x not in d1)
	for i1,x in enumerate(d1):
		if x in d2:
			break
	for i2,x in enumerate(d2):
		if x in d1:
			break
	m = min(i1, i2)  #
	shuffle_list = random.sample(range(m), min(n/2,m))
	for i in shuffle_list:
		d1[i], d2[i] = d2[i], d1[i]
	d1.sort()
	d2.sort()
	return (d1, d2)	
	
def findBestOfSize(matrix, num_subset, num_trials):
	"Find best result on num_subset columns of matrix entries"
	num_attribs = len(matrix[0])-1  # last column is category
	print 'findBestOfSize', len(matrix), num_attribs, 'num_subset', num_subset, 'num_trials', num_trials
	num_tried = 0
	results = []
	csv_results_name = csv.makeCsvPath('subset'+('%03d'%num_subset))
	csv_results = file(csv_results_name, 'w')
	
	def doOneRun(columns):
		accuracy, temp_csv, temp_results,duration = testMatrixMLP(matrix,columns)
		r = {'num':num_subset, 'accuracy':accuracy, 'columns':columns,'csv':temp_csv, 'results':temp_results, 'duration':duration, 'index':num_tried}
		results.append(r)
		print num_subset, num_tried, accuracy, columns, temp_csv, temp_results, duration, 'seconds'
		for i in range(min(3,len(results))):
			print '  ', results[i]
		summary = [num_subset, num_tried, accuracy, '"' + str(columns) + '"', temp_csv, temp_results, duration]
		csv_line = ','.join([str(e) for e in summary])
		csv_results.write(csv_line + '\n')
		csv_results.flush()
		return num_tried + 1
		
	for i in range(0, num_attribs, num_subset):
		if i + num_subset > num_attribs:
			i = num_attribs - num_subset 
		columns = [i+j for j in range(num_subset)]
		num_tried = doOneRun(columns)
		results.sort(key = lambda(r): -r['accuracy'])
		
	mating_size = num_tried	
	count = 0	
	index = 0
	results.sort(key = lambda(r): -r['accuracy'])
	best_result = copy.deepcopy(results[0])
	while num_tried <= num_trials:
		roulette = [(i,1.0/(1.01-r['accuracy'])) for i,r in enumerate(results)]
		index = (index + 1) % mating_size
		second_index = index if count % 3 == 0 else 0
		c1,c2 = crossOver(results[0]['columns'], results[second_index]['columns'])
		num_tried = doOneRun(c1)
		num_tried = doOneRun(c2)
		if count % 10 == 0:
			 mutation = random.sample(range(num_attribs), num_subset)
			 num_tried = doOneRun(mutation)
        results.sort(key = lambda(r): -r['accuracy'])
        #
        # !@#$ Need to terminate on convergence
        #
        if results[0]['accuracy'] == best_result['accuracy']:
        	print 'Converged !!' 
        best_result = copy.deepcopy(results[0])
       
	
if __name__ == '__main__':
	
	if False:
		dumpEnv()
		
	if False:  # Do this once. Then use headered_name_pp
		preprocess()
	
	if False:
		out_fn = 'tmp.out.txt'
		in_fn = csv.headered_name_pca
		runMLP(in_fn, out_fn)
		
	if True:
		testRouletteWheel()
		
	if False:
		matrix = csv.readCsvRaw(csv.headered_name_pca_corr)
		num_attributes = len(matrix[0])-1
		if True:
			num_subset = 5
			num_trials = max(100, num_attributes*2)
			findBestOfSize(matrix, num_subset, num_trials)
		if False:
			for num_subset in range(5, num_attributes, 5):
				#
				# !@#$ Should use the results of previous runs to select important attributes
				#      Simple resorting based on best previous subset
				#      order=[]
				#      for r in results:
				#         for i in r.subset:
				#			if not i in order:
				#				order.append(i)
				#
				#
				num_trials = max(100, num_attributes*2)
				findBestOfSize(matrix, num_subset, num_trials)
		
	if False:
		out = open(out_fn, 'w')
		err = open(err_fn, 'w')
		print args
		print '------------------------ 1'
		p = subprocess.Popen(args, stdout=out, stderr=err)
		print '------------------------ 2xx'		
		p.wait()
		print '------------------------ 3'
					
					
					
					
					
		
		
	
