"""
http://docs.python.org/library/subprocess.html
"""
import shlex, subprocess, os, time, random, copy, shutil, csv, pca

# Set True for testing
is_testing = False

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
	# mlp_opts = ' -H "a,2" -x 4'
 	mlp_opts = ' -H "a" -x 4'
	
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
	"Run MLP on attributes with index in columns"
	c_x = columns + [-1]      # include outcome
	sub_matrix = [[row[i] for i in c_x] for row in matrix]
	temp_base = csv.makeTempPath('subset'+('%03d'%len(columns))+'_')
	temp_csv = temp_base + '.csv'
	temp_results = temp_base + '.results'
	if is_testing:
		num_attributes = len(matrix[0]) - 1
		accuracy,dt = 1.0/float(sum([abs(x-num_attributes/2) for x in columns])), 0.1
	else:
		csv.writeCsv(temp_csv, sub_matrix)
		accuracy,dt = runMLP(temp_csv, temp_results)
	return (accuracy, temp_csv, temp_results, dt)

def makeRankings(roulette):
	"Rankings for use in roulette"
	ranks = copy.deepcopy(roulette)
	ranks.sort(key = lambda x: -x['val'])
	ratio = 0.5
	for i,x in enumerate(ranks):
		x['weight'] = ratio**(i+1)
	ranks.sort(key = lambda x: -x['weight'])
	return ranks
		
	
def spinRouletteWheel(roulette_in):
	"""	Find the roulette wheel winner
		roulette is a list of 2-tuples
			1st val is index
			2nd val is probability of the index
		Return an index with probability proportional to one specified
	"""
	show = False
	roulette = makeRankings(roulette_in)
	if show:
		print '--------------------'
		print 'roulette', roulette
	total = float(sum([x['weight'] for x in roulette]))
	v = total*random.random()
	#print 'v', v, 'total', total
	base = 0.0
	for x in roulette:
		top = base + float(x['weight'])
		#print x[0], [base, top], ';',
		if v <= top:
			if show:
				print '--------------------'
				print 'roulette winner', x, v, total
			return x['idx']
		base = top
	# If we get here something is wrong, so dump out state
	print '------------------- spinRouletteWheel -----------------'
	print 'v', v, 'total', total
	print 'roulette', roulette
	print 'ranges', 
	base = 0.0
	for x in roulette:
		print base,
		base = base + float(x['weight'])
	print base
	
def spinRouletteWheelTwice(roulette):
	while True:
		i1 = spinRouletteWheel(roulette)
		i2 = spinRouletteWheel(roulette)	
		if i2 != i1:
			return (i1,i2)

def myRound(x):
	return float(int(round(x*100.0)))/100.0

def testRouletteWheel():
	num_bins = 10
	roulette = [{'idx':i, 'val':num_bins-i} for i in range(num_bins)]
	print 'roulette', roulette
	counts = [0 for i in range(num_bins)]
	for j in range(10000):
		k = spinRouletteWheel(roulette)
		counts[k] = counts[k] + 1
	print 'roulette', roulette
	print 'counts', counts
	total = sum(counts)
	print 'splits', [myRound(float(x)/total) for x in counts]
	
def testRouletteWheelTwice():
	num_bins = 10
	roulette = [{'idx':i, 'val':num_bins-i} for i in range(num_bins)]
	print 'roulette', roulette
	counts = [0 for i in range(num_bins)]
	for j in range(10000):
		k1,k2 = spinRouletteWheelTwice(roulette)
		counts[k1] = counts[k1] + 1
		counts[k2] = counts[k2] + 1
	print 'roulette', roulette
	print 'counts', counts
	total = sum(counts)
	print 'splits', [myRound(float(x)/total) for x in counts]	
		
def mutate(columns, number_indexes):
	"Apply a random mutation to a list of columns"
	d = columns[:]
	while True:
		n = random.randint(0, number_indexes-1)
		if not n in d:
			d[random.randint(0, len(d)-1)] = n
			return d

def testMutate():
	columns = [x for x in range(5)]
	mutation0 = columns[:]
	for i in range(10000):
		mutation1 = mutate(mutation0, 100)
		if mutation1 == columns:
			break
		mutation0 = mutation1[:]
		
def crossOver(c1, c2):
	"Swap half the elements in c1 and c2"
	assert(len(c1) == len(c2))
	n = len(c1)
	#shuffle_list = random.sample(range(n), n/2)
	d1, d2 = c1[:], c2[:]
	# Find elements that are not in both lists
	d1.sort(key = lambda x: x in d2)
	d2.sort(key = lambda x: x in d1)
	#print 'xover', (d1,d2)
	for i1,x in enumerate(d1):
		if x in d2:
			#print x, 'in', d2
			break
	for i2,x in enumerate(d2):
		if x in d1:
			#print x, 'in', d1
			break
	#print 'xover', (i1,i2)
	m = min(i1, i2)  #
	shuffle_list = random.sample(range(m), min(n/2,m))
	for i in shuffle_list:
		d1[i], d2[i] = d2[i], d1[i]
	d1.sort()
	d2.sort()
	return (d1, d2)	

def testCrossOver():
	num_cpts = 5
	c1 = [i for i in range(num_cpts)]
	c2 = [i+num_cpts for i in range(num_cpts)]
	for i in range(10):
		d1,d2 = crossOver(c1,c1)
		print 'crossOver', (c1,c1), '=>', (d1,d2)
	for i in range(10):
		d1,d2 = crossOver(c1,c2)
		print 'crossOver', (c1,c2), '=>', (d1,d2)
	
def findBestOfSize(matrix, num_subset, num_trials, csv_results_name):
	"Find best result on num_subset columns of matrix entries"
	num_attribs = len(matrix[0])-1  # last column is category
	print 'findBestOfSize', len(matrix), num_attribs, 'num_subset', num_subset, 'num_trials', num_trials
	num_tried = 0
	results = []
	
	csv_results = file(csv_results_name, 'w')
	
	def doOneRun(columns, show):
		accuracy, temp_csv, temp_results,duration = testMatrixMLP(matrix,columns)
		columns.sort()
		r = {'num':num_subset, 'accuracy':accuracy, 'columns':columns,'csv':temp_csv, 'results':temp_results, 'duration':duration, 'index':num_tried}
		results.append(r)
		results.sort(key = lambda r: -r['accuracy'])
		if show:
			print num_tried, ':', num_subset, accuracy, len(results), columns, int(duration), 'seconds'
			for i in range(min(3,len(results))):
				rr = results[i]
				print '    ',i, ':', rr['accuracy'],rr['columns'], int(rr['duration'])
		summary = [num_subset, num_tried, accuracy, '"' + str(columns) + '"', temp_csv, temp_results, duration]
		csv_line = ','.join([str(e) for e in summary])
		csv_results.write(csv_line + '\n')
		csv_results.flush()
		return num_tried + 1
		
	for i in range(0, num_attribs, num_subset):
		if i + num_subset > num_attribs:
			i = num_attribs - num_subset 
		columns = [i+j for j in range(num_subset)]
		num_tried = doOneRun(columns, True)
				
	# start the Genetic Algorithm
	ga_base = num_tried
	history_of_best = []
		
	while num_tried <= num_trials:
		roulette = [{'idx':i, 'val':r['accuracy']} for i,r in enumerate(results)]
		existing_columns = [r['columns'] for r in results]
		if not random.randrange(20) == 1:
			found = False
			for j in range(1000):
				i1,i2 = spinRouletteWheelTwice(roulette)
				c1,c2 = crossOver(results[i1]['columns'], results[i2]['columns'])
				if not c1 in existing_columns and not c2 in existing_columns and not c1==c2:
					found = True
					break
			if not found:
				print 'Converged after', num_tried - ga_base, 'GA rounds'
				break
			print 'cross over', i1, i2, '-', j+1, 'tries'
			num_tried = doOneRun(c1, True)
			num_tried = doOneRun(c2, True)
		else:
			for j in range(1000):
				i1 = spinRouletteWheel(roulette)
				c1 = mutate(results[i1]['columns'], num_attributes)
				if not c1 in existing_columns:
					break
			print 'mutation', i1,'took', '-', j+1, 'tries'
			num_tried = doOneRun(c1, True)
		# Test for convergence
		convergence_number = 10
		history_of_best.append(results[0]['accuracy'])
		if len(history_of_best) >= convergence_number:
			converged = True
			for i in range(1,convergence_number):
				if not history_of_best[i] == history_of_best[0]:
					converged = False
					break
			if converged:
				print 'Converged after', num_tried - ga_base, 'GA rounds'
				break
		
	return results
	
def orderByResults(results, num_attributes):
	order = []
	for r in results:
		for i in r['columns']:
			if not i in order:
				order.append(i)	
	for i in range(num_attributes):
		if not i in order:
			order.append(i) 
	assert(len(order) == num_attributes)
	print 'orderByResults', num_attributes, order
	return order

if __name__ == '__main__':
	
	if False:
		dumpEnv()
		
	if False:  # Do this once. Then use headered_name_pp
		preprocess()
	
	if False:
		out_fn = 'tmp.out.txt'
		in_fn = csv.headered_name_pca
		runMLP(in_fn, out_fn)
		
	if False:
		testRouletteWheel()
		testRouletteWheelTwice()
		testMutate()
		testCrossOver()
		
	if True:
		matrix = csv.readCsvRaw(csv.headered_name_pca_corr)
		num_attributes = len(matrix[0])-1
		if False:
			num_subset = 5
			num_trials = max(100, num_attributes*2)
			results = findBestOfSize(matrix, num_subset, num_trials)
			order = orderByResults(results,num_attributes)
		if True:
			sort_order = [i for i in range(num_attributes)]
			for num_subset in range(5, num_attributes, 5):
				num_trials = max(100, num_attributes*2)
				csv_matrix_name  = csv.makeCsvPath('subset.matrix' +('%03d'%num_subset))
				csv_results_name = csv.makeCsvPath('subset.results'+('%03d'%num_subset))
				csv_best_name    = csv.makeCsvPath('subset.best'   +('%03d'%num_subset))
				csv_summary_name  = csv.makeCsvPath('subset.summary'+('%03d'%num_subset))
			
				ordered_matrix = pca.reorderMatrix(matrix, sort_order)
				csv.writeCsv(csv_matrix_name, ordered_matrix)
				
				results = findBestOfSize(ordered_matrix, num_subset, num_trials, csv_summary_name)
				
				sort_order = orderByResults(results,num_attributes)
				#c_x = results[0].columns + [-1]      # include outcome
				#sub_matrix = [[row[i] for i in c_x] for row in ordered_matrix]
				#csv.writeCsv(csv_best_name,sub_matrix, )
				if not is_testing:
					shutil.copyfile(results[0]['csv'],csv_best_name)
					shutil.copyfile(results[0]['results'],csv_results_name)
		
	if False:
		out = open(out_fn, 'w')
		err = open(err_fn, 'w')
		print args
		print '------------------------ 1'
		p = subprocess.Popen(args, stdout=out, stderr=err)
		print '------------------------ 2xx'		
		p.wait()
		print '------------------------ 3'
					
					
					
					
					
		
		
	
