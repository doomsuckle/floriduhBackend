#!/bin/python

import csv,math


names = ["Zipcode","ZipCodeType","City","State","LocationType"
	,"Lat","Long","Location","Decommisioned","TaxReturnsFiled","EstimatedPopulation","TotalWage"]


sinfile = 'data/free-zipcode-database-Primary.csv' 


infile = open(sinfile,'r')

#print infile.readlines()[:10]

reader = csv.reader(infile)#,delimiter=',')

dat = reader.next()
print dat

jline = 0


from sphereDist import distance_on_unit_sphere 


class cityData:

	def __init__(self,_zipcode,_city,_state,_lat,_lon):

		self.zipcode,self.city,self.state,self.lat,self.lon = _zipcode,str(_city).lower(),str(_state),float(_lat),float(_lon)

		self.sname = city,"-",state 

		self.epop = 0

	def __repr__(self): return city	#+"-"+state
	def __str__(self): return city	#+"-"+state

	def addpop(self,epop): self.epop += float(epop or 0)

#	def __cmp__(self): return sname 


used = set()

cities = []

for line in reader:
#	print line

	zipcode,zipcodeType, city, state, locationType, lat, lon, location, decommisioned,taxReturnsFiled,estimPop,totalWage = line

	if str(state) != "FL": continue 

#	print len(state)



	cd = cityData(zipcode,city, state,lat,lon)
	if str(cd) in used: 
		continue
		

	used.add(str(cd))

	cities.append(cd)
	
	jline +=1

def kmtomile(d1): return d1*0.621371
def mtomile(d1): return d1*0.621371/1.e3




sout = 'city1|city2|r\n'

ofile = open('cr.csv','w')
ofile.write(sout)

for cd in cities:
#	print cd.city,cd.lat,cd.lon, '---'

#	if cd.city != 'pensacola': continue
	
	for cd1 in cities:
	
		if cd1 == cd: continue
#		if cd1.city != 'jacksonville': continue
		
#		print cd.city,cd.lat,cd.lon, '---', cd1.city,cd1.lat,cd1.lon
		r = distance_on_unit_sphere(cd.lat, cd.lon, cd1.lat, cd1.lon)
#		print cd.city,cd.lat,cd.lon, '---', cd1.city,cd1.lat,cd1.lon,mtomile(r)

#		print cd.city	
		ofile.write('|'.join(map(str,[cd.city,cd1.city,mtomile(r)]))+'\n')
	

#		break
#	break
ofile.close()

#print used


