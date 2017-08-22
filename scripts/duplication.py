# -*- coding:utf-8 -*-


### V. Cedeno
### 17 august 2017.
### Take experiments team words, user letters, letter transactions data
### and generate plot files 
### to understand duplication of words
### input files:
###     team words file
###		user letters file
###		letter transactions file
###     
### output files:
### letters in a word vs. words duplicated by team (also by player)
### letters in a word vs. words that could have been duplicated by team (also by player)
### letters in a word vs. Fraction of words that the team could have duplicated
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
def getSessionData(ireader,session_code):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    rows=[row for row in ireader if row[0] == session_code]
    return rows

### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 4):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ### Command line arguments.
    team_words = sys.argv[1]
    user_letters = sys.argv[2]
    letter_tran = sys.argv[3]
	
    ### Echo inputs.
    print ("  input file containing team words (team_words file): ",team_words)
    
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/duplication'):
    	os.makedirs(os.getcwd()+'/duplication')
    
    twords=open(team_words,'rt')
    uletters=open(user_letters,'rt')
    ltran=open(letter_tran,'rt')
    
    twords_reader=csv.reader(twords,delimiter=',')
    uletter_reader=csv.reader(uletters,delimiter=',')
    ltran_reader=csv.reader(ltran,delimiter=',')
    
    
    #duplication analysis#
    #contribution=open('Duplication.csv', 'a+')
    

    #as csvfile
    allwords=[]
    duplications=[]
    dupfraction=[]
    
    next(twords_reader)
    for key,items in groupby(twords_reader,operator.itemgetter(0)):
    	for item in items:
    		lenword=len(item[5])
    		word=item[5]
    		present=0
    		for dup in allwords:
    			if dup[0]==key and dup[2]==word:
    				dup[3]=dup[3]+1
    				present=1
    		if present==0:
    			allwords.append([key,lenword,word,1])
    for row in allwords:
    #	print(row)
    	if row[3]>1:
    		duplications.append(row)
    #for row in duplications:
    	#print(row)
    fig, ax = plt.subplots(figsize=(25, 15))
    x=[]
    y=[]
    cycol=cycle('bgrcmk')
    labelx='Duplication Analysis'
    allsessions='Sessions:'
    fig, ax = plt.subplots(figsize=(25, 15))
    cycol=cycle('bgrcmky')
    for key,items in groupby(sorted(duplications),operator.itemgetter(0)):
    	#print(key)
    	for key1,items1 in groupby(items,key=operator.itemgetter(1)):
    		#print(key1)
    		counts=0
    		for item in items1:
    			counts=counts+item[3]-1
    		#print(counts)
    		
    		x.append(key1)
    		y.append(counts)
    	if(len(x)>0):
    		ax.plot(x, y, 'ro',ms=15, label=key, color=next(cycol))	
    		dupfraction.append([key,x,y])
    		#print(key)
    		#print(x)
    		#print(y)	
    	#allsessions=allsessions+key+'-'
    	x=[]
    	y=[]
    #print(dupfraction)
    #for i, txt in enumerate(playerlabel):
    #	ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    ax.margins(0.05)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('#Words duplicated by team',fontsize=45)
    plt.xlabel('Letters in a word',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    plt.savefig(os.getcwd()+'/duplication/#lettersVSDuplicatedWords.png')
    plt.cla()
    plt.close(fig)
    	
    
    
    #####
    twords.seek(0)
    numwords=[]
    next(twords_reader)
    tsorted=sorted(twords_reader, key=operator.itemgetter(0,3))
    for key,items in groupby(tsorted,operator.itemgetter(0,3)):
    	for item in items:
    		lenword=len(item[5])
    		word=item[5]
    		duplicated=0
    		for dup in duplications:
    			if dup[0]==key[0] and dup[2]==word:
    				duplicated=1
    		if duplicated==1:	
    			present=0
    			for num in numwords:
    				if num[0]==key[0] and num[1]==key[1] and  num[2]==lenword:
    					num[3]=num[3]+1
    					present=1
    			if present==0:
    				numwords.append([key[0],key[1],lenword,1])
    		
    for key,items in groupby(numwords,operator.itemgetter(0)):
    	labelx='Duplication Analysis'
    	fig, ax = plt.subplots(figsize=(25, 15))
    	x=[]
    	y=[]
    	xdup=[]
    	ydup=[]
    	cycol=cycle('bgrcmky')
    	sessionlabel=[]
    	#print(key)
    	for key1,items1 in groupby(items,key=operator.itemgetter(1)):
    		for item in items1:
    			#print(item)
    			x.append(item[2])
    			y.append(item[3])
    		ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    		x=[]
    		y=[]
    	ax.margins(0.05)
    	#allsessions=allsessions+key1+'-'
    	if not os.path.exists(os.getcwd()+'/duplication/'+key):
    		os.makedirs(os.getcwd()+'/duplication/'+key)
    	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    	plt.ylabel('#Words duplicated by player',fontsize=45)
    	plt.xlabel('Letters in a word',fontsize=45)
    	plt.xticks(fontsize=45)
    	plt.yticks(fontsize=45)
    	plt.title(key,fontsize=45)
    	plt.savefig(os.getcwd()+'/duplication/'+key+'/#lettersVSDuplicatedWords.png')
    	plt.cla()
    	plt.close(fig)
    	
    ######
    #for row in allwords:
    	#print(row)

	#### all possible duplicated words
    		
    twords.seek(0)
    numwords=[]
    allplayerwords=[]
    next(twords_reader)
    tsorted=sorted(twords_reader, key=operator.itemgetter(0,3))
    for key,items in groupby(tsorted,operator.itemgetter(0,3)):
    	for item in items:
    		lenword=len(item[5])
    		word=item[5]
    		allplayerwords.append([key[0],key[1],lenword,word,1])
    		isdup=0
    		for dup in allplayerwords:
    			if dup[0]==key[0] and dup[1]!=key[1] and dup[3]==word:
    				dup[4]=dup[4]+1
    				isdup=1
    		if 	isdup==1:
    			for dup in allplayerwords:
    				if dup[0]==key[0] and dup[1]==key[1] and dup[3]==word:
    					dup[4]=dup[4]+1		
    		
    #for row in allplayerwords:
    	#print(row)
    fig, ax = plt.subplots(figsize=(25, 15))
    cycol=cycle('bgrcmky')
    for key,items in groupby(allplayerwords,operator.itemgetter(0)):
    	labelx='Duplication Analysis'
    	x=[]
    	y=[]
    	xdup=[]
    	ydup=[]
    	sessionlabel=[]
    	coord=[]
    	#print(key)
    	for key1,items1 in groupby(items,key=operator.itemgetter(1)):
    		#print(key1)
    		myletters='^['
    		uletters.seek(0)
    		for lett in uletter_reader:
    			if lett[0]==key and lett[3]==key1: 
    				#myletters.append(lett[4])
    				myletters=myletters+lett[4].lower()
    		ltran.seek(0)
    		for lett in ltran_reader:
    			if lett[0]==key1 and lett[5]=='True': 
    				#myletters.append(lett[2])
    				myletters=myletters+lett[2].lower()
    		myletters=myletters+']+$'		
    		#print(myletters)
    		#letters=set(myletters)
    		#print(letters)
    		m = re.compile(myletters)
    		#mywords=[]
    		#for row in allplayerwords:
    		#	if row[0]==key and row[1]==key1 :
    		#		mywords.append(row[3])
    		words=[]
    		for row in allplayerwords:
    			if row[0]==key:# and row[4]>1:# and row[1]!=key1 :
    				#if row[3] not in words and row[3] not in mywords:
    				#present=0
    				#for word in words:
    					#if row[3]==word:
    						#present=1
    				#if present==0:
    				words.append(row[3])
    		#coord=[]

    		for word in words:
    			#print(word)
    			if (m.match(word) is not None) == True:
    				#print(word)
    				lenword=len(word)
    				present=0
    				for row in coord:
    					if row[0]==lenword:
    						row[1]=row[1]+1
    						present=1
    				if present==0:
    					coord.append([lenword,1])
    	for row in coord:
    		#print(row)
    		x.append(row[0])
    		y.append(row[1])
    		for dup in dupfraction:
    			#print(dup)
    			if dup[0]==key:
    				for index,xcoord in enumerate(dup[1]):
    					#print(xcoord)
    					if xcoord==row[0]:
    						dup[2][index]=float(dup[2][index]/row[1])
    	if len(coord)>0:
    		ax.plot(x, y, 'ro',ms=15, label=key, color=next(cycol))
    		#print(key)
    		#print(x)
    		#print(y)
    #print(dupfraction)
    	#x=[]
    	#y=[]
    ax.margins(0.05)
    	#allsessions=allsessions+key1+'-'
    	#if not os.path.exists(os.getcwd()+'/duplication/'+key):
    	#	os.makedirs(os.getcwd()+'/duplication/'+key)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('# Possible Words duplicated by team',fontsize=45)
    plt.xlabel('Letters in a word',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title('',fontsize=45)
    plt.savefig(os.getcwd()+'/duplication/#lettersVSpossibleDuplicates.png', format='png')
    plt.cla()
    plt.close(fig)
    
    ####
    
     ##### possible duplicated words
    twords.seek(0)
    numwords=[]
    allplayerwords=[]
    next(twords_reader)
    tsorted=sorted(twords_reader, key=operator.itemgetter(0,3))
    for key,items in groupby(tsorted,operator.itemgetter(0,3)):
    	for item in items:
    		lenword=len(item[5])
    		word=item[5]
    		allplayerwords.append([key[0],key[1],lenword,word,1])
    		isdup=0
    		for dup in allplayerwords:
    			if dup[0]==key[0] and dup[1]!=key[1] and dup[3]==word:
    				dup[4]=dup[4]+1
    				isdup=1
    		if 	isdup==1:
    			for dup in allplayerwords:
    				if dup[0]==key[0] and dup[1]==key[1] and dup[3]==word:
    					dup[4]=dup[4]+1		
    		
    #for row in allplayerwords:
    	#print(row)

    for key,items in groupby(allplayerwords,operator.itemgetter(0)):
    	labelx='Duplication Analysis'
    	fig, ax = plt.subplots(figsize=(25, 15))
    	cycol=cycle('bgrcmky')
    	x=[]
    	y=[]
    	xdup=[]
    	ydup=[]
    	sessionlabel=[]
    	#coord=[]
    	#print(key)
    	for key1,items1 in groupby(items,key=operator.itemgetter(1)):
    		#print(key1)
    		myletters='^['
    		uletters.seek(0)
    		for lett in uletter_reader:
    			if lett[0]==key and lett[3]==key1: 
    				#myletters.append(lett[4])
    				myletters=myletters+lett[4].lower()
    		ltran.seek(0)
    		for lett in ltran_reader:
    			if lett[0]==key1 and lett[5]=='True': 
    				#myletters.append(lett[2])
    				myletters=myletters+lett[2].lower()
    		myletters=myletters+']+$'		
    		#print(myletters)
    		#letters=set(myletters)
    		#print(letters)
    		m = re.compile(myletters)
    		#mywords=[]
    		#for row in allplayerwords:
    		#	if row[0]==key and row[1]==key1 :
    		#		mywords.append(row[3])
    		words=[]
    		for row in allplayerwords:
    			if row[0]==key: #and row[4]>1: and row[1]!=key1 :
    				#if row[3] not in words and row[3] not in mywords:
    				#present=0
    				#for word in words:
    					#if row[3]==word:
    						#present=1
    				#if present==0:
    				words.append(row[3])
    		coord=[]
    		for word in words:
    			#print(word)
    			if (m.match(word) is not None) == True:
    				#print(word)
    				lenword=len(word)
    				present=0
    				for row in coord:
    					if row[0]==lenword:
    						row[1]=row[1]+1
    						present=1
    				if present==0:
    					coord.append([lenword,1])
    		for row in coord:
    			#print(row)
    			x.append(row[0])
    			y.append(row[1])

    		if len(coord)>0:
    			ax.plot(x, y, 'ro',ms=15, label=key1, color=next(cycol))
    		x=[]
    		y=[]
    	ax.margins(0.05)
    	if not os.path.exists(os.getcwd()+'/duplication/'+key):
    		os.makedirs(os.getcwd()+'/duplication/'+key)
    	legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    	plt.ylabel('# Possible Words duplicated by team',fontsize=45)
    	plt.xlabel('Letters in a word',fontsize=45)
    	plt.xticks(fontsize=45)
    	plt.yticks(fontsize=45)
    	plt.title('',fontsize=45)
    	plt.savefig(os.getcwd()+'/duplication/'+key+'/#lettersVSpossibleDuplicates.png', format='png')
    	plt.cla()
    	plt.close(fig)
    	#print(key)
    	#print(x)
		#print(y)
    #print(dupfraction)
    	
    
    	#allsessions=allsessions+key1+'-'
    	
    
    
    ####
    fig, ax = plt.subplots(figsize=(25, 15))
    cycol=cycle('bgrcmky')
    for row in dupfraction:
    	ax.plot(row[1], row[2], 'ro',ms=15, label=row[0], color=next(cycol))

    ax.margins(0.05)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('#duplicated Words/#possible duplicated words',fontsize=45)
    plt.xlabel('Letters in a word',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title('',fontsize=45)
    plt.savefig(os.getcwd()+'/duplication/#lettersVSfractionDuplicates.png', format='png')
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
