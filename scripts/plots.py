# -*- coding:utf-8 -*-

### V. Cedeno
### 06 jul 2017.
### Take experiment 1 output data
### and generate plot files.
### input files:
###     
### output files:
###      Users interaction plot
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
    if (len(sys.argv) != 4):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ### Command line arguments.
    session = sys.argv[1]
    timeend = sys.argv[2]
    duration = sys.argv[3]
    global begin
    begin=datetime.utcfromtimestamp(float(timeend)-int(duration))
    global end
    end=datetime.utcfromtimestamp(float(timeend))
    
    ### Echo inputs.
    #print ("  plots for session or player: ",type)
    #print ("  id of session or player ",id)
     
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/'+session+'/'+'/plot'):
    	os.makedirs(os.getcwd()+'/'+session+'/'+'/plot')
    #as csvfile
    path = os.fsencode(os.getcwd()+'/'+session+'/'+'/plot/*.csv')
    
    allwords=[]
    allwordsid=[]
    for filename in glob.glob(path):
	    #twords=open('Session-'+id+'.csv','rt')
	    type=str(filename).split('/')[-1].split('-')[-2]
	    id=str(filename).split('/')[-1].split('.csv')[-2]
	    
	    if not os.path.exists(os.getcwd()+'/'+session+'/'+'/plot/'+id):
    		os.makedirs(os.getcwd()+'/'+session+'/'+'/plot/'+id)
	    twords=open(filename,'rt')
	    words_reader=csv.reader(twords,delimiter=',')
	    words=[]
	    wordscd=[]
	    requests=[]
	    requestscd=[]
	    replies=[]
	    repliescd=[]
	    letters=[]
	    letterscd=[]
	    scrabble=[]
	    scrabblecd=[]
	    normscrabble=[]
	    normscrabblecd=[]
	    maxscrabble=0
	    wordscdv=0
	    requestscdv=0
	    repliescdv=0
	    letterscdv=0
	    scrabblecdv=0
	    normscrabblecdv=0
	    dates=[]
	    rereplies=[]
	    rerepliescd=[]
	    repliescdv=0
	    rerepliescdv=0
	    sec=0
	    next(words_reader)
	    for row in words_reader:
	    	words.append(str(row[1]))
	    	wordscd.append(str(int(row[1])+wordscdv))
	    	wordscdv=int(row[1])+wordscdv
	    	requests.append(str(row[2]))
	    	requestscd.append(str(int(row[2])+requestscdv))
	    	requestscdv=int(row[2])+requestscdv
	    	replies.append(str(row[3]))
	    	repliescd.append(str(int(row[3])+repliescdv))
	    	repliescdv=int(row[3])+repliescdv
	    	letters.append(str(row[4]))
	    	letterscd.append(str(int(row[4])+letterscdv))
	    	letterscdv=int(row[4])+letterscdv
	    	difference=int(row[2])-int(row[3])
	    	rereplies.append(difference)
	    	rerepliescd.append(str(difference+rerepliescdv))
	    	rerepliescdv=difference+rerepliescdv
	    	scrabble.append(str(row[5]))
	    	scrabblecd.append(str(int(row[5])+scrabblecdv))
	    	scrabblecdv=int(row[5])+scrabblecdv
	    	if int(row[5])>maxscrabble:
	    		maxscrabble=int(row[5])
	    	if sec==60 or sec==0:
	    		if sec==60:
	    			sec=0
	    		dates.append(str(row[0].split(' ')[-1]))
	    		sec=sec+1
	    	else:
	    		dates.append('')
	    		sec=sec+1
	    if maxscrabble==0:
	    	maxscrabble=1
	    for row in scrabble:
	    	norm=int(row[0])/maxscrabble
	    	normscrabble.append(norm)
	    	normscrabblecd.append(norm+normscrabblecdv)
	    	normscrabblecdv=norm+normscrabblecdv
	    	
	    if type=="Player":
	    		allwords.append([id,wordscd])
	    
	    labelx='Analysis by second from game time'+str(begin.time())+'-'+str(end.time())
	    x=[i+1 for i in range(len(dates))]
	    fig, ax = plt.subplots(figsize=(20, 10))
	    
	    ax.plot(x, words, 'k--',marker='o', label='#Words')
	    ax.plot(x, requests, 'bs--', label='#Requests')
	    ax.plot(x, replies, 'r^--', label='#Replies')
	    ax.plot(x, rereplies, 'r--',marker='o',color='y', label='#Requests-Replies')
	    #ax.plot(x, letters, 'k:',marker='o',color='g', label='#Letters')
	    #ax.plot(x, scrabble, 'k:',marker='o',color='m', label='Scrabble score')
	    box = ax.get_position()
	    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    #plt.plot(x, value)
	    plt.ioff()
	    plt.gcf().subplots_adjust(bottom=0.35)
	    axes = plt.gca()
	    ymin, ymax = axes.get_ylim()
	    axes.set_ylim([ymin,ymax+0.1])
	
	    plt.ylabel(str('Value'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)#rotation='vertical'
	    plt.title(str(begin.date())+' '+str(id))
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/WRR.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    plt.ioff()
	    ax.plot(x, wordscd, 'k--',marker='o', label='#Words CDF')
	    ax.plot(x, requestscd, 'bs--', label='#Requests CDF')
	    ax.plot(x, repliescd, 'r^--', label='#Replies CDF')
	    ax.plot(x, rerepliescd, 'r--',marker='o',color='y', label='#Requests-Replies CDF')
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    plt.gcf().subplots_adjust(bottom=0.35)
	    plt.ylabel(str('Value'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/WRRCDF.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    plt.ioff()
	    ax.plot(x, letters, 'k:',marker='o',color='g', label='#Letters')
	    ax.plot(x, scrabble, 'k:',marker='o',color='m', label='Scrabble score')
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    #plt.plot(x, value)
	    plt.gcf().subplots_adjust(bottom=0.35)
	    axes = plt.gca()
	    ymin, ymax = axes.get_ylim()
	    axes.set_ylim([ymin,ymax+0.1])
	    
	    plt.ylabel(str('Value'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/LettersScore.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    plt.ioff()
	    ax.plot(x, letterscd, 'k:',marker='o',color='g', label='#Letters CDF')
	    ax.plot(x, scrabblecd, 'k:',marker='o',color='m', label='#Scrabble score CDF')
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    plt.gcf().subplots_adjust(bottom=0.35)
	    plt.ylabel(str('Value'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/LettersScoreCDF.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    plt.ioff()
	    ax.plot(x, normscrabble, 'k:',marker='o',color='m', label='#Normalized Scrabble score')
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    plt.gcf().subplots_adjust(bottom=0.35)
	    plt.ylabel(str('Value'),fontsize=18)
	    axes = plt.gca()
	    ymin, ymax = axes.get_ylim()
	    axes.set_ylim([ymin,ymax+0.1])
	    
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/NormScore.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    plt.ioff()
	    ax.plot(x, normscrabblecd, 'k:',marker='o',color='m',label='#CDF Normalized score')
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    plt.gcf().subplots_adjust(bottom=0.35)
	    plt.ylabel(str('Value'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/'+id+'/NormScoreCDF.png')
	    plt.cla()
	    plt.close(fig)
	    
	    fig, ax = plt.subplots(figsize=(20, 10))
	    cycol=cycle('bgrcmk')
	    marker1='o'
	    marker2='x'
	    flagodd=0
	    for row in allwords:
	    	if flagodd<6:
	    		ax.plot(x, row[1], marker=marker1, label=row[0],color=next(cycol))
	    	else:
	    		ax.plot(x, row[1], marker=marker2, label=row[0],color=next(cycol))
	    	flagodd=flagodd+1
	    legend=ax.legend(loc='upper left',prop={'size':8}, bbox_to_anchor=(1, 0.5))
	    plt.gcf().subplots_adjust(bottom=0.35)
	    plt.ylabel(str('Total number of words'),fontsize=18)
	    plt.xlabel(str(labelx),fontsize=18)
	    plt.xticks(x, dates,fontsize=18)
	    plt.title(str(begin.date())+' '+id)
	    #plt.show()
	    plt.savefig(os.getcwd()+'/'+session+'/'+'/plot/AllPlayers.png')
	    plt.cla()
	    plt.close(fig)
    #as csvfile
    #if type=='player':
    	#transactions=open('player/words/Words-Player-'+id+'.csv','rt')
    	#tran_reader=csv.reader(transactions,delimiter=',') 	
    	
	    
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
