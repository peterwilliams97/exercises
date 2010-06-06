"""
A set of tools for running  the Weka MLP function and analyzing its output
This class is 
weka.classifiers.functions.MultilayerPerceptron

"""
import shlex, subprocess, os, time, random, copy, shutil, csv, pca

# Set True for testing
is_testing = False

random.seed(0)

def dumpEnv():
	for param in os.environ.keys():
		print "%20s %s" % (param,os.environ[param])
		
def checkExists(title, filename):
	"Check that filename exists"	
	if not os.path.exists(filename):
		print title, filename, 'does not exist'
		exit()
				
def preprocess(raw_name, headered_name, headered_name_pp):
	"""	Add headers and pre-process the raw Kushmerick  data. 
		This needs to be done once.
		- raw_name is the Kushmerick data that is input
		- headered_name is the name of CSV file with headers that is created
		- headered_name_pp is the named a file created by preprocessing header name that is created
	"""
	print 'preprocess', raw_name, '=>', headered_name, '=>', headered_name_pp
	header = csv.makeHeader()
	data = csv.readCsvRaw(raw_name)
    
	hdata = [header] + data
	assert(len(hdata)==len(data)+1)
	csv.validateMatrix(hdata)

	#swapMatrixColumn(data, 3, -1)
	csv.writeCsv(headered_name, hdata)
	h2data = csv.readCsvRaw(headered_name)
    
	csv.replaceMissingValues(hdata)
	csv.writeCsv(headered_name_pp, hdata)
		
def getAccuracy(filename):	
	"Extract the accuracy from stdout save in file called filename"
	results = file(filename, 'r').read().strip().split('\n')
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

def getPredictions(filename):	
	"Extract Weka prediction from results stored in filename"
	checkExists('Predictions file', filename)
	prediction_file = file(filename, 'r').read().strip().split('\n')
	found_header = False
	results = []
	for line in prediction_file:
		if found_header:
			terms = [s.strip() for s in line.split(' ') if not s == '']
			inst = int(terms[0])
			actual = terms[1]
			predicted = terms[2]
			if len(terms) > 4:
				error = True
				prediction = float(terms[4])
			else:
				error = False
				prediction = float(terms[3])
			r = {'inst':inst, 'actual':actual, 'predicted':predicted, 'error':error, 'prediction':prediction}
			if False:
				if r['error']:
					print r
			assert(r['error'] == (r['actual'] != r['predicted']))
			results.append(r)
		elif line.find('error prediction') >= 0:
			found_header = True
	return results


	
# Locations of Weka files on my computer. This will need to be customized
# for each computer that runs this program	

if True:
	weka_root = os.environ['WEKA_ROOT']	
	weka_jar = os.path.join(weka_root, 'weka.jar')
	weka_mlp = 'weka.classifiers.functions.MultilayerPerceptron'
	# mlp_opts = ' -H "a,2" -x 4'
 	mlp_opts = '-H "a" -x 4'
 	# http://old.nabble.com/WEKA-CLI:-Problems-with-flags-td23670055.html
 	weka_cost = 'weka.classifiers.meta.CostSensitiveClassifier -cost-matrix "[0.0 1.0; 10.0 0.0]" -S 1 -W '
	
def outnameToModelname(out_fn):	
	return out_fn + '.model'
	

def runWekaClass(out_fn, weka_cmds):
	""" Run the Weka class weka_cmds
		Write data to file out_fn
		See http://docs.python.org/library/subprocess.html
	"""
	checkExists('Weka jar',  weka_jar) 
	out = open(out_fn, 'w')		
	cmd = 'java -cp ' + weka_jar  + ' ' + weka_cmds
	print cmd
	t1 = time.time()
	p = subprocess.Popen(cmd, stdout=out)	
	p.wait()
	t2 = time.time()
	return t2-t1		
	
def runMLPTrain(data_filename, results_filename, opts = mlp_opts):
	""" Run the Weka MultilayerPerceptron with options mlp_opts on the data in data_filename
		Write data to file out_fn
	"""
	checkExists('Data file', data_filename) 
	duration = runWekaClass(results_filename, weka_mlp + ' ' + opts + ' -t ' + data_filename + ' -d ' + outnameToModelname(results_filename)) 
	accuracy = getAccuracy(results_filename)
	return (accuracy, duration)

def runMLPPredict(data_filename, model_filename, predictions_filename):
	""" Run the Weka MultilayerPerceptron with model model_filename on
		data_filename.
		Write data to predictions_filename
	"""
	checkExists('Data file', data_filename) 
	checkExists('Model file', model_filename) 
	duration = runWekaClass(predictions_filename, weka_mlp + ' -p 0 -T ' + data_filename + ' -l ' + model_filename) 
	#accuracy = getAccuracy(predictions_filename)
	return duration

def testMatrixMLP(matrix, columns, opts = mlp_opts):
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
		accuracy,dt = runMLPTrain(temp_csv, temp_results, opts)
	return (accuracy, temp_csv, temp_results, dt)

def mapToWekaOptions(options_map):
	"""	Convert a map with keys and values corresponding to Weka options 
		to a Weka options string
		e.g. {'M':0.5 'L':0.3, 'H':7 'x':5} => '-m 0.5 -L -0.3 -H 7 -x 5'
		"""
	option_strings = ['-' + k + ' ' + str(options_map[k]) for k in options_map.keys()]
	return ' '.join(option_strings)

def spaceSeparatedLine(arr):
	return ' '.join(map(str,arr))

def makeWekaOptions(learning_rate, momentum, number_hidden, num_cv, costs = None):
	"Return Weka option string for specified values"
	options_map = {'M':momentum, 'L':learning_rate, 'H':number_hidden, 'x':num_cv}
	if costs:
		cost_matrix_path = csv.makeTempPath('cost') + '.cost'
		options_map['m'] = cost_matrix_path
		cost_matrix = ['%% Rows	Columns',
					   spaceSeparatedLine([2,2]),
					   '%% Matrix elements',
					   spaceSeparatedLine([0.0,  costs['True']]),
					   spaceSeparatedLine([costs['False'], 0.0])]	
		file(cost_matrix_path, 'w').write('\n'.join(cost_matrix))
	return mapToWekaOptions(options_map)
	

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
			print num_subset, num_tried, ':',  accuracy, len(results), columns, int(duration), 'seconds'
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

def selectAttibutesGA():
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
			csv_results_name = csv.makePath('subset.results'+('%03d'%num_subset))
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

def testBySize(incrementing_hidden):
	"Test MLP results on matrix by number of left side columns"
	
	start_num_columns = 30 
	delta_num_columns = 10
	opts = '-M 0.5 -L 0.3 -x 4 -H '
	num_hidden = 13
		
	csv_matrix_name = csv.makeCsvPath('subset.matrix035')	
	base_name = 'number.attributes'
	if incrementing_hidden:
		base_name = base_name + '.inc'
	csv_results_name = csv.makePath(base_name + '.results')
	csv_summary_name = csv.makeCsvPath(base_name + '.summary')
	csv_best_name    = csv.makeCsvPath(base_name + '.best')
	
	matrix  = csv.readCsvRaw(csv_matrix_name)
	num_attribs = len(matrix[0])-1  # last column is category
	print 'testBySize', len(matrix), start_num_columns, delta_num_columns, len(matrix[0])
	
	best_accuracy = 0.0
	summary = []
	csv_summary = file(csv_summary_name, 'w')
	
	for num_columns in range(start_num_columns, len(matrix[0]), delta_num_columns):
		columns = [i for i in range(num_columns)]
		if incrementing_hidden:
			num_hidden = int(float(num_columns)*13.0/30.0)
		accuracy, temp_csv, temp_results, duration = testMatrixMLP(matrix, columns, opts + str(num_hidden))
		r = {'num':num_columns, 'accuracy':accuracy, 'csv':temp_csv, 'results':temp_results, 'duration':duration}
		summary.append(r)
		summary.sort(key = lambda r: -r['accuracy'])
		if True:
			print num_columns, ':',  accuracy, len(results), int(duration), 'seconds'
			for i in range(min(3,len(results))):
				rr = results[i]
				print '    ',i, ':', rr['accuracy'], rr['num'], int(rr['duration'])
		summary_row = [num_columns, accuracy, duration, temp_csv, temp_results]
		csv_line = ','.join([str(e) for e in summary_row])
		csv_summary.write(csv_line + '\n')
		csv_summary.flush()
		if accuracy > best_accuracy:
			best_accuracy = accuracy
			shutil.copyfile(temp_csv, csv_best_name)
			shutil.copyfile(temp_results, csv_results_name)
		
	return results

def testByNumberHidden(csv_matrix_name, output_basename, num_columns, num_cv = 4):
	"""Test MLP results on matrix by number of neurons in hidden layer
		num_columns is number of leftmost columns of matrix to test
		num_cv is the number of cross-validation rounds
	"""
	
	start_num_hidden = min(15, num_columns-1) 
	delta_num_hidden = 10
	
	results_name = csv.makePath(output_basename + '.results')
	model_name   = csv.makePath(output_basename + '.model')
	csv_summary_name = csv.makeCsvPath(output_basename + '.summary')
	csv_best_name    = csv.makeCsvPath(output_basename + '.best')
	
	matrix  = csv.readCsvRaw(csv_matrix_name)
	num_attribs = len(matrix[0])-1  # last column is category
	print 'testByNumberHidden', len(matrix), start_num_hidden, delta_num_hidden, num_columns
	
	best_accuracy = 0.0
	results = []
	csv_summary = file(csv_summary_name, 'w')
	
	for num_hidden in range(start_num_hidden, num_columns, delta_num_hidden):
		columns = [i for i in range(num_columns)]
		accuracy, temp_csv, temp_results, duration = testMatrixMLP(matrix, columns, makeWekaOptions(0.3, 0.5, num_hidden, num_cv))
		r = {'num':num_hidden, 'accuracy':accuracy, 'csv':temp_csv, 'results':temp_results, 'duration':duration}
		results.append(r)
		results.sort(key = lambda r: -r['accuracy'])
		if True:
			print num_hidden, ':',  accuracy, len(results), int(duration), 'seconds'
			for i in range(min(5,len(results))):
				rr = results[i]
				print '    ',i, ':', rr['accuracy'], rr['num'], int(rr['duration'])
		summary = [num_hidden, accuracy, duration, temp_csv, temp_results]
		csv_line = ','.join([str(e) for e in summary])
		csv_summary.write(csv_line + '\n')
		csv_summary.flush()
		if accuracy > best_accuracy:
			best_accuracy = accuracy
			shutil.copyfile(temp_csv, csv_best_name)
			shutil.copyfile(temp_results, results_name)
			shutil.copyfile(outnameToModelname(temp_results), model_name)
			
	return {'summary':csv_summary_name, 'best':csv_best_name, 'results':results_name, 'model':model_name}

def testCostMatrix(num_columns, num_cv = 4):
	"""Test MLP results with a range of false positive costs
	"""
	
	num_hidden = 5 
	
	csv_matrix_name = csv.makeCsvPath('subset.matrix035')	
	base_name = 'cost.col' + str(num_columns) + '.x' + str(num_cv) 
	csv_results_name = csv.makePath(base_name + '.results')
	csv_summary_name = csv.makeCsvPath(base_name + '.summary')
	csv_best_name    = csv.makeCsvPath(base_name + '.best')
	
	matrix  = csv.readCsvRaw(csv_matrix_name)
	num_attribs = len(matrix[0])-1  # last column is category
	print 'testCostMatrix', len(matrix), num_hidden, num_columns
	
	best_accuracy = 0.0
	results = []
	csv_results = file(csv_summary_name, 'w')
	
	for false_positive_cost in range(1, 11, 2):
		columns = [i for i in range(num_columns)]
		costs_map = {'True':1.0, 'False':float(false_positive_cost)}
		accuracy, temp_csv, temp_results, duration = testMatrixMLP(matrix, columns, makeWekaOptions(0.3, 0.5, num_hidden, num_cv, costs_map))
		r = {'cost':false_positive_cost, 'accuracy':accuracy, 'csv':temp_csv, 'results':temp_results, 'duration':duration}
		results.append(r)
		results.sort(key = lambda r: -r['accuracy'])
		if True:
			print false_positive_cost, ':',  accuracy, len(results), int(duration), 'seconds'
			for i in range(min(5,len(results))):
				rr = results[i]
				print '    ',i, ':', rr['accuracy'], rr['cost'], int(rr['duration'])
		summary = [num_hidden, accuracy, duration, temp_csv, temp_results]
		csv_line = ','.join([str(e) for e in summary])
		csv_results.write(csv_line + '\n')
		csv_results.flush()
		if accuracy > best_accuracy:
			best_accuracy = accuracy
			shutil.copyfile(temp_csv, csv_best_name)
			shutil.copyfile(temp_results, csv_results_name)
		
	return results

#
#
# Data files used in this test

# Input data - Don't touch this    
raw_name = csv.makeCsvPath('ad1')
# Input data with header. Needs to be generated once
headered_name = csv.makePath('header')
#Input data with header and pre-processing
headered_name_pp = csv.makePath('header.pp')   
# PCA on headered_name_pp
headered_name_pca = csv.makePath('header.pp.pca')  
# PCA data normalized to stdev == 1
headered_name_pca_norm = csv.makePath('header.pp.pca.norm')            
# PCA data normalized to stdev == 1 by correlation with outcome
headered_name_pca_corr = csv.makePath('header.pp.pca.norm.corr_order')

if __name__ == '__main__':
	
	if False:
		dumpEnv()
		
	if True:  # Do this once. Then use headered_name_pp
		preprocess(raw_name, headered_name, headered_name_pp)
	
	if False:
		out_fn = 'tmp.out.txt'
		in_fn = csv.headered_name_pca
		runMLPTrain(in_fn, out_fn)
		
	if False:
		testRouletteWheel()
		testRouletteWheelTwice()
		testMutate()
		testCrossOver()
		
	if False:
		selectAttibutesGA()
		
	if False:
		num_subset = 25
		in_filename = csv.makeCsvPath('subset.best' + ('%03d'%num_subset))
		csv_results_name = csv.makePath('hidden.layer.results')
		csv_summary_name = csv.makeCsvPath('hidden.layer.summary')
		csv_best_name = csv.makeCsvPath('hidden.layer.best')
		csv_summary = file(csv_summary_name, 'w')
		best_accuracy = 0.0
		for num_hidden in range(1, num_subset):
			opts = '-H ' + str(num_hidden) + ' -x 4'
			out_filename = csv.makeCsvPath('num.hidden' + ('%03d'%num_hidden))
			temp_base = csv.makeTempPath('num.hidden' + ('%03d'%num_hidden))
			temp_results = temp_base + '.results'
			accuracy, duration = runMLPTrain(in_filename, temp_results, opts)
			summary = [num_hidden, accuracy, best_accuracy, duration, temp_results]
			print summary
			csv_line = ','.join([str(e) for e in summary])
			csv_summary.write(csv_line + '\n')
			csv_summary.flush()
			if accuracy > best_accuracy:
				best_accuracy = accuracy
				shutil.copyfile(temp_results, csv_results_name)
			
	if False:
		num_subset = 25
		in_filename = csv.makeCsvPath('subset.best' + ('%03d'%num_subset))
		csv_results_name = csv.makePath('learning.rate.results')
		csv_summary_name = csv.makeCsvPath('learning.rate.summary')
		csv_best_name = csv.makeCsvPath('learning.rate.best')
		csv_summary = file(csv_summary_name, 'w')
		best_accuracy = 0.0
		for lr in range(1, 10):
			learning_rate = float(lr)/10.0
			opts = '-L ' + str(learning_rate) + ' -H 13 -x 4'
			out_filename = csv.makeCsvPath('learning.rate' + ('%0.2f'%learning_rate))
			temp_base = csv.makeTempPath('learning.rate' + ('%0.2f'%learning_rate))
			temp_results = temp_base + '.results'
			accuracy, duration = runMLP(in_filename, temp_results, opts)
			summary = [learning_rate, accuracy, best_accuracy, duration, temp_results]
			print summary
			csv_line = ','.join([str(e) for e in summary])
			csv_summary.write(csv_line + '\n')
			csv_summary.flush()
			if accuracy > best_accuracy:
				best_accuracy = accuracy
				shutil.copyfile(temp_results, csv_results_name)
				
	if False:
		num_subset = 25
		in_filename = csv.makeCsvPath('subset.best' + ('%03d'%num_subset))
		csv_results_name = csv.makePath('momentum.results')
		csv_summary_name = csv.makeCsvPath('momentum.summary')
		csv_best_name = csv.makeCsvPath('momentum.best')
		csv_summary = file(csv_summary_name, 'w')
		best_accuracy = 0.0
		for lr in range(1, 10):
			momentum = float(lr)/10.0
			opts = '-M ' + str(momentum) + ' -L 0.3 -H 13 -x 4'
			out_filename = csv.makeCsvPath('momentum' + ('%0.2f'%momentum))
			temp_base = csv.makeTempPath('momentum' + ('%0.2f'%momentum))
			temp_results = temp_base + '.results'
			accuracy, duration = runMLP(in_filename, temp_results, opts)
			summary = [momentum, accuracy, best_accuracy, duration, temp_results]
			print summary
			csv_line = ','.join([str(e) for e in summary])
			csv_summary.write(csv_line + '\n')
			csv_summary.flush()
			if accuracy > best_accuracy:
				best_accuracy = accuracy
				shutil.copyfile(temp_results, csv_results_name)			
				
	if False:
		testBySize(True)			
		
	if False:
		if False:
			csv_matrix_name = csv.makeCsvPath('subset.matrix035')	
			num_columns = 10 
			num_cv = 4
			output_basename = 'number.hidden.col' + str(num_columns) + '.x' + str(num_cv) 
			files = testByNumberHidden(csv_matrix_name, output_basename, num_columns, num_cv = 4)
			# testBySize found best size was around 120
			#testByNumberHidden(120, 10)
			predictions_filename = csv.makePath(output_basename + '.predict')
			runMLPPredict(files['best'], files['model'], predictions_filename)
			files['predict'] = predictions_filename
			print files
		if True:
			predictions_filename =  'C:\\dev\\5167assigment1\\number.hidden.col10.x4.predict'
			predictions = getPredictions(predictions_filename)
			def meanPrediction(predictions):
				return sum([p['prediction'] for p in predictions])/float(len(predictions))
			def getPredictionAccuracy(predictions):
				if len(predictions) == 0:
					return 0.0
				else:
					return float(len([p for p in predictions if not p['error']]))/float(len(predictions))
			def getPredictionAccuracyThreshold(predictions, threshold):
				predictions_subset = [p for p in predictions if p['prediction'] >= threshold]
				accuracy =  getPredictionAccuracy(predictions_subset)
				fraction = float(len(predictions_subset))/float(len(predictions))
				return accuracy, len(predictions_subset), fraction
			print 'mean prediction all     ', '%.03f' % meanPrediction(predictions)
			print 'mean prediction error   ', '%.03f' % meanPrediction([p for p in predictions if p['error']])
			print 'prediction accuracy all ', '%.03f' % getPredictionAccuracy(predictions)
			for i in range(11):
				threshold = 0.5 + float(i)*0.05
				accuracy,number, fraction = getPredictionAccuracyThreshold(predictions, threshold)
				print 'prediction accuracy', '%.02f' % threshold, '%.03f' % accuracy, number, '%.03f' % fraction
		#row_index = getRowsFromPredictionsFile(predictions_filename)
		#do pca on this file,train and repeat
				
	if False:
		num_columns = 35
		num_cv = 4
		testCostMatrix(num_columns, num_cv)
		
	if False:
		out = open(out_fn, 'w')
		err = open(err_fn, 'w')
		print args
		print '------------------------ 1'
		p = subprocess.Popen(args, stdout=out, stderr=err)
		print '------------------------ 2xx'		
		p.wait()
		print '------------------------ 3'
					
					
					
					
					
		
		
	
