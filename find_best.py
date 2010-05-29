"""
http://docs.python.org/library/subprocess.html
"""
import shlex, subprocess, os, csv

if False:
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
	
weka_root = os.environ['WEKA_ROOT']	
weka_jar = weka_root + '\\weka.jar'
weka_mlp = 'weka.classifiers.functions.MultilayerPerceptron'
weka_args = '-H "a,2"'
weka  
	
def runMLP(in_fn, out_fn):
	cmd = 'java -cp ' + weka_root + ' ' + weka_mlp + ' -H "a,2"  + -t ' + in_fn"
	# args = 'java -cp ' + weka_root + ' ' + weka_mlp + ' -H "a,2"  + -t "data\pima_indians_diabetes.arff"'
	out = open(out_fn, 'w')
	err = open(err_fn, 'w')
	print args
	print '------------------------ 1'
	p = subprocess.Popen(args, stdout=out, stderr=err)
	print '------------------------ 2xx'		
	p.wait()
	print '------------------------ 3'

out_fn = 'tmp.out.txt'
err_fn = 'tmp.err.txt'

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
	
#
# The data we are working on
#

# Input data - Don't touch this	
raw_name = 'C:\\dev\\5047assigment1\\ad1.csv'

# Add heade
headered_name = 'C:\\dev\\5047assigment1\\ad1_header.csv'
headered_name_pp = 'C:\\dev\\5047assigment1\\ad1_header_pp.csv'
	
def preprocess
	
if __name__ == '__main__':
	raw_name = 'C:\\dev\\5047assigment1\\ad1.csv'
    headered_name = 'C:\\dev\\5047assigment1\\ad1_header.csv'
    headered_name_pp = 'C:\\dev\\5047assigment1\\ad1_header_pp.csv'
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
					
					
					
					
					
		
		
	
