#!/bin/python

import sqlite3 as lite
import sys,csv

stablename = 'censusPop'


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


scols 		= ['city','state','census2010','proj2010','proj2011','proj2012']
scoltypes 	= ['TEXT','TEXT','REAL','REAL','REAL','REAL']



def writeFile(sfile,con):

	with open(sfile,'r') as ofile: 
		
		reader = csv.reader(ofile,delimiter=",")
		reader.next() # advance past the header 
		
		for line in reader:
				
#
# city state format
#
			citystate = line[2].lower().split(', ')
			if len(citystate) != 2: 
				print line 
				continue

			
			sstate 		= citystate[-1] 
			scitylist 	= citystate[0].split()[:-1]

			scity = ' '.join(scitylist)


			s = map(str,[scity,sstate]+line[-4:])
#			con.cursor().execute('insert into '+stablename+'('+','.join(scols)+') values('+'?,'*(len(s)-1)+'?)',s) 

			swrite = 'insert into censusPop('+','.join(scols)+') values('+'?,'*5+'?)'
#			print swrite
#			print repr(s)
			try: con.cursor().execute(swrite,s) 
			except: 
				print s
				continue
		con.commit()


def createRawSchema():
	
	print len(scols), len(scoltypes)

	sschema = 'create table '+stablename+'(Id INTEGER PRIMARY KEY autoincrement'
	for scol,stype in zip(scols,scoltypes): sschema += ', %s %s'%(scol,stype)
	sschema += ');'



	con = None

	try:
		con = lite.connect('florida.db')
		cur = con.cursor()    
		cur.execute('SELECT SQLITE_VERSION()')
		cur.execute('drop table if exists %s'%stablename)
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



def testfile(sfile,dups = set()):
	elcities = set()
	with open(sfile,'r') as ofile: 
		
		jline = 0
		reader = csv.reader(ofile,delimiter=",")
		reader.next() 
		
		
		for line in reader:
#			print line
				
			jline +=1
#			if jline > 10: break
#			sline = line[2:]

#
# city state format
#
			citystate = line[2].lower().split(', ')
			if len(citystate) != 2: 
				print line 
				continue

			
			sstate 		= citystate[-1] 
			scitylist 	= citystate[0].split()[:-1]

			scity = ' '.join(scitylist)


			print map(str,[scity,sstate]+line[-4:])
			

#			if len(scitylist) < 1: 
#				print line
#				continue
#				
#
#
#			if (scity,sstate) in elcities or (scity,sstate) in dups: 
#				print '\tduplicate city!'
#				print '\t',line
#				dups.add((scity,sstate))
#				
#			else: 
#				elcities.add((scity,sstate))
##			print scity,sstate	
##			print jline
#		print len(elcities), jline		
#	return dups



if __name__ == '__main__':

	sfile = 'medicareData/PEP_2012_PEPANNRES_with_ann.csv'


	con = createRawSchema()
	writeFile(sfile,con)
#	elcities = testfile(sfile)
#	testfile(sfile)
'''
	sfile = 'Medicare-Physician-and-Other-Supplier-PUF-a-CY2012.xlsx' 
	sfile = '../Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012/Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012.xlsx'
	sfile = 'cr.csv'



'''




