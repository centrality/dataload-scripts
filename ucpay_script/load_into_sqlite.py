#!/usr/bin/env python3

DB_FILE = './ucpay.sqlite'
# @@@@@@@ 2010 uses a different format
YEARS = range(2004, 2010)

# @@@@@@@@ csv: append &csv=true

import sqlite3
import csv
from zipfile import ZipFile
from io import TextIOWrapper

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
	datafile = ZipFile('./ucpay{y}.csv.zip'.format(y=y), mode='r').open('ucpay.csv', mode='r')
	
	# Kludge to make it work on python 3.1
	datafile.readable = lambda: True
	datafile.writable = lambda: False
	datafile.seekable = lambda: False
	datafile.read1 = datafile.read
	
	data = csv.reader(TextIOWrapper(datafile, newline=''))
	#data = csv.reader(open(, 'rt', newline=''))
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
