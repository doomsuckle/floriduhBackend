#!/bin/python

import sqlite3 as lite
import sys,json
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from sphereDist import distance_on_unit_sphere
import numpy as np


con = lite.connect('/Users/kypreos/projects/healthcare/plots/florida.db')
cur = con.cursor()

def getProviderTypes(cur):
    cur.execute('''select distinct provider_type as type
    from florida
    order by provider_type asc
    '''
    )
    #ptypes = zip(*cur.fetchall())
    ptypes = [str(x[0]) for x in cur.fetchall()]
    return ptypes
ptypes = getProviderTypes(cur)


def getZipLocations(tcur,stype='Geriatric Psychiatry'):
    tcur.execute('''select lat,long 
    from ziplut
    where provider_type = \'%s\'
'''%(stype))
    gps = tcur.fetchall()
    return gps


import collections

def compressPath(pc,res=4):
    retp = []
    nc = 1
    for j in pc:
        j = map(lambda x:round(x,res),j)
        if retp: 
            if retp[-1][0] == j[0] and retp[-1][1] == j[1] : continue
        retp.append(np.array(j))
    return retp


def getAllPatchPatches(sinfile = '/Users/kypreos/projects/healthcare/states/us-atlas/shp/us/nation.json'):
    
    infile = open(sinfile,'r')

    dat = infile.readlines()
    dat = json.loads(dat[0])
    coords = dat['coordinates']
    
    lpatches = []
    
    for pc in coords:
        pc = compressPath(pc[0],3)

        if len(pc) < 4: continue
        if len(pc) < 10000: continue

        path = Path(pc)
        lpatches.append(path)
    infile.close()
    return lpatches

lpatches = getAllPatchPatches()

def testPointInPaths(pathlist,latp,lonp):
    
    for path in pathlist:
        if path.contains_point(np.array([lonp,latp])): return True
    return False

print testPointInPaths(lpatches,25,-80)
print testPointInPaths(lpatches,32,-87)


con1 = lite.connect('/Users/kypreos/projects/healthcare/medicare.db')
cur1 = con1.cursor()

'''
get the shortest patch a bit faster with fewer calls
'''
from operator import itemgetter
def getClosestPoint(lat0,lon0,lllist,radius=3960):
    
    llbest =[]
    if len(lllist) ==0: return -1
    llbest.extend(sorted(np.array(lllist)-(lat0,lon0),key = lambda x: sum(np.array(map(abs,x)))**2)[:5])
    llbest = np.array(llbest) + (lat0,lon0)
    return distance_on_unit_sphere(lat0,lon0,llbest[0][-2],llbest[0][-1],3960)
    
    

print ptypes

pdict = dict()
for t in ptypes:
    pdict[t]=getZipLocations(cur1,t)

of = open('/Users/kypreos/projects/healthcare/data/tots1.csv','w')
of.write('provider_type,lng,lat,dist\n')
lonstep = 0.4
latstep = 0.4


lonrange = (-130,-62)
latrange = (22,50.4)

lonp = lonrange[0]
latp = latrange[0]

while lonp <= lonrange[1]:

    latp = latrange[0]
    while latp <= latrange[1]:
        for k,v in pdict.iteritems():
            minv = getClosestPoint(latp,lonp,v)
            of.write(','.join(map(str,[k,lonp,latp,minv]))+'\n')
                
        latp+=latstep
        
    lonp += lonstep
    
print 'completed'
of.close()

