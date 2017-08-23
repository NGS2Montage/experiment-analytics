# -*- coding:utf-8 -*-

### V. Cedeno
### 06 august 2017.
### Take experiments letter transactions data
### and generate plot files to understand difi2-difi1.
### input files:
###     Letter_transactions file
###     
### output files:
### d1vsd2 Color by requests sent
### d1vsd2 Color by requests received
### d1vsd2 Color by replies sent
### d1vsd2 Color by replies received
### d1vsd2 Color by fraction requests
### d1vsd2 Color by fraction replies
### d1vsd2 Color by number of words
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
from matplotlib.colors import Normalize
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
##def getRequestsReceived(reader,player):
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
##def getRepliesReceived(reader, player):
def getRequestsReceived(reader,player):
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
    		score=score+SCORES[row[4]]
    return score   
    
### -----------------------------

        
### Start.
def main():
    if (len(sys.argv) != 2):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    ltran = sys.argv[1]
    #twords = sys.argv[2]
    #ins = sys.argv[3]
    #anag = sys.argv[4]
    #pg = sys.argv[5]
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
    
    letter_tran=open(ltran,'rt')
    ltran_reader=csv.reader(letter_tran,delimiter=',')
    
    next(difi_reader)
    maxWords=0
    for row in difi_reader:
    	if int(row[3])>maxWords:
    		maxWords=int(row[3])
####all d1d2 word color
    
    x=[]
    y=[]
    z=[]
    xall=[]
    yall=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    numsessions=1
    allsessions='Color by # of Words'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[4])
    			y.append(row[5])
    			xall.append(row[4])
    			yall.append(row[5])
    			playerlabel.append(numsessions)	
    			z.append(row[3])
    		#cmap, norm = from_levels_and_colors([0, 10, 20, 30, 40, 50], ['red', 'green', 'blue','cyan','magenta'])
    		cm = plt.cm.get_cmap('Blues')
    		labellegend=str(numsessions)+':'+sessionb
    		numsessions=numsessions+1
    		#print(labellegend)
    		sc=ax.scatter(x, y,c=z, vmin=0, vmax=maxWords,s=300,cmap=cm,label=labellegend)
    		#ax.scatter(x, y,c=z, cmap=cmap, norm=norm,s=300,label=labellegend)
    		#print(x)
    		#print(y)
    		#print(z)
    		x=[]
    		y=[]
    		z=[]
    	if idx<points-1:
    		x.append(row[4])
    		y.append(row[5])
    		z.append(row[3])
    		xall.append(row[4])
    		yall.append(row[5])
    		playerlabel.append(numsessions)
    	sessionb=session
    	
    
    for i, txt in enumerate(playerlabel):
    	ax.annotate(txt, (xall[i],yall[i]),fontsize=20)
    #sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #fig.colorbar(sm, pad=0.02)
    plt.colorbar(sc, pad=0.02)
    legend=ax.legend(loc='upper left',prop={'size':14}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('DIFI1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    #axes.margins(0.05)
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorWords.png')
    plt.cla()
    plt.close(fig)
    
    
    ####all d1d2 requests color
    
    x=[]
    y=[]
    z=[]
    xall=[]
    yall=[]
    requestfraction=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    numsessions=1
    allsessions='Color by # of Requests Sent'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest=getRequestsSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[4])			
    			y.append(row[5])
    			xall.append(row[4])
    			yall.append(row[5])
    			playerlabel.append(numsessions)	
    			z.append(numrequest)
    			#z.append(row[10])
    		#cmap, norm = from_levels_and_colors([0, 1, 2, 3, 4, 5, 6, 7], ['red', 'green', 'blue','cyan','magenta','yellow','orange'])
    		cm = plt.cm.get_cmap('Blues')
    		labellegend=str(numsessions)+':'+sessionb
    		numsessions=numsessions+1
    		#print(labellegend)
    		sc=ax.scatter(x, y,c=z, vmin=0, vmax=6,s=300,cmap=cm,label=labellegend)
    		#ax.scatter(x, y,c=z, cmap=cmap, norm=norm,s=300,label=labellegend)
    		requestfraction.append([sessionb,x,y,z])
    		#print(x)
    		#print(y)
    		#print(z)
    		x=[]
    		y=[]
    		z=[]
    	if idx<points-1:
    		x.append(row[4])
    		y.append(row[5])
    		#z.append(row[10])
    		z.append(numrequest)
    		xall.append(row[4])
    		yall.append(row[5])
    		playerlabel.append(numsessions)
    	sessionb=session
    	
    #print(requestfraction)
    for i, txt in enumerate(playerlabel):
    	ax.annotate(txt, (xall[i],yall[i]),fontsize=20)
    #sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #fig.colorbar(sm, pad=0.02)
    plt.colorbar(sc, pad=0.02)
    legend=ax.legend(loc='upper left',prop={'size':14}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('DIFI1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    #axes.margins(0.05)
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorRequestsSent.png')
    plt.cla()
    plt.close(fig)
    
    ####
    ####all d1d2 requests received color
    
    x=[]
    y=[]
    z=[]
    xall=[]
    yall=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    numsessions=1
    allsessions='Color by # of Replies Received'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numrequest,score=getRepliesReceived(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[4])			
    			y.append(row[5])
    			xall.append(row[4])
    			yall.append(row[5])
    			playerlabel.append(numsessions)	
    			z.append(numrequest)
    			#print(numrequest)
    			for req in requestfraction:
    				if req[0]==session:
    					for index,coord in enumerate(req[3]):
    						#print(req[3][index])
    						if req[3][index]>0 and req[1][index]==row[4]and req[2][index]==row[5]:
    							req[3][index]=float(numrequest/req[3][index])
    						#if req[3][index]>0:
    							#req[3][index]=float(numrequest/req[3][index])
    						
    					#req[3][index]=float(numrequest/coord)
    			#z.append(row[10])
    		#cmap, norm = from_levels_and_colors([0, 1, 2, 3, 4, 5, 6, 7], ['red', 'green', 'blue','cyan','magenta','yellow','orange'])
    		cm = plt.cm.get_cmap('Blues')
    		labellegend=str(numsessions)+':'+sessionb
    		numsessions=numsessions+1
    		#print(labellegend)
    		sc=ax.scatter(x, y,c=z, vmin=0, vmax=6,s=300,cmap=cm,label=labellegend)
    		#print(session)
    		#ax.scatter(x, y,c=z, cmap=cmap, norm=norm,s=300,label=labellegend)
    		#print(x)
    		#print(y)
    		#print(z)
    		x=[]
    		y=[]
    		z=[]
    	if idx<points-1:
    		x.append(row[4])
    		y.append(row[5])
    		#z.append(row[10])
    		z.append(numrequest)
    		#print(numrequest)
    		for req in requestfraction:
    			if req[0]==session:
    				for index,coord in enumerate(req[3]):
    					if req[3][index]>0 and req[1][index]==row[4]and req[2][index]==row[5]:
    						req[3][index]=float(numrequest/req[3][index])
    					#if req[3][index]>0:
    						#req[3][index]=float(numrequest/req[3][index])
    					#print(req[3][index])
    		xall.append(row[4])
    		yall.append(row[5])
    		playerlabel.append(numsessions)
    	sessionb=session
    	
    #print(requestfraction)
    
    for i, txt in enumerate(playerlabel):
    	ax.annotate(txt, (xall[i],yall[i]),fontsize=20)
    #sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #fig.colorbar(sm, pad=0.02)
    plt.colorbar(sc, pad=0.02)
    legend=ax.legend(loc='upper left',prop={'size':14}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('DIFI1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    #axes.margins(0.05)
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorRepliesReceived.png')
    plt.cla()
    plt.close(fig)
    
    ####all requests fraction
    
    fig, ax = plt.subplots(figsize=(25, 15))
    cm = plt.cm.get_cmap('Blues')
    for row in requestfraction:
    	#print(row)
    	sc=ax.scatter(row[1], row[2],c=row[3], vmin=0, vmax=1,s=300,cmap=cm,label=row[0])
    #ax.margins(0.05)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.colorbar(sc, pad=0.02)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI 2',fontsize=45)
    plt.xlabel('DIFI 1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title('Color by #Replies received/#Requests sent',fontsize=45)
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorFractionRequestsSent.png', format='png')
    plt.cla()
    plt.close(fig)
    
    
    ####all d1d2 replies sent
    
    x=[]
    y=[]
    z=[]
    xall=[]
    yall=[]
    repliesfraction=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    numsessions=1
    allsessions='Color by # of Replies Sent'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRepliesSent(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[4])
    			y.append(row[5])
    			xall.append(row[4])
    			yall.append(row[5])
    			playerlabel.append(numsessions)	
    			#z.append(row[11])
    			z.append(numreplies)
    		#cmap, norm = from_levels_and_colors([0, 1, 2, 3, 4, 5, 6, 7], ['red', 'green', 'blue','cyan','magenta','yellow', 'orange'])
    		#norm = MidpointNormalize(midpoint=3)
    		cm = plt.cm.get_cmap('Blues')
    		labellegend=str(numsessions)+':'+sessionb
    		numsessions=numsessions+1
    		#print(labellegend)
    		sc=ax.scatter(x, y,c=z, vmin=0, vmax=6,s=300,cmap=cm,label=labellegend)
    		#ax.scatter(x, y,c=z, cmap=plt.cm.seismic, norm=norm,s=300,label=labellegend)
    		repliesfraction.append([sessionb,x,y,z])
    		#print(x)
    		#print(y)
    		#print(z)
    		x=[]
    		y=[]
    		z=[]
    	if idx<points-1:
    		x.append(row[4])
    		y.append(row[5])
    		#z.append(row[11])
    		z.append(numreplies)
    		xall.append(row[4])
    		yall.append(row[5])
    		playerlabel.append(numsessions)
    	sessionb=session
    	
    for i, txt in enumerate(playerlabel):
    	ax.annotate(txt, (xall[i],yall[i]),fontsize=20)
    #sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #fig.colorbar(sm, pad=0.02)
    plt.colorbar(sc, pad=0.02)
    
    legend=ax.legend(loc='upper left',prop={'size':14}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('DIFI1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    #axes.margins(0.05)
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorRepliesSent.png')
    plt.cla()
    plt.close(fig)
    
    ####
    ####all d1d2 replies received
    
    x=[]
    y=[]
    z=[]
    xall=[]
    yall=[]
    playerlabel=[]
    cycol=cycle('bgrcmky')
    tdifi.seek(0)
    next(difi_reader)
    sessionb=''
    numsessions=1
    allsessions='Color by # of Requests Received'
    fig, ax = plt.subplots(figsize=(25, 15))
    points=len(list(difi_reader))
    tdifi.seek(0)
    next(difi_reader)
    for idx,row in enumerate(difi_reader):
    	session=row[0]
    	letter_tran.seek(0)
    	numreplies=getRequestsReceived(ltran_reader,row[2])
    	if session!=sessionb and sessionb!='' or idx==points-1:
    		if idx==points-1:
    			x.append(row[4])
    			y.append(row[5])
    			xall.append(row[4])
    			yall.append(row[5])
    			playerlabel.append(numsessions)	
    			#z.append(row[11])
    			z.append(numreplies)
    			for req in repliesfraction:
    				if req[0]==session:
    					for index,coord in enumerate(req[3]):
    						#print(req[3][index])
    						if req[3][index]>0 and req[1][index]==row[4]and req[2][index]==row[5]:
    							req[3][index]=float(numrequest/req[3][index])
    		#cmap, norm = from_levels_and_colors([0, 1, 2, 3, 4, 5, 6, 7], ['red', 'green', 'blue','cyan','magenta','yellow', 'orange'])
    		#norm = MidpointNormalize(midpoint=3)
    		cm = plt.cm.get_cmap('Blues')
    		labellegend=str(numsessions)+':'+sessionb
    		numsessions=numsessions+1
    		#print(labellegend)
    		sc=ax.scatter(x, y,c=z, vmin=0, vmax=6,s=300,cmap=cm,label=labellegend)
    		#ax.scatter(x, y,c=z, cmap=plt.cm.seismic, norm=norm,s=300,label=labellegend)
    		#print(x)
    		#print(y)
    		#print(z)
    		x=[]
    		y=[]
    		z=[]
    	if idx<points-1:
    		x.append(row[4])
    		y.append(row[5])
    		#z.append(row[11])
    		z.append(numreplies)
    		for req in repliesfraction:
    			if req[0]==session:
    				for index,coord in enumerate(req[3]):
    					#print(req[3][index])
    					if req[3][index]>0 and req[1][index]==row[4]and req[2][index]==row[5]:
    						req[3][index]=float(numrequest/req[3][index])
    		xall.append(row[4])
    		yall.append(row[5])
    		playerlabel.append(numsessions)
    	sessionb=session
    	
    for i, txt in enumerate(playerlabel):
    	ax.annotate(txt, (xall[i],yall[i]),fontsize=20)
    #sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #fig.colorbar(sm, pad=0.02)
    plt.colorbar(sc, pad=0.02)
    
    legend=ax.legend(loc='upper left',prop={'size':14}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI2',fontsize=45)
    plt.xlabel('DIFI1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title(allsessions,fontsize=45)
    
    
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    #axes.margins(0.05)
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorRequestsReceived.png')
    plt.cla()
    plt.close(fig)
    
    ####all replies fraction
    
    fig, ax = plt.subplots(figsize=(25, 15))
    cm = plt.cm.get_cmap('Blues')
    for row in repliesfraction:
    	#print(row)
    	sc=ax.scatter(row[1], row[2],c=row[3], vmin=0, vmax=1,s=300,cmap=cm,label=row[0])
    #ax.margins(0.05)
    axes = plt.gca()
    axes.set_ylim([-120,145])
    axes.set_xlim([-120,145])
    plt.plot( [-120,145],[-120,145] ,color='black')
    plt.colorbar(sc, pad=0.02)
    legend=ax.legend(loc='upper left',prop={'size':18}, bbox_to_anchor=(1.1, 0.5),markerscale=0)
    plt.ylabel('DIFI 2',fontsize=45)
    plt.xlabel('DIFI 1',fontsize=45)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.title('Color by #Replies sent/#Requests Received',fontsize=45)
    plt.savefig(os.getcwd()+'/difi/all/d1-d2ColorFractionRequestsReceived.png', format='png')
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
