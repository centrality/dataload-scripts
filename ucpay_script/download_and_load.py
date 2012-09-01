#!/usr/bin/env python3

import subprocess as S

DB_FILE = './ucpay.sqlite'
# 2009 and 2010,2011 use a different format
YEARS = range(2004, 2012)

import sqlite3
import csv
from zipfile import ZipFile
from codecs import iterdecode

def download():
	'''Downloads the raw data files from ucpay.globl.org into the current working directory.'''
	uris = list(map("http://ucpay.globl.org/ucpay{0}.csv.zip".format, YEARS))
	S.check_call(["wget"] + uris)

def create_ucpay_table(db):
	'''Creates in the sqlite DB file a "ucpay" table that data will be stored into.'''
	db.execute('DROP TABLE IF EXISTS ucpay')
	# Some of these columns probably won't be needed, but we may as well store them.
	db.execute('''
		CREATE TABLE ucpay
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
	''')

def load_data_for_year(db, y):
	'''Loads data for the year from the CSV file in the current directory into the sqlite DB.'''
	print('Loading data for {y}'.format(y=y))
	
	inner_filename = 'ucpay.csv' if y < 2010 else 'ucpay{0}.csv'.format(y)
	datafile = iterdecode(ZipFile('./ucpay{y}.csv.zip'.format(y=y), mode='r').open(inner_filename, mode='r'), 'utf8')
	data = csv.reader(datafile, dialect=(csv.excel_tab if y >= 2010 else csv.excel))

	if y != 2009:
		print(next(data))	# skip header
	
	for e in data:
		assert len(e) == len(["ID","year","campus","name","title","gross","base","overtime","extra","exclude"])
		# Skip tuples with "exclude"=="1", which are grad students and temporary employees rather than research professors
		if e[-1] != '1':
			assert e[-1] == '0'
			assert e[1] == str(y), "\tBogus year '{0}'; should be '{1}'".format(e[1], str(y))
			db.execute('INSERT INTO ucpay VALUES (?,?,?,?,?,?,?,?,?)', e[:-1])
	db.commit()
	
	print('	done')

if __name__ == '__main__':
	download()
	db = sqlite3.connect(DB_FILE)
	create_ucpay_table(db)
	for y in YEARS:
		load_data_for_year(db, y)
	print('All done')
