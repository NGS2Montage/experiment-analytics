# -*- coding:utf-8 -*-


### 06 jun 2017.
### Take experiment 1 output data
### and generate output files for plotting.
### input files:
###     Team_words file
###     Letter_transactions file
###     
### output files:
###     Time history of (#words, #request, #replies) summary over all players.
###     Time history of (#words, #request, #replies) summary for every player individually.
###     


### Modification History
### --------------------

import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import groupby
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter

timegroup='1'

##scrabble score
SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
          "x": 8, "z": 10}
        
## ------------------------------
def scrabble_score(word):
    """
    	word: word we eant the scrabble score form
    """
    score=sum(SCORES[letter] for letter in word)
    return score

## ------------------------------
def getCounts(player,end,begin):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    twords=open(sys.argv[1],'rt')
    ltran=open(sys.argv[2],'rt')
    nwords=0
    nreq=0
    t_reader=csv.reader(twords,delimiter=',')
    l_reader=csv.reader(ltran,delimiter=',')
    next(t_reader)
    next(l_reader)
    #print(begin)
    #print(end)
    for row in l_reader:
    	#print(row[7])
    	if row[0]==player and float(row[7])>=begin and float(row[7])<end:
    		nreq=nreq+1
    for row in t_reader:
    	#print(row[])
    	if row[3]==player and float(row[6])>=begin and float(row[6])<end:
    		nwords=nwords+1
    return (nwords,nreq)

## ------------------------------
def getReplies(player,end,begin):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    ltran=open(sys.argv[2],'rt')
    nrep=0
    l_reader=csv.reader(ltran,delimiter=',')
    next(l_reader)
    #print(begin)
    #print(end)
    for row in l_reader:
    	#print(row[7])
    	if row[1]==player and row[5]=='True' and float(row[6])>=begin and float(row[6])<end:
    		nrep=nrep+1
    return (nrep)


### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 3):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    ### Command line arguments.
    team_words = sys.argv[1]
    letter_tran = sys.argv[2]
	
    ### Echo inputs.
    print ("  input file containing team words (team_words file): ",team_words)
    
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/delta'):
    	os.makedirs(os.getcwd()+'/delta')
    
    twords=open(team_words,'rt')
    ltran=open(letter_tran,'rt')
    
    twords_reader=csv.reader(twords,delimiter=',')
    ltran_reader=csv.reader(ltran,delimiter=',')
    
    
    #duplication analysis#
    #contribution=open('Duplication.csv', 'a+')
    starttime=[['7tbi6mwd',1502215076]]
    next(twords_reader)
    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    cycol=cycle('bgrcmky')
    allsessions=''
    fig, ax = plt.subplots(figsize=(25, 15))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	reptimes=[]
    	deltas=[]
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				reptimes.append(round(float(row[6])))
    		#print(reptimes)
    		
    		for row in starttime:
    			if row[0]==key:
    				d1=row[1]
    		if len(reptimes)>0:
    			reptimes=sorted(reptimes)
    			for row in reptimes:
    				deltas.append(row-d1)
    				d1=row
    			#print(reptimes)	
    			#print(deltas)
    		gdelta=Counter(deltas)
    	for number,count in gdelta.items():
    		x.append(number)
    		y.append(count)
    	if len(x)>0:	
    		ax.plot(x, y, 'ro',ms=15, label=key, color=next(cycol))
    		#print(x)
    		#print(y)
    			#plt.hist(deltas, bins=range(min(deltas), max(deltas) + 10, 10))
    			#plt.show()
    		x=[]
    		y=[]
    ax.margins(0.05)
    #allsessions=allsessions+key
    
 	#for i, txt in enumerate(playerlabel):
    	#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)

    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('Count',fontsize=45)
    plt.xlabel('Time duration between sucessive replies',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/delta/deltaRepliesVS#Count.png')
    plt.cla()
    plt.close(fig)
    	
    	#####individual
    #as csvfile
    twords.seek(0)
    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	cycol=cycle('bgrcmky')
    	allsessions='Session:'
    	fig, ax = plt.subplots(figsize=(25, 15))
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		reptimes=[]
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				reptimes.append(round(float(row[6])))
    		#print(reptimes)
    		deltas=[]
    		for row in starttime:
    			if row[0]==key:
    				d1=row[1]
    		if len(reptimes)>0:
    			reptimes=sorted(reptimes)
    			for row in reptimes:
    				deltas.append(row-d1)
    				d1=row
    			#print(reptimes)	
    			#print(deltas)
    		gdelta=Counter(deltas)
    		for number,count in gdelta.items():
    			x.append(number)
    			y.append(count)
    		if len(x)>0:	
    			ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    			#plt.hist(deltas, bins=range(min(deltas), max(deltas) + 10, 10))
    			#plt.show()
    		x=[]
    		y=[]
    	ax.margins(0.05)
    	allsessions=allsessions+key
    
    		#for i, txt in enumerate(playerlabel):
    		#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	if not os.path.exists(os.getcwd()+'/delta/'+key):
    		os.makedirs(os.getcwd()+'/delta/'+key)
    	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    	plt.ylabel('Count',fontsize=45)
    	plt.xlabel('Time duration between sucessive replies',fontsize=45)
    	plt.xticks(fontsize=45)
    	plt.yticks(fontsize=45)
    	plt.title(allsessions,fontsize=45)
    	plt.savefig(os.getcwd()+'/delta/'+key+'/deltaRepliesVS#Count.png')
    	plt.cla()
    	plt.close(fig)
    
    #####
    twords.seek(0)

    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	cycol=cycle('bgrcmky')
    	allsessions='Session:'
    	fig, ax = plt.subplots(figsize=(25, 15))
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		deltas=[]
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				delta=float(row[6])-float(row[7])
    				nwords,nreq=getCounts(key1,float(row[6]),float(row[7]))
    				present=0
    				for de in deltas:
    					if de[0]==round(delta):
    						de[1]=de[1]+nwords+nreq
    						present=1
    				if present==0:
    					deltas.append([round(delta),nwords+nreq])
    		for de in deltas:
    			#print(de)
    			x.append(de[0])
    			y.append(de[1])
    		if len(x)>0:	
    			ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    		x=[]
    		y=[]
    	ax.margins(0.05)
    	allsessions=allsessions+key
    
    		#for i, txt in enumerate(playerlabel):
    		#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	if not os.path.exists(os.getcwd()+'/delta/'+key):
    		os.makedirs(os.getcwd()+'/delta/'+key)
    	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    	plt.ylabel('#Words+#RequestsMade',fontsize=45)
    	plt.xlabel('Time duration between request and reply',fontsize=45)
    	plt.xticks(fontsize=45)
    	plt.yticks(fontsize=45)
    	plt.title(allsessions,fontsize=45)
    	plt.savefig(os.getcwd()+'/delta/'+key+'/deltaVS#Words+Requests.png')
    	
    	plt.cla()
    	plt.close(fig)
    	
    	 #####individual
    twords.seek(0)

    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    cycol=cycle('bgrcmky')
    allsessions=''
    fig, ax = plt.subplots(figsize=(25, 15))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	deltas=[]
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				delta=float(row[6])-float(row[7])
    				nwords,nreq=getCounts(key1,float(row[6]),float(row[7]))
    				present=0
    				for de in deltas:
    					if de[0]==round(delta):
    						de[1]=de[1]+nwords+nreq
    						present=1
    				if present==0:
    					deltas.append([round(delta),nwords+nreq])
    	for de in deltas:
    		#print(de)
    		x.append(de[0])
    		y.append(de[1])
    	if len(x)>0:	
    		ax.plot(x, y, 'ro',ms=15, label=key, color=next(cycol))
    	x=[]
    	y=[]
    ax.margins(0.05)
    #allsessions=allsessions+key
    
    		#for i, txt in enumerate(playerlabel):
    		#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('#Words+#RequestsMade',fontsize=45)
    plt.xlabel('Time duration between request and reply',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/delta/deltaVS#Words+Requests.png')
    	
    plt.cla()
    plt.close(fig)
    	 ##### individual
    twords.seek(0)

    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	cycol=cycle('bgrcmky')
    	allsessions='Session:'
    	fig, ax = plt.subplots(figsize=(25, 15))
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		deltas=[]
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				delta=float(row[6])-float(row[7])
    				nwords,nreq=getCounts(key1,float(row[6]),float(row[7]))
    				present=0
    				for de in deltas:
    					if de[0]==round(delta):
    						de[1]=de[1]+nwords
    						present=1
    				if present==0:
    					deltas.append([round(delta),nwords])
    		for de in deltas:
    			#print(de)
    			x.append(de[0])
    			y.append(de[1])
    		if len(x)>0:	
    			ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    		x=[]
    		y=[]
    	ax.margins(0.05)
    	allsessions=allsessions+key
    
    		#for i, txt in enumerate(playerlabel):
    		#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	if not os.path.exists(os.getcwd()+'/delta/'+key):
    		os.makedirs(os.getcwd()+'/delta/'+key)
    	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    	plt.ylabel('#Words',fontsize=45)
    	plt.xlabel('Time duration between requests and reply',fontsize=45)
    	plt.xticks(fontsize=45)
    	plt.yticks(fontsize=45)
    	plt.title(allsessions,fontsize=45)
    	plt.savefig(os.getcwd()+'/delta/'+key+'/deltaVS#Words.png')
    	
    	plt.cla()
    	plt.close(fig)
    	
    	#####
    	
    	
    	#####all
    twords.seek(0)

    twords_reader=sorted(twords_reader,key=operator.itemgetter(0,3))
    cycol=cycle('bgrcmky')
    allsessions=''
    fig, ax = plt.subplots(figsize=(25, 15))
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	#print(key)
    	x=[]
    	y=[]
    	deltas=[]
    	for key1,items1 in groupby(items,key=operator.itemgetter(3)):
    		#print(key1)
    		ltran.seek(0)
    		for row in ltran_reader:
    			if row[1]==key1 and row[5]=='True':
    				delta=float(row[6])-float(row[7])
    				nwords,nreq=getCounts(key1,float(row[6]),float(row[7]))
    				present=0
    				for de in deltas:
    					if de[0]==round(delta):
    						de[1]=de[1]+nwords
    						present=1
    				if present==0:
    					deltas.append([round(delta),nwords])
    	for de in deltas:
    		#print(de)
    		x.append(de[0])
    		y.append(de[1])
    	if len(x)>0:	
    		ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    	x=[]
    	y=[]
    ax.margins(0.05)
    #allsessions=allsessions+key
    
    		#for i, txt in enumerate(playerlabel):
    		#	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)

    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('#Words',fontsize=45)
    plt.xlabel('Time duration between request and reply',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/delta/deltaVS#Words.png')	
    plt.cla()
    plt.close(fig)
    	
    endTime = datetime.now()

    print (" elapsed time (seconds): ",endTime-startTime)
    print (" elapsed time (hours): ",(endTime-startTime)/3600.0)

    print (" -- good termination --")

    return	

## --------------------------
## Execution starts.
if __name__ == '__main__':
    main()
    print (" -- good termination from main --")
