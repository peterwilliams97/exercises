"""
Do various things with the soybean data set
http://archive.ics.uci.edu/ml/machine-learning-databases/soybean/

1. Add attribute names
2. Check for duplicates
3. Convert to .arff format
4. Combine data sets
"""

from __future__ import division
import math, csv

def readAllData(test_data_path, training_data_path, names_path):
	test_data = csv.readCsvRaw(test_data_path)
	training_data = csv.readCsvRaw(training_data_path)
	return test_data + training_data
	
def getAttrs(instance):
	return [int(x) for x in instance[1:]]
	
def extractAttrs(data):
	return [getAttrs(instance) for instance in data] 

def hasDuplicates(attrs):	
	attrs.sort()
	
	for i in range(1, len(attrs)):
		if attrs[i] == attrs[i-1]:
			return True
		
	return False 
	
def runTests():
	dir = r'C:\dev\5045'
	test_file = 'soybean-large.test.txt'
	training_file = 'soybean-large.data.txt'	
		