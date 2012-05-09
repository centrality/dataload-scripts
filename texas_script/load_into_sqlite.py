#!/usr/bin/env python3

TIMESTR = '2012-05-09 02:39:51+00:00'
DB_FILE = './Texas state employees{0}.sqlite'.format(TIMESTR)


# @@@@@@@@ csv: append &csv=true

import sqlite3
import csv
from bz2 import BZ2File
from io import *
from codecs import iterdecode
import subprocess

def load_data_for_time(db, timestr):
	'''Loads data for the year from the CSV file in the current directory into the sqlite DB.'''
	print('Loading data for {timestr}'.format(timestr=timestr))
	
	db.execute('DROP TABLE IF EXISTS texas')
	# Some of these columns probably won't be needed, but we may as well store them.
	db.execute('''
		create table texas("Employee ID" integer primary key,"Name" varchar,"Title" varchar,"Department" varchar,"Gender" char(1),"Hire_date" string,"Annual_salary" numeric,"Entity" string,"Entity_Type" string)
	''')
	datafile = iterdecode(BZ2File('./Texas state employees{timestr}.csv.bz2'.format(timestr=timestr), mode='r'), 'utf8')
	
	data = csv.reader(datafile)
	#data = csv.reader(open(datafile, 'rt', newline=''))
	print(next(data))	# skip header
	for e in data:
		assert len(e) == len(["Employee ID","Name","Title","Department","Gender","Hire_date","Annual_salary","Entity","Entity_Type"])
		db.execute('INSERT INTO texas VALUES (?,?,?,?,?,?,?,?,?)', e)
	db.commit()
	
	print('	done')

if __name__ == '__main__':
	db = sqlite3.connect(DB_FILE)
	load_data_for_time(db, TIMESTR)
	print('All done')
