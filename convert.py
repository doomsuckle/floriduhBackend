#!/bin/python

import xlrd




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

if __name__ == '__main__':

	sfile = 'Medicare-Physician-and-Other-Supplier-PUF-a-CY2012.xlsx' 
	sfile = '../Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012/Medicare-Physician-and-Other-Supplier-PUF-yz-CY2012.xlsx'

	dumpFile(sfile)
	

