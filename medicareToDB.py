#!/bin/python

import xlrd
import sqlite3 as lite
import sys,glob


scols = ['npi','nppes_provider_last_org_name','nppes_provider_first_name','nppes_provider_mi'
	,'nppes_credentials','nppes_provider_gender','nppes_entity_code','nppes_provider_street1'
	,'nppes_provider_street2','nppes_provider_city','nppes_provider_zip','nppes_provider_state'
	,'nppes_provider_country','provider_type','medicare_participation_indicator','place_of_service'
	,'hcpcs_code','hcpcs_description','line_srvc_cnt','bene_unique_cnt','bene_day_srvc_cnt'
	,'average_Medicare_allowed_amt','stdev_Medicare_allowed_amt','average_submitted_chrg_amt'
	,'stdev_submitted_chrg_amt','average_Medicare_payment_amt','stdev_Medicare_payment_amt'
]

scoltypes = ['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'
	,'TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'
	,'TEXT','TEXT','real','real','real','real','real','real'
	,'real','real','real']


dbname = 'medicare.db'


stableName = 'RawMedicareUtilData'

def convertString(x):
	retval = ''
	try:
		retval = str(x.value)
	except:
		retval = str(x).split(':u',1)[-1][1:-1]
	return retval

def writeSheet(ssheet,con):

	for jrow in xrange(0,ssheet.nrows):
		s = ssheet.row(jrow)
		
		swrite = ''
		try:
			swrite = map(convertString,s)
		except: 
			next

		con.cursor().execute('insert into %s('%stableName+','.join(scols)+') values('+'?,'*26+'?)',swrite)


	con.commit()
#		if jrow > 50: break	

def writeFile(sfile,con):
	workbook = xlrd.open_workbook(sfile)

	for ssheet in workbook.sheet_names():
		
		print 'dumping sheet: ', ssheet
		worksheet = workbook.sheet_by_name(ssheet)
		writeSheet(worksheet,con)
	del workbook

def createRawSchema():
	
	print len(scols), len(scoltypes)

	sschema = 'create table %s(Id INTEGER PRIMARY KEY autoincrement'%(stableName)
	for scol,stype in zip(scols,scoltypes): sschema += ', %s %s'%(scol,stype)
	sschema += ');'



	con = None

	try:
		con = lite.connect(dbname)
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')
		cur.execute('drop table if exists %s '%stableName)
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
	sfile = 'medicareData/Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012.xlsx'

	con = createRawSchema()
	sinfiles = glob.glob('medicareData/*.xlsx')
#	sinfiles = [sfile]
#	sinfiles = ['medicareData/Medicare-Physician-and-Other-Supplier-PUF-cd-CY2012.xlsx']
	
	for sfile in sinfiles: 
		
		print sfile
		writeFile(sfile,con)

	con.cursor().execute('create index idx_provider_type on %s(provider_type);'%(stableName))
	con.cursor().execute('create index idx_nppes_provider_zip on %s(nppes_provider_zip);'%(stableName))
	con.cursor().execute('create index idx_nppes_provider_state on %s(nppes_provider_state);'%(stableName))

	con.commit()
	con.close()



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

##sqlite> create table hcpcsDescription as select distinct hcpcs_code,hcpcs_description from RawMedicareUtilData order by hcpcs_code asc,hcpcs_description asc;

#PRAGMA table_info(hcpcsDescription)
 
