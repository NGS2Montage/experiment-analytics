# -*- coding:utf-8 -*-

### V. Cedeno
### 08 jul 2017.
### Take experiment 1 output data
### and generate output files for plotting.
### input files:
###     
### output files:
###     Output:
### 	Users interaction plot
###     


### Modification History
### --------------------


import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import groupby
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
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
    #user_words = sys.argv[1]
    session = sys.argv[1]
    timeend = sys.argv[2]
    duration = sys.argv[3]
    global begin
    begin=datetime.utcfromtimestamp(float(timeend)-int(duration))
    global end
    end=datetime.utcfromtimestamp(float(timeend))
    strbegin=str(begin.time())
    strend=str(end.time())
    ### Echo inputs.
    #print ("  input file containing team words (team_words file): ",user_words)
     
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/'+session+'/session'):
    	os.makedirs(os.getcwd()+'/'+session+'/session')
    #as csvfile
    uwords=open(os.getcwd()+'/'+session+'/PlayersInteraction.csv','rt')
    #as csvfile
    
    words_reader=csv.reader(uwords,delimiter=',')
    next(words_reader)
    words_reader=sorted(words_reader, key=operator.itemgetter(2),reverse=True)
    wordlabel=[]
    xlabel=[]
    xs=[]
    ys=[]
    #zs=[]
    #zdirs=[]
    sec=0
    j=0
    counter=0
    fig, ax = plt.subplots(figsize=(20, 10))
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 3))
    for index,row in enumerate(words_reader):
    	id=int(row[2])
    	#print(j)
    	if counter<int(duration):
    		xs.append(int(row[1]))
    	if sec==60 or sec==0:
    		if sec==60:
    			sec=0
    		if counter<int(duration):
    			xlabel.append(row[0].split(' ')[-1])
    		sec=sec+1	
    	else:
    		if counter<int(duration):
    			xlabel.append('')
    		sec=sec+1
    	if row[3]=='':
    		ys.append(np.nan)
    		#zs.append(np.nan)
    		wordlabel.append(np.nan)
    	if len(row[3])>=1:
    		ys.append(int(row[2]))
    		#zs.append(int(row[2]))	
    		if row[6]!='':
    			wordlabel.append(row[6]+' '+row[3])
    		else:
    			wordlabel.append(row[3])
    		#zdirs.append('x')
    	if j==int(duration)-1:
    		j=0
    		ax.scatter(xs,ys,s=2, label=row[2]+'-'+row[5]+'-'+row[4])
    		for i, txt in enumerate(wordlabel):
    			if isinstance(txt, str)== True:
    				if ' ' in txt: 
    					writetype,writeword=txt.split(" ")
    					if writetype=='1':
    						ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='red', rotation='vertical')
    					if writetype=='2':
    						ax.annotate(writeword, (xs[i],ys[i]),fontsize=18,color='green', rotation='vertical')
    				else:
    					ax.annotate(txt, (xs[i],ys[i]),fontsize=18, rotation='vertical')
    			else:
    				ax.annotate(txt, (xs[i],ys[i]),fontsize=18, rotation='vertical')
    		ys=[]
    		#xs=[]
    		wordlabel=[]
    	else:	
    		j=j+1
    	counter=counter+1
    #print(xs)
    #print(len(ys))
    #print(ys)
    #print(zs)
    #print(wordlabel)
    #print(len(xlabel))
    labelx='Analysis by second from game time: '+strbegin+'-'+strend
    legend=ax.legend(loc='upper left',prop={'size':10}, bbox_to_anchor=(1, 0.5))
    plt.gcf().subplots_adjust(bottom=0.35)
    plt.title(str(begin.date())+' Session:'+session,fontsize=35)
    plt.ylabel(str('Player id'), fontsize=35)
    plt.xlabel(labelx, fontsize=35)
    plt.xticks(xs, xlabel,fontsize=35)#rotation='vertical'
    plt.yticks(fontsize=35)
    #plt.show()
    plt.savefig(os.getcwd()+'/'+session+'/''Interaction.png')
    plt.cla()
    plt.close(fig)
	
    #zdirs=wordlabel
    #fig = plt.figure()
    #ax = fig.gca(projection='3d')
    #for word,zdir, x, y, z in zip(wordlabel,zdirs, xs, ys, zs):
    #	label = '%s' % (word)
    	#print(x)
    	#print(y)
    	#print(z)
    	#print(label)
    	#print(zdir)
    	#ax.text(x, y, z, label, zdir)
    	
    #ax.text(9, 0, 0, "red", color='red')
    #ax.text2D(0.05, 0.95, "2D Text", transform=ax.transAxes)
    
    #ax.set_xlim(0, 300)
    #ax.set_ylim(0, 70)
    #ax.set_zlim(0, 7)
    #ax.set_xlabel('X axis')
    #ax.set_ylabel('Y axis')
    #ax.set_zlabel('Z axis')
    
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
