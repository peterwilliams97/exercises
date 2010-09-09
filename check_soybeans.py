"""
Pre-process the soybean data set
http://archive.ics.uci.edu/ml/machine-learning-databases/soybean/

1. Add attribute names
2. Check for duplicates
3. Compare number of duplicates to expected rate
4. Remove duplicates
5. Convert to .arff format
6. Combine data sets
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
	vals = [x.strip() for x in post.strip().split(',')]
	return {'num':int(number), 'attr':attr.strip(), 'vals':vals}

def parseAttrs(filename):
	lines = file(filename).read().strip().split('\n')
	lines = [x.strip() for x in lines if len(x.strip()) > 0]
	return [parseAttrLine(x) for x in lines]

def applyAttrs(data, attrs):
	assert(len(data[0]) == len(attrs) + 1)
	num_attrs = len(attrs)
	num_instances = len(data)
	header = ['class'] + [attrs[i]['attr'] for i in range(num_attrs)]
	
	out = [None] * len(data)
	for row in range(num_instances):
		instance = data[row]
		out[row] = [instance[0]] + ['?' if instance[i+1] == '?' else attrs[i]['vals'][int(instance[i+1])] for i in range(num_attrs)]

	return (header, out)

def writeArff(data, attrs, name):
	""" Write a Weka .arff file """

def getRandomData(data):
	""" Simulate the population in data with random data with 
	    the same distribution of each attributes.
	    Returns a synthetic population of the same size as data
	"""
	num_attrs = len(data[0])
	num_instances = len(data)
	counts = [{} for i in range(num_attrs)]

	for instance in data:
		for i in range(num_attrs):
			cnt = counts[i]
			val = instance[i]
			if not val in cnt.keys():
				cnt[val] = 0
			cnt[val] = cnt[val] + 1

	for i in range(num_attrs):
		tot = sum([counts[i][k] for k in counts[i].keys()])
		for k in counts[i].keys():
			counts[i][k] = counts[i][k]/tot
		tot = sum([counts[i][k] for k in counts[i].keys()])
		assert(abs(tot - 1.0) < 1e-6)

	random_data = [None] * num_instances
	for row in range(num_instances):
		random_data[row] = [0] * num_attrs
		for i in range(num_attrs): 
			r = random.random()
			top = 0
			for k in counts[i].keys():
				top = top + counts[i][k]
				if r <= top:
					random_data[row][i] = k
					break

	random_data.sort()
	return  random_data

def preprocessSoybeanData():
	dir = r'C:\dev\5045'
	training_file = 'soybean-large.data.csv'
	test_file = 'soybean-large.test.csv'
	combined_file = 'soybean-combined.csv'
	attrs_file = 'soybean.attributes'
	random_file = 'soybean-random.csv'
	
	training_data = csv.readCsvRaw(os.path.join(dir, training_file))
	test_data = csv.readCsvRaw(os.path.join(dir, test_file))
	combined_data = test_data + training_data
	
	random_data = getRandomData(combined_data)

	training_duplicates = numberDuplicates(training_data)
	print 'training_duplicates =', training_duplicates
	test_duplicates = numberDuplicates(test_data)
	print 'test_duplicates =', test_duplicates
	combined_duplicates = numberDuplicates(combined_data)
	print 'combined_duplicates =', combined_duplicates
	random_duplicates = numberDuplicates(random_data)
	print 'random_duplicates =', random_duplicates

	out_training_data = removeDuplicates(training_data)
	random.shuffle(out_training_data)
	out_test_data = removeDuplicates(test_data)
	random.shuffle(out_test_data)
	out_combined_data = removeDuplicates(combined_data)
	random.shuffle(out_combined_data)

	csv.writeCsv(appendDescription(dir, training_file, 'sorted'), training_data)
	csv.writeCsv(appendDescription(dir, test_file, 'sorted'), test_data)
	csv.writeCsv(appendDescription(dir, combined_file, 'sorted'), combined_data)
	csv.writeCsv(appendDescription(dir, random_file, 'sorted'), random_data)

	csv.writeCsv(appendDescription(dir, training_file, 'out'), out_training_data)
	csv.writeCsv(appendDescription(dir, test_file, 'out'), out_test_data)
	csv.writeCsv(appendDescription(dir, combined_file, 'out'), out_combined_data)

	attrs = parseAttrs(os.path.join(dir, attrs_file))
	
	header, named_training_data = applyAttrs(out_training_data, attrs)
	csv.writeCsv(appendDescription(dir, training_file, 'named'), named_training_data, header)
	header, named_test_data = applyAttrs(out_test_data, attrs)
	csv.writeCsv(appendDescription(dir, test_file, 'named'), named_test_data, header)
	header, named_combined_data = applyAttrs(out_combined_data, attrs)
	csv.writeCsv(appendDescription(dir, combined_file, 'named'), named_combined_data, header)

	
if __name__ == '__main__':
	preprocessSoybeanData()
	