from __future__ import division

dir = r'C:\dev\natalie'
data_file = 'Course_BSB50101.csv'
counts_file = 'counts.csv'

import math, os, sys, random, datetime, csv

def transpose(data):
	w = len(data[0])
	for instance in data:
		assert(len(instance) == w)
	out = [[]] * w
	for i in range(w):
		out[i] = [instance[i] for instance in data]
	return out
	
def getGradeCounts():
	""" Read the data file
		This is a set of grades """
	data,header = csv.readCsvRaw2(os.path.join(dir, data_file), True)

	""" Category is in column 1 """
	categories = []
	for instance in data:
		cat = instance[1]
		if not cat in categories:
			if len(cat) == 0:
				print instance
			assert(len(cat) > 0)
			categories.append(cat)

	print 'categories -------------------------------'
	for cat in categories:
		print cat

	""" Grades end in _g """
	grades_columns = []
	for i, h in enumerate(header):
		if '_g' in h:
			grades_columns.append(i)

	num_grades = len(grades_columns)

	print 'grades columns names ---------------------'
	for i in range(num_grades):
		print '%5d, %6d,' % (i, grades_columns[i]), header[grades_columns[i]]

	possible_grades = ('HD','D','C','P','N')
	
	if False:
		""" Find all possible values of grades in all subjects """
		grades_vals = [[]] * num_grades
		for instance in data:
			for i in range(num_grades):
				col = grades_columns[i]
				v = instance[col]
				vals = grades_vals[i]
				if not v in vals:
					vals.append(v)
	else:
		grades_vals = [possible_grades] * num_grades

	print 'grades -----------------------------------'
	for i in range(num_grades):
		print '%-10s' % header[grades_columns[i]], grades_vals[i]

	""" counts = categories : subjects : grades 
		First create all the counters """
	counts = {} 
	for cat in categories:
		counts[cat] = []
		for i in range(num_grades):
			vals = grades_vals[i]
			c = {}
			for v in vals:
				c[v] = 0
			counts[cat].append(c)

	for instance in data:
		cat = instance[1]
		cnt = counts[cat]
		for i in range(num_grades):
			col = grades_columns[i]
			v = instance[col]
			cnt[i][v] = cnt[i][v] + 1

	""" Calculate totals """
	total_keys = possible_grades
	if False:
		for i in range(num_grades):
			for k in cnt[i].keys():
				if not k in total_keys:
					total_keys.append(k)

	totals = {}

	for cat in categories:
		totals[cat] = {}
		for i in range(num_grades):
			for v in grades_vals[i]:
				if not v in totals[cat].keys():
					totals[cat][v] = 0
		cnt = counts[cat]
		for i in range(num_grades):
			for k in cnt[i].keys():
				totals[cat][k] = totals[cat][k] + cnt[i][k]
		print 'totals[%s]' % cat, totals[cat]
		counts[cat] = cnt + [totals[cat]]

	header.append('total')
	grades_columns.append(len(header)-1)
	grades_vals.append(total_keys)
	num_grades = num_grades + 1 
	print header

	""" Display the data as a .csv """
	count_header = ['category']
	for i in range(num_grades):
		count_header.append(header[grades_columns[i]])
		for j in range(len(grades_vals[i])-1):
			count_header.append("")

	count_header2 = ['category']
	for i in range(num_grades):
		for k in grades_vals[i]:
			count_header2.append(k)

	count_data = [count_header, count_header2]
	for cat in sorted(counts.keys()):
		row = [cat]
		for i in range(num_grades):
			for k in grades_vals[i]:
				row.append(counts[cat][i][k])
		count_data.append(row)

	csv.writeCsv(os.path.join(dir,counts_file), transpose(count_data))	

if __name__ == '__main__':
	print getGradeCounts.__doc__
	getGradeCounts()
	
	