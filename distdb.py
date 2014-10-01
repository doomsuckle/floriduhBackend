#!/bin/python

import sqlite3 as lite
import sys,csv


def dumpSheet(ssheet):

	for jrow in xrange(0,ssheet.nrows):
		print ssheet.row(jrow)

		if jrow > 50: break	



def dumpFile(sfile):
	workbook = xlrd.open_workbook(sfile)

	for ssheet in workbook.sheet_names():
		
		print 'dumping sheet: ', ssheet
		worksheet = workbook.sheet_by_name(ssheet)
		dumpSheet(worksheet)


scols = ['city1','city2','dist']
scoltypes = ['TEXT','TEXT','REAL']



def writeFile(sfile,con):
#	workbook = xlrd.open_workbook(sfile)

	with open(sfile,'r') as infile:
		reader = csv.reader(infile,delimiter='|')
		reader.next()
		for s in reader:
		
#			print 'dumping sheet: ', ssheet
#			worksheet = workbook.sheet_by_name(ssheet)
			con.cursor().execute('insert into CityDist('+','.join(scols)+') values('+'?,'*2+'?)',map(str,s)) 
		con.commit()

def createRawSchema():
	
	print len(scols), len(scoltypes)

	sschema = 'create table CityDist(Id INTEGER PRIMARY KEY autoincrement'
	for scol,stype in zip(scols,scoltypes): sschema += ', %s %s'%(scol,stype)
	sschema += ');'



	con = None

	try:
		con = lite.connect('florida.db')
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')
		cur.execute('drop table if exists CityDist')
		cur.execute(sschema)
		data = cur.fetchone()
		print "SQLite version: %s" % data  
		print 'created schema, bro'

	except lite.Error, e:
    
		print "Error %s:" % e.args[0]
		sys.exit(1)

	return con 
#	finally:
 #   
#		if con:
#			con.close()


if __name__ == '__main__':

	sfile = 'Medicare-Physician-and-Other-Supplier-PUF-a-CY2012.xlsx' 
	sfile = '../Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012/Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012.xlsx'
	sfile = 'cr.csv'

	con = createRawSchema()


	writeFile(sfile,con)

