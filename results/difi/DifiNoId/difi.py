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
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import glob

## ------------------------------
def plot(xvalues,yvalues,xlabel,ylabel,title):
    """
    	xvalues: x coordinates
    	yvalues: y coordinates
    	xlabel: x label string
    	ylabel: y label string
    	title: plot title string
    """
    x=[i+1 for i in range(len(xvalues))]
    plt.plot(x, yvalues)
    plt.ylabel(str(ylabel))
    plt.xlabel(str(xlabel))
    plt.xticks(x, xvalues, rotation='vertical')
    plt.title(str(title))
    plt.show()
    
### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 1):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
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
    if not os.path.exists(os.getcwd()+'/difi/all'):
    	os.makedirs(os.getcwd()+'/difi/all')
    #as csvfile
    tdifi=open('Contributions.csv','rt')
    
    difi_reader=csv.reader(tdifi,delimiter=',')
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
    		if not os.path.exists(os.getcwd()+'/difi/'+sessionb):
    			os.makedirs(os.getcwd()+'/difi/'+sessionb)
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
    ax.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/words-d2-d1.png')
    plt.cla()
    plt.close(fig)
    
    
    ###individual
    x=[]
    y=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		fig, ax = plt.subplots(figsize=(25, 15))
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[7])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    		plt.ylabel('DIFI2-DIFI1',fontsize=45)
    		plt.xlabel('Number of words per player',fontsize=45)
    		plt.xticks(fontsize=45)
    		plt.yticks(fontsize=45)
    		plt.title('Session:'+sessionb,fontsize=45)
    		ax.margins(0.05)
    		#for i, txt in enumerate(playerlabel):
    			#ax.annotate(txt, (x[i],y[i]),fontsize=45)
    		plt.savefig(os.getcwd()+'/difi/'+sessionb+'/'+'words-d2-d1.png')
    		plt.cla()
    		plt.close(fig)
    		x=[]
    		y=[]
    		playerlabel=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[7])
    	playerlabel.append(row[1])
    	sessionb=session    	
    
    
    
    
    ####
    x=[]
    xall=[]
    playerlabel=[]
    pggcontribution=[]
    pggalcont=[]
    allsessions='Sessions:'
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[3])
    			pggcontribution.append(row[8])
    			xall.append(row[3])
    			pggalcont.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, pggcontribution, 'ro',ms=15 , label=sessionb, color=next(cycol))
    		x=[]
    		pggcontribution=[]
    	if idx<points-1:
    		x.append(row[3])
    		pggcontribution.append(row[8])
    	xall.append(row[3])
    	pggalcont.append(row[8])
    	playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],pggalcont[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('Public Goods Game Contribution',fontsize=45)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    ax.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/pggContribution.png')
    plt.cla()
    plt.close(fig)
    
    
    ###individual pggContribution
    
    x=[]
    playerlabel=[]
    pggcontribution=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		fig, ax = plt.subplots(figsize=(25, 15))
    		if idx==points-1:
    			x.append(row[3])
    			pggcontribution.append(row[8])
    			playerlabel.append(row[1])
    		ax.plot(x, pggcontribution, 'ro',ms=15, label=sessionb, color=next(cycol))
    		legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    		plt.ylabel('Public Goods Game Contribution',fontsize=45)
    		plt.xlabel('Number of words per player',fontsize=45)
    		plt.xticks(fontsize=45)
    		plt.yticks(fontsize=45)
    		plt.title('Session:'+sessionb,fontsize=45)
    		ax.margins(0.05)
    		#for i, txt in enumerate(playerlabel):
    			#ax.annotate(txt, (x[i],pggcontribution[i]),fontsize=45)
    		plt.savefig(os.getcwd()+'/difi/'+sessionb+'/pggContribution.png')
    		plt.cla()
    		plt.close(fig)
    		x=[]
    		playerlabel=[]
    		pggcontribution=[]
    	if idx<points-1:
    		x.append(row[3])
    		pggcontribution.append(row[8])
    	playerlabel.append(row[1])
    	sessionb=session
    
    
    	
    
    ####
    
    x=[]
    y=[]
    xall=[]
    yall=[]
    playerlabel=[]
    allsessions='Sessions:'
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[4])
    			xall.append(row[3])
    			yall.append(row[4])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		x=[]
    		y=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[4])
    	xall.append(row[3])
    	yall.append(row[4])
    	playerlabel.append(row[1])
    	sessionb=session
    
    #for i, txt in enumerate(playerlabel):
    	#ax.annotate(txt, (xall[i],yall[i]),fontsize=45)
    	
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    plt.ylabel('DIFI1',fontsize=45)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    ax.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/words-d1.png')
    plt.cla()
    plt.close(fig)
    
    ###individual 
    
    x=[]
    y=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		fig, ax = plt.subplots(figsize=(25, 15))
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[4])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    		plt.ylabel('DIFI1',fontsize=45)
    		plt.xlabel('Number of words per player',fontsize=45)
    		plt.xticks(fontsize=45)
    		plt.yticks(fontsize=45)
    		plt.title('Session:'+sessionb,fontsize=45)
    		ax.margins(0.05)
    		#for i, txt in enumerate(playerlabel):
    			#ax.annotate(txt, (x[i],y[i]),fontsize=45)
    		plt.savefig(os.getcwd()+'/difi/'+sessionb+'/words-d1.png')
    		plt.cla()
    		plt.close(fig)
    		x=[]
    		y=[]
    		playerlabel=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[4])
    	playerlabel.append(row[1])
    	sessionb=session
    
    
    
    
    ####
    
    x=[]
    y=[]
    xall=[]
    yall=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    allsessions='Sessions:'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
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
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('Number of words per player',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    ax.margins(0.05)
    plt.savefig(os.getcwd()+'/difi/all/words-d2.png')
    plt.cla()
    plt.close(fig)
    
    ###individual 
    
    x=[]
    y=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		fig, ax = plt.subplots(figsize=(25, 15))
    		if idx==points-1:
    			x.append(row[3])
    			y.append(row[5])
    			playerlabel.append(row[1])
    		ax.plot(x, y, 'ro',ms=15, label=sessionb, color=next(cycol))
    		legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1, 0.5))
    		plt.ylabel('DIFI2',fontsize=45)
    		plt.xlabel('Number of words per player',fontsize=45)
    		plt.xticks(fontsize=45)
    		plt.yticks(fontsize=45)
    		plt.title('Session:'+sessionb,fontsize=45)
    		ax.margins(0.05)
    		#for i, txt in enumerate(playerlabel):
    			#ax.annotate(txt, (x[i],y[i]),fontsize=45)
    		plt.savefig(os.getcwd()+'/difi/'+sessionb+'/words-d2.png')
    		plt.cla()
    		plt.close(fig)
    		x=[]
    		y=[]
    		playerlabel=[]
    	if idx<points-1:
    		x.append(row[3])
    		y.append(row[5])
    	playerlabel.append(row[1])
    	sessionb=session

    ####
    
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
