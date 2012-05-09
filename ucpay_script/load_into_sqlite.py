#!/usr/bin/env python3

DB_FILE = './ucpay.sqlite'
# 2009 and 2010 use a different format
YEARS = range(2004, 2011)

import sqlite3
import csv
from zipfile import ZipFile
from codecs import iterdecode

def load_data_for_year(db, y):
	'''Loads data for the year from the CSV file in the current directory into the sqlite DB.'''
	print('Loading data for {y}'.format(y=y))
	
	db.execute('DROP TABLE IF EXISTS ucpay{y}'.format(y=y))
	# Some of these columns probably won't be needed, but we may as well store them.
	db.execute('''
		CREATE TABLE ucpay{y}
		(	ucpay_id INT PRIMARY KEY
		,	year INT
		,	campus TEXT
		,	name TEXT
		,	job_title TEXT
		,	gross_pay NUMERIC
		,	base_pay NUMERIC
		,	overtime_pay NUMERIC
		,	extra_pay NUMERIC
		)
	'''.format(y=y))
	inner_filename = 'ucpay.csv' if y != 2010 else 'ucpay2010.csv'
	datafile = iterdecode(ZipFile('./ucpay{y}.csv.zip'.format(y=y), mode='r').open(inner_filename, mode='r'), 'utf8')
	data = csv.reader(datafile, dialect=(csv.excel_tab if y == 2010 else csv.excel))

	if y != 2009:
		print(next(data))	# skip header
	
	for e in data:
		assert len(e) == len(["ID","year","campus","name","title","gross","base","overtime","extra","exclude"])
		# Skip tuples with "exclude"=="1", which are grad students and temporary employees rather than research professors
		if e[-1] != '1':
			assert e[-1] == '0'
			db.execute('INSERT INTO ucpay{y} VALUES (?,?,?,?,?,?,?,?,?)'.format(y=y), e[:-1])
	db.commit()
	
	print('	done')






if __name__ == '__main__':
	db = sqlite3.connect(DB_FILE)
	for y in YEARS:
		load_data_for_year(db, y)
	print('All done')
