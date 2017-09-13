# -*- coding:utf-8 -*-


### V. Cedeno
### 12 september 2017.
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
    if (len(sys.argv) != 4):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    #starttimes=[['vhmb74qv',1500405556],['5ydhsfg6',1500666678],['gbwspag3', 1501084376],['89ykytnu',1501188119],['ef0hzbwg',1501251511],['jrseoprn',1502200606],['7tbi6mwd',1502215071]]
    #duration=307
    demo = sys.argv[1]
    ltran = sys.argv[2]
    session = sys.argv[3]
    #endtime = float(sys.argv[4])
    #duration = int(sys.argv[5])
    #starttime=endtime-duration
    
    ### Echo inputs.
    #print ("  plots for session or player: ",type)
    #print ("  id of session or player ",id)
     
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/difi'):
    	os.makedirs(os.getcwd()+'/difi')
    #as csvfile
    
    r_demo=open(demo,'rt')
    demo_reader=csv.reader(r_demo,delimiter=',')
    
    letter_tran=open(ltran,'rt')
    ltran_reader=csv.reader(letter_tran,delimiter=',')
    
    notconfile=0
    if not os.path.exists(os.getcwd()+'/delta/deltaFrequency.csv'):
    	notconfile=1
    contribution=open('delta/deltaFrequency.csv', 'a+')
    if notconfile==1:
    	contribution.write('sessionid,playerid,delta\n')
    	
    next(demo_reader)
    #uletter_reader=groupby(sorted(uletter_reader), key=operator.itemgetter(0))
    players=getPlayers(demo_reader,session)

    for row in players:
    	#print(row)
    	letter_tran.seek(0)
    	for row1 in ltran_reader:
    		if row1[1]==row and row1[5]=='True':
    			delta=float(row1[6])-float(row1[7])
    			contribution.write(session+','+row+','+str(delta)+'\n')

 
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
