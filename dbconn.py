#!/bin/python

import xlrd
import sqlite3 as lite
import sys


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


scols = ['npi','nppes_provider_last_org_name','nppes_provider_first_name','nppes_provider_mi','nppes_credentials','nppes_provider_gender','nppes_entity_code','nppes_provider_street1','nppes_provider_street2','nppes_provider_city','nppes_provider_zip','nppes_provider_state','nppes_provider_country','provider_type','medicare_participation_indicator','place_of_service','hcpcs_code','hcpcs_description','line_srvc_cnt','bene_unique_cnt','bene_day_srvc_cnt','average_Medicare_allowed_amt','stdev_Medicare_allowed_amt','average_submitted_chrg_amt','stdev_submitted_chrg_amt','average_Medicare_payment_amt','stdev_Medicare_payment_amt']



scoltypes = ['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','real','real','real','real','real','real','real','real','real']


def writeSheet(ssheet,con):

	for jrow in xrange(0,ssheet.nrows):
#		print ssheet.row(jrow)
		s = ssheet.row(jrow)
#		swrite = 'values('+','.join(map(lambda x: "'"+str(x)+"'",map(lambda x:x.value,s)))+')'
		
#		con.cursor().execute('insert into RawMedicareUtilData values('+','.join(scols)+')'+swrite) 
#		con.cursor().execute('insert into RawMedicareUtilData values('+'?,'*27+'?)',swrite) 
		con.cursor().execute('insert into RawMedicareUtilData('+','.join(scols)+') values('+'?,'*26+'?)',map(lambda x:str(x.value),s)) 


	con.commit()
#		if jrow > 50: break	

def writeFile(sfile,con):
	workbook = xlrd.open_workbook(sfile)

	for ssheet in workbook.sheet_names():
		
		print 'dumping sheet: ', ssheet
		worksheet = workbook.sheet_by_name(ssheet)
		writeSheet(worksheet,con)

def createRawSchema():
	
	print len(scols), len(scoltypes)

	sschema = 'create table RawMedicareUtilData(Id INTEGER PRIMARY KEY autoincrement'
#	sschema = 'create table RawMedicareUtilData('
	for scol,stype in zip(scols,scoltypes): sschema += ', %s %s'%(scol,stype)
	sschema += ');'



	con = None

	try:
		con = lite.connect('test.db')
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')
		cur.execute('drop table if exists RawMedicareUtilData ')
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


	con = createRawSchema()


	writeFile(sfile,con)

'''



if __name__ == '__main__':

	sfile = 'Medicare-Physician-and-Other-Supplier-PUF-a-CY2012.xlsx' 
	sfile = '../Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012/Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012.xlsx'

#	dumpFile(sfile)

	con = None

	try:
		con = lite.connect('test.db')
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')
		data = cur.fetchone()
		print "SQLite version: %s" % data  

	except lite.Error, e:
    
		print "Error %s:" % e.args[0]
		sys.exit(1)
    
	finally:
    
		if con:
			con.close()
'''

