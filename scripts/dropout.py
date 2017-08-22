# -*- coding:utf-8 -*-


### V. Cedeno
### 15 august 2017.
### Take experiments neighbor data
### and generate plot files 
### to understand dropout
### input files:
###     Neighbors file
###     
### output files:
### initial scrabble score vs. dropout fraction
### initial and all scrabble score vs. dropout fraction
### dropout neighbors vs. dropout fraction
### y value: pggc



### Modification History
### --------------------

import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import groupby
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import glob

## ------------------------------
def getNeighborData(ireader,player_code):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    dropout=0
    n1=''
    n2=''
    for row in ireader:
    	if row[1] == player_code:
    		n1=row[2]
    		n2=row[3]
    		dr=open('Dropout.csv','rt')
    		reader=csv.reader(dr,delimiter=',')
    		for rows in reader:
    			if rows[1]==n1 or rows[1]==n2:
    				if rows[3] >='1':
    					dropout=dropout+1
    return dropout

### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 2):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ### Command line arguments.
    neighbors = sys.argv[1]
    
    #session = sys.argv[1]
    #timeend = sys.argv[2]
    #duration = sys.argv[3]
    #global begin
    #begin=datetime.utcfromtimestamp(float(timeend)-int(duration))
    #global end
    #end=datetime.utcfromtimestamp(float(timeend))
    
    ### Echo inputs.
    #print ("  plots for session or player: ",type)
    #print ("  id of session or player ",id)
     
    ### Output files. 
    ne=open(neighbors,'rt')
    
    ne_reader=csv.reader(ne,delimiter=',')
    
    
    if not os.path.exists(os.getcwd()+'/dropout/all'):
    	os.makedirs(os.getcwd()+'/dropout/all')
    #as csvfile
    
    notconfile=0
    if not os.path.exists(os.getcwd()+'/Dropout.csv'):
    	notconfile=1
    dropout=open('Dropout.csv','rt')
    if notconfile==1:
    	contribution.write('session,playercode,score,dropout,unansweredRequests,neighborsScores,totalscore\n')
    	
    	
    
    
    dropout_reader=csv.reader(dropout,delimiter=',')
    
    labelx='Dropout Analysis'
    allsessions='Sessions:-'
    fig, ax = plt.subplots(figsize=(25, 15))
    x=[]
    y=[]
    xall=[]
    yall=[]
    cycol=cycle('bgrcmky')
    sessionlabel=[]
    next(dropout_reader)
    dropout_reader=sorted(dropout_reader, key=operator.itemgetter(0,2,3))
    bsession=''
    index=0
    maxindex=len(dropout_reader)
    dropout.seek(0)
    for key,items in groupby(dropout_reader,operator.itemgetter(0,2)):
    	if index==0:
    		bsession=key[0]
    	total=0
    	dropcount=0
    	for item in items:
    		index=index+1
    		total=total+1
    		if item[3]>='1':
    			dropcount=dropcount+1
    	if bsession!=key[0]:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		allsessions=allsessions+bsession+'-'
    		bsession=key[0] 		
    		x=[]
    		y=[]	
    	x.append(key[1])
    	y.append(dropcount/total)
    	xall.append(dropcount)
    	yall.append(total)
    	if index==maxindex:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		allsessions=allsessions+bsession+'-'
    	#print(key)
    	#print(dropcount)
    	#print(total)
    
    #for i, txt in enumerate(playerlabel):
    #	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('Fraction of players dropout',fontsize=35)
    plt.xlabel('Initial Scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/dropout/all/scrabbleScoreFractionDropout.png')
    plt.cla()
    plt.close(fig)
    
    ####
    
    allsessions='Sessions:-'
    fig, ax = plt.subplots(figsize=(25, 15))
    x=[]
    y=[]
    xall=[]
    yall=[]
    cycol=cycle('bgrcmky')
    sessionlabel=[]
    dropout.seek(0)
    dropout_reader=sorted(dropout_reader, key=operator.itemgetter(0,6,3))
    bsession=''
    index=0
    maxindex=len(dropout_reader)
    dropout.seek(0)
    for key,items in groupby(dropout_reader,operator.itemgetter(0,6)):
    	if index==0:
    		bsession=key[0]
    	total=0
    	dropcount=0
    	for item in items:
    		index=index+1
    		total=total+1
    		if item[3]>='1':
    			dropcount=dropcount+1
    	if bsession!=key[0]:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		allsessions=allsessions+bsession+'-'
    		bsession=key[0] 		
    		x=[]
    		y=[]	
    	x.append(key[1])
    	y.append(dropcount/total)
    	xall.append(dropcount)
    	yall.append(total)
    	if index==maxindex:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		allsessions=allsessions+bsession+'-'
    	#print(key)
    	#print(dropcount)
    	#print(total)
    
    #for i, txt in enumerate(playerlabel):
    #	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('Fraction of players dropout',fontsize=35)
    plt.xlabel('Possible Scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/dropout/all/possibleScrabbleScoreFractionDropout.png')
    plt.cla()
    plt.close(fig)

 ####
    
    allsessions='Sessions:-'
    fig, ax = plt.subplots(figsize=(25, 15))
    x=[]
    y=[]
    xall=[]
    yall=[]
    nelist=[]
    cycol=cycle('bgrcmky')
    dropout.seek(0)
    maxindex=0
    for key,items in groupby(dropout_reader,operator.itemgetter(0)):
    	for item in items:
    		ne.seek(0)
    		ndrop=getNeighborData(ne_reader,item[1])
    		nelist.append([key,ndrop,item[3]])	
    		maxindex=maxindex+1
    nesorted=sorted(nelist, key=operator.itemgetter(0,1,2))
    #print(nesorted)
    bsession=''
    index=0
    for key,items in groupby(nesorted,operator.itemgetter(0,1)):
    	if index==0:
    		bsession=key[0]
    	total=0
    	dropcount=0
    	for item in items:
    		index=index+1
    		total=total+1
    		if item[2]>='1':
    			dropcount=dropcount+1
    	if bsession!=key[0]:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		#print(x)
    		#print(y)
    		allsessions=allsessions+bsession+'-'
    		bsession=key[0] 		
    		x=[]
    		y=[]	
    	x.append(key[1])
    	y.append(dropcount/total)
    	xall.append(dropcount)
    	yall.append(total)
    	if index==maxindex:
    		ax.plot(x, y, 'ro',ms=15, label=bsession, color=next(cycol))
    		ax.margins(0.05)
    		#print(x)
    		#print(y)
    		allsessions=allsessions+bsession+'-'
    	#print(key)
    	#print(dropcount)
    	#print(total)
    
    #for i, txt in enumerate(playerlabel):
    #	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('Fraction of players dropout',fontsize=35)
    plt.xlabel('Number of dropout neighbors',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/dropout/all/neighborsDropoutFractionDropout.png')
    plt.cla()
    plt.close(fig)
    
    
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
