"""
Do various things with the soybean data set
http://archive.ics.uci.edu/ml/machine-learning-databases/soybean/

1. Add attribute names
2. Check for duplicates
3. Convert to .arff format
4. Combine data sets
"""

from __future__ import division
import math, os, random, csv

def getAttrs(instance):
	return instance[1:]
	return [int(x) for x in instance[1:]]
	
def extractAttrs(data):
	return [getAttrs(instance) for instance in data] 

def numberDuplicates(data):	
	data.sort()
	duplicates = 0
	for i in range(1, len(data)):
		if data[i] == data[i-1]:
			if False:
				print '--------------------------'
				print i-1, data[i-1]
				print i, data[i]
			print '(%d,%d),' % (i,i+1),
			duplicates = duplicates + 1
	print
	return duplicates

def removeDuplicates(data):	
	data.sort()
	out = []
	out.append(data[0])
	for i in range(1, len(data)):
		if not data[i] == data[i-1]:
			out.append(data[i])
	return out

def appendDescription(dir, file_name, description):
	path = os.path.join(dir, file_name)
	base, ext = os.path.splitext(path)
	return base + '.' + description + ext

def parseAttrLine(line):
	"""  1. date:		april,may,june,july,august,september,october,?. """
	pre, post = line.strip().split(':')
	number, attr = pre.strip().split('.')
	vals = post.strip().split(',')
	return {'num':int(num), 'attr':attr.strip(), 'vals':[x.strip() for x in vals]}

def parseAttrs(file):
	lines = file(filename).read().strip().split('\n')
	return [parseAttrLine(line) for line in lines]
	
def runTests():
	dir = r'C:\dev\5045'
	training_file = 'soybean-large.data.csv'
	test_file = 'soybean-large.test.csv'
	combined_file = 'soybean-combined.csv'
	
	training_data = csv.readCsvRaw(os.path.join(dir, training_file))
	test_data = csv.readCsvRaw(os.path.join(dir, test_file))
	combined_data = test_data + training_data
	
	use_class = True
	
	training_duplicates = numberDuplicates(training_data)
	print 'training_duplicates =', training_duplicates
	test_duplicates = numberDuplicates(test_data)
	print 'test_duplicates =', test_duplicates
	combined_duplicates = numberDuplicates(combined_data)
	print 'combined_duplicates =', combined_duplicates
	
	out_training_data = removeDuplicates(training_data)
	random.shuffle(out_training_data)
	out_test_data = removeDuplicates(test_data)
	random.shuffle(out_test_data)
	out_combined_data = removeDuplicates(combined_data)
	random.shuffle(out_combined_data)
	
	csv.writeCsv(appendDescription(dir, training_file, 'sorted'), training_data)
	csv.writeCsv(appendDescription(dir, test_file, 'sorted'), test_data)
	csv.writeCsv(appendDescription(dir, combined_file, 'sorted'), combined_data)
	
	csv.writeCsv(appendDescription(dir, training_file, 'out'), out_training_data)
	csv.writeCsv(appendDescription(dir, test_file, 'out'), out_test_data)
	csv.writeCsv(appendDescription(dir, combined_file, 'out'), out_combined_data)
	
if __name__ == '__main__':
	runTests()
	