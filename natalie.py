from __future__ import division

dir = r'C:\dev\natalie'
data_file = 'Course_BSB50101.csv'
counts_file = 'counts.csv'

import math, os, sys, random, datetime, csv

def transpose(data):
	w = len(data[0])
	for instance in data:
		assert(len(instance) == w)
	return [[instance[i] for instance in data] for i in range(w)]
	
def getGradeCounts():
	""" Read the data file
		This is a set of grades """
	data,header = csv.readCsvRaw2(os.path.join(dir, data_file), True)

	""" Category is in column 1 """
	categories = set([instance[1] for instance in data])

	print 'categories -------------------------------'
	for cat in sorted(categories):
		print cat

	""" Grades end in _g """
	subject_grades_columns = [i for i, h in enumerate(header) if '_g' in h]
	num_subjects = len(subject_grades_columns)

	print 'grades columns names ---------------------'
	for i in range(num_subjects):
		print '%5d, %6d,' % (i, subject_grades_columns[i]), header[subject_grades_columns[i]]

	possible_grades = frozenset(['HD','D','C','P','N'])
	print 'grades -----------------------------------'
	
	for i in range(num_subjects):
		print '%-10s' % header[subject_grades_columns[i]], possible_grades

	""" counts = categories : subjects : grades """
	"""	First create all the counters """
	counts = {} 
	for cat in categories:
		counts[cat] = [{}.fromkeys(possible_grades, 0) for i in range(num_subjects)] 

	""" Count all the category:subject:grade bins """
	for instance in data:
		cat = instance[1]
		cnt = counts[cat]
		for i in range(num_subjects):
			col = subject_grades_columns[i]
			v = instance[col]
			cnt[i][v] = cnt[i][v] + 1

	""" Calculate totals """
	totals = {}

	for cat in categories:
		totals[cat] = {}
		cnt = counts[cat]
		for i in range(num_subjects):
			for k in cnt[i].keys():
				totals[cat][k] = totals[cat].get(k,0) + cnt[i][k]
		print 'totals[%s]' % cat, totals[cat]
		counts[cat] = cnt + [totals[cat]]

	header.append('total')
	subject_grades_columns.append(len(header)-1)
	num_subjects = num_subjects + 1 
	print header

	""" Display the data as a .csv """
	count_header = ['subject']
	for i in range(num_subjects):
		count_header.append(header[subject_grades_columns[i]])
		for j in range(len(possible_grades)):
			count_header.append('')

	count_header2 = ['grade']
	for i in range(num_subjects):
		count_header2.append('')
		for k in possible_grades:
			count_header2.append(k)

	count_data = [count_header, count_header2]
	for cat in sorted(counts.keys()):
		row = ['']
		for i in range(num_subjects):
			row.append('cat_%s' % cat)
			for k in possible_grades:
				row.append(counts[cat][i][k])
		count_data.append(row)

	csv.writeCsv(os.path.join(dir,counts_file), transpose(count_data))	

if __name__ == '__main__':
	getGradeCounts()
	