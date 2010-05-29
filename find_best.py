"""
http://docs.python.org/library/subprocess.html
"""
import shlex, subprocess, os, csv

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
			
	cmd = 'java -cp ' + weka_jar  + ' ' + weka_mlp + mlp_opts + ' -t ' + in_fn
	
	# args = 'java -cp ' + weka_root + ' ' + weka_mlp + ' -H "a,2"  + -t "data\pima_indians_diabetes.arff"'
	out = open(out_fn, 'w')
	print cmd
	print '------------------------ 1'
	p = subprocess.Popen(cmd, stdout=out)
	print '------------------------ 2'		
	p.wait()
	print '------------------------ 3'

	
if __name__ == '__main__':
	
	if False:
		dumpEnv()
		
	if False:  # Do this once. Then use headered_name_pp
		preprocess()
	
	if True:
		out_fn = 'tmp.out.txt'
		in_fn = csv.headered_name_pca
		runMLP(in_fn, out_fn)
		
	if False:
		out = open(out_fn, 'w')
		err = open(err_fn, 'w')
		print args
		print '------------------------ 1'
		p = subprocess.Popen(args, stdout=out, stderr=err)
		print '------------------------ 2xx'		
		p.wait()
		print '------------------------ 3'
					
					
					
					
					
		
		
	
