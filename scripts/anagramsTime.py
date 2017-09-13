# -*- coding:utf-8 -*-


### V. Cedeno
### 5 september 2017.
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
    	if row[0]==session:
    		if row[3] not in players:
    			players.append(row[3])
    return players

## ------------------------------
def getRequestsSent(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    requests=[]
    for row in reader:
    	if row[0]==player:
    		requests.append([row[7],row[6]])
    return requests

## ------------------------------
def getRequestsReceived(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    requests=[]
    for row in reader:
    	if row[1]==player:
    		requests.append([row[7],row[6]])
    return requests
    

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
    csession = sys.argv[1]
    uletter = sys.argv[2]
    tspent = sys.argv[3]
     
    ### Output files. 
    #if not os.path.exists(os.getcwd()+'/requestsReplies'):
    #	os.makedirs(os.getcwd()+'/requestsReplies')
    #as csvfile
    
    com_session=open(csession,'rt')
    csession_reader=csv.reader(com_session,delimiter=',')
    
    user_letter=open(uletter,'rt')
    uletter_reader=csv.reader(user_letter,delimiter=',')
    
    t_spent=open(tspent,'rt')
    tspent_reader=csv.reader(t_spent,delimiter=',')
    
    fileA=open('anagramsTime.csv', 'w')
    
    sessions=[]
    for row in csession_reader:
    	if row[1] == 'Public Goods Game - IRB.v2':
    		sessions.append(row[0])
    
    players=[]
    for row in sessions:
    	user_letter.seek(0)
    	players=getPlayers(uletter_reader, row)
    	#print(row)
    	fileA.write(row+'\n')
    	maxinit=0
    	minresta=1504640941
    	for player in players:
    		t_spent.seek(0)
    		for line in tspent_reader:
    			if line[2]==player and line[4]=='anagrams' and line[5]=='Anagrams':
    				if float(line[6])>maxinit:
    					maxinit=float(line[6])
    				fileA.write(player+',')
    				fileA.write(line[6]+',')
    				fileA.write(line[7]+'\n')
    				resta=float(line[6])-int(line[7])
    				if resta<minresta:
    					minresta=resta
    	fileA.write(str(maxinit)+'\n')
    	fileA.write(str(maxinit-minresta)+'\n')
    	#fileA.write(str(minresta)+'\n')
    				#print(line[6])
    				#print(line[7])
    	
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
