# -*- coding:utf-8 -*-


### V. Cedeno
### 11 september 2017.
### Take experiments 
### and user letter data
### and generate plot files 
### to determine if parameters from Phase 1 
### will predict occurrences in Phase 2
### input files:
###     Letter_transactions file
###     User_letters file
###     
### output files:
### x values: words, requests, replies, fraction requests, fraction replies, 
### scrabble score, all scrabble score, number of duplicated words
### y value: difi2-difi1
### y value: difi2
### y value: pggc

###     


### Modification History
### --------------------

import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import cycle
from itertools import groupby
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import numpy as np
import datetime as dt
import time
import glob
from matplotlib.colors import from_levels_and_colors


##scrabble score
SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
          "x": 8, "z": 10}
     
## ------------------------------
def getPlayers(reader, session):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    players=[]
    for row in reader:
    	if row[50]==session:
    		if row[1] not in players:
    			players.append(row[1])
    return players


### Start.
def main():
    if (len(sys.argv) != 7):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    #starttimes=[['vhmb74qv',1500405556],['5ydhsfg6',1500666678],['gbwspag3', 1501084376],['89ykytnu',1501188119],['ef0hzbwg',1501251511],['jrseoprn',1502200606],['7tbi6mwd',1502215071]]
    #duration=307
    demo = sys.argv[1]
    instana = sys.argv[2]
    ana = sys.argv[3]
    pg = sys.argv[4]
    sessionid = sys.argv[5]
    anagrams = sys.argv[6]
    ### Echo inputs.
    #print ("  plots for session or player: ",type)
    #print ("  id of session or player ",id)
     
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/difi'):
    	os.makedirs(os.getcwd()+'/difi')
    #as csvfile
    
    r_demo=open(demo,'rt')
    demo_reader=csv.reader(r_demo,delimiter=',')
    
    r_instana=open(instana,'rt')
    instana_reader=csv.reader(r_instana,delimiter=',')
    
    r_ana=open(ana,'rt')
    ana_reader=csv.reader(r_ana,delimiter=',')
    
    r_pg=open(pg,'rt')
    pg_reader=csv.reader(r_pg,delimiter=',')
    
    notconfile=0
    if not os.path.exists(os.getcwd()+'/difi/playerContributions.csv'):
    	notconfile=1
    contribution=open('difi/playerContributions.csv', 'a+')
    if notconfile==1:
    	contribution.write('sessionid,playerid,anagrams,d1Distance,d1Overlap,d2Distance,d2Overlap,d3Distance,d3Overlap,pggContribution,pggEarning\n')
    	
    next(demo_reader)
    #uletter_reader=groupby(sorted(uletter_reader), key=operator.itemgetter(0))
    players=getPlayers(demo_reader,sessionid)

    for row in players:
    	print(row)
    	r_instana.seek(0)
    	r_ana.seek(0)
    	r_pg.seek(0)
    	d1Distance=''
    	d1Overlap=''
    	d2Distance=''
    	d2Overlap=''
    	d3Distance=''
    	d3Overlap=''
    	pggContribution=''
    	pggEarning=''
    	for row1 in instana_reader:
    		if row1[1]==row:
    			d1Distance=row1[18]
    			d1Overlap=row1[19]
    	for row1 in ana_reader:
    		if row1[1]==row:
    			d2Distance=row1[18]
    			d2Overlap=row1[19]
    	for row1 in pg_reader:
    		if row1[1]==row:
    			d3Distance=row1[19]
    			d3Overlap=row1[20]	
    			pggContribution=row1[17]
    			pggEarning=row1[18]
    	contribution.write(sessionid+','+row+','+anagrams+','+d1Distance+','+d1Overlap+','+d2Distance+','+d2Overlap+','+d3Distance+','+d3Overlap+','+pggContribution+','+pggEarning+'\n')

 
 #####
 
    endTime=datetime.now()
    print (" elapsed time (seconds): ",endTime-startTime)
    print (" elapsed time (hours): ",(endTime-startTime)/3600.0)

    print (" -- good termination --")

    return	

## --------------------------
## Execution starts.
if __name__ == '__main__':
    main()
    print (" -- good termination from main --")
