# -*- coding:utf-8 -*-


### V. Cedeno
### 15 august 2017.
### Take experiments letter transactions data
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
def getRequestsSent(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    count=0
    for row in reader:
    	if row[0]==player:
    		count=count+1
    return count

## ------------------------------
def getRepliesReceived(reader,player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    count=0
    score=0
    for row in reader:
    	if row[0]==player and row[5]=='True':
    		count=count+1
    		score=score+SCORES[row[2].lower()]
    return count,score

## ------------------------------
def getRequestsReceived(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    count=0
    for row in reader:
    	if row[1]==player:
    		count=count+1
    return count
    
## ------------------------------
def getRepliesSent(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    count=0
    for row in reader:
    	if row[1]==player and row[5]=='True':
    		count=count+1
    return count
 
## ------------------------------
def getInitialScore(reader, player):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    score=0
    for row in reader:
    	if row[3]==player:
    		score=score+SCORES[row[4].lower()]
    return score   

    
### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 3):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ltran = sys.argv[1]
    uletter = sys.argv[2]
    #twords = sys.argv[3]
    #ins = sys.argv[4]
    #anag = sys.argv[5]
    #pg = sys.argv[6]
    ### Command line arguments.
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
    if not os.path.exists(os.getcwd()+'/difi/all/variousValues'):
    	os.makedirs(os.getcwd()+'/difi/all/variousValues')
    #as csvfile
    tdifi=open('Contributions.csv','rt')
    
    difi_reader=csv.reader(tdifi,delimiter=',')
    
    letter_tran=open(ltran,'rt')
    ltran_reader=csv.reader(letter_tran,delimiter=',')
    
    user_letter=open(uletter,'rt')
    uletter_reader=csv.reader(user_letter,delimiter=',')
    
    #difi_reader=groupby(sorted(difi_reader), key=operator.itemgetter(0))
    labelx='DIFI Analysis'
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[7])
    			xall.append(row[3])
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[7])
    		xall.append(row[3])
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([-5,50])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/words-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[5])
    			xall.append(row[3])
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[5])
    		xall.append(row[3])
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-5,50])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/words-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[8])
    			xall.append(row[3])
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[8])
    		xall.append(row[3])
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/words-pggc.png')
    plt.cla()
    plt.close(fig)

    ###Letter Requests
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numrequest)
    			y.append(row[7])
    			xall.append(numrequest)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numrequest)
    		y.append(row[7])
    		xall.append(numrequest)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('Number of requests sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([0,7])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/requestsSent-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numrequest)
    			y.append(row[5])
    			xall.append(numrequest)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numrequest)
    		y.append(row[5])
    		xall.append(numrequest)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('Number of requests sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([0,7])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/requestsSent-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numrequest)
    			y.append(row[8])
    			xall.append(numrequest)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numrequest)
    		y.append(row[8])
    		xall.append(numrequest)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('Number of requests sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/requestsSent-pggc.png')
    plt.cla()
    plt.close(fig)

	###Letter Replies
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRepliesSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numreplies)
    			y.append(row[7])
    			xall.append(numreplies)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numreplies)
    		y.append(row[7])
    		xall.append(numreplies)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('Number of replies sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([0,7])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/repliesSent-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRepliesSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numreplies)
    			y.append(row[5])
    			xall.append(numreplies)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numreplies)
    		y.append(row[5])
    		xall.append(numreplies)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('Number of replies sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([0,7])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/repliesSent-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRepliesSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(numreplies)
    			y.append(row[8])
    			xall.append(numreplies)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(numreplies)
    		y.append(row[8])
    		xall.append(numreplies)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('Number of replies sent per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/repliesSent-pggc.png')
    plt.cla()
    plt.close(fig)

	###Fraction Letter Requests
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	if numrequest==0:
    		fraction=0
    	else:
    		fraction=numrequestBack/numrequest
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[7])
    			xall.append(fraction)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[7])
    		xall.append(fraction)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('replies received/requests sent',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([-0.1,1.1])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/fractionRequestsSent-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	if numrequest==0:
    		fraction=0
    	else:
    		fraction=numrequestBack/numrequest
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[5])
    			xall.append(fraction)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[5])
    		xall.append(fraction)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('replies received/requests sent',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-0.1,1.1])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/fractionRequestsSent-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	if numrequest==0:
    		fraction=0
    	else:
    		fraction=numrequestBack/numrequest
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[8])
    			xall.append(fraction)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[8])
    		xall.append(fraction)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('replies received/requests sent',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/fractionRequestsSent-pggc.png')
    plt.cla()
    plt.close(fig)
    
    ###Fraction Letter Replies
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRequestsReceived(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrepliesBack=getRepliesSent(ltran_reader,row[2])
    	if numreplies==0:
    		fraction=0
    	else:
    		fraction=numrepliesBack/numreplies
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[7])
    			xall.append(fraction)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[7])
    		xall.append(fraction)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('replies sent/requests received',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([-0.1,1.1])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/FractionRequestsReceived-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRequestsReceived(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrepliesBack=getRepliesSent(ltran_reader,row[2])
    	if numreplies==0:
    		fraction=0
    	else:
    		fraction=numrepliesBack/numreplies
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[5])
    			xall.append(fraction)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[5])
    		xall.append(fraction)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('replies sent/requests received',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-0.1,1.1])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/fractionRequestsReceived-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRequestsReceived(ltran_reader,row[2])
    	letter_tran.seek(0)
    	numrepliesBack=getRepliesSent(ltran_reader,row[2])
    	if numreplies==0:
    		fraction=0
    	else:
    		fraction=numrepliesBack/numreplies
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(fraction)
    			y.append(row[8])
    			xall.append(fraction)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(fraction)
    		y.append(row[8])
    		xall.append(fraction)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('replies sent/requests received',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/fractionRequestsReceived-pggc.png')
    plt.cla()
    plt.close(fig)

 ###Initial scrabble score
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(iscore)
    			y.append(row[7])
    			xall.append(iscore)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(iscore)
    		y.append(row[7])
    		xall.append(iscore)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('Initial Scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([2.5,15])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scrabbleScore-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(iscore)
    			y.append(row[5])
    			xall.append(iscore)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(iscore)
    		y.append(row[5])
    		xall.append(iscore)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('Inital scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([2.5,15])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scrabbleScore-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(iscore)
    			y.append(row[8])
    			xall.append(iscore)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(iscore)
    		y.append(row[8])
    		xall.append(iscore)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('Initial scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scrabbleScore-pggc.png')
    plt.cla()
    plt.close(fig)
    
    ###All scrabble score
    
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	allscore=iscore+score
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(allscore)
    			y.append(row[7])
    			xall.append(allscore)
    			yall.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(allscore)
    		y.append(row[7])
    		xall.append(allscore)
    		yall.append(row[7])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2-DIFI1',fontsize=35)
    plt.xlabel('All Scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-250,250])
    axes.set_xlim([4,21])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scoreAllLetters-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	allscore=iscore+score
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(allscore)
    			y.append(row[5])
    			xall.append(allscore)
    			yall.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(allscore)
    		y.append(row[5])
    		xall.append(allscore)
    		yall.append(row[5])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI2',fontsize=35)
    plt.xlabel('All scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([4,21])
    #axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scoreAllLetters-d2.png')
    plt.cla()
    plt.close(fig)
    #####
    ####
    tdifi.seek(0)
    x=[]
    y=[]
    xall=[]
    yall=[]
    allsessions='Sessions:'
    playerlabel=[]
    cycol=cycle('bgrcmky')
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	user_letter.seek(0)
    	iscore=getInitialScore(uletter_reader,row[2])
    	letter_tran.seek(0)
    	numrequestBack,score=getRepliesReceived(ltran_reader,row[2])
    	allscore=iscore+score
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		#allsessions=allsessions+sessionb+'-'
    		if idx==points-1:
    			x.append(allscore)
    			y.append(row[8])
    			xall.append(allscore)
    			yall.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(allscore)
    		y.append(row[8])
    		xall.append(allscore)
    		yall.append(row[8])
    		playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('PGGC',fontsize=35)
    plt.xlabel('All scrabble score',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    axes = plt.gca()
    #axes.set_ylim([-5,145])
    #axes.set_xlim([-5,50])
    axes.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/variousValues/scoreAllLetters-pggc.png')
    plt.cla()
    plt.close(fig)
    ###
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
