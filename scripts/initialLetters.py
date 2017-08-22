# -*- coding:utf-8 -*-

### V. Cedeno
### 09 jul 2017.
### Take experiment 1 output data
### and generate output files for plotting.
### input files:
###     User_letters file
###     Time_spent file
###     Letter_transactions file
###		Neighbors file
###     
### output files:
### Histogram for the initial letter score per player
### Contributions file used by difi.oy script
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
import matplotlib.pyplot as plt

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
## ------------------------------
def getDropoutData(ireader,player_code,session_id):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    summary=open(session_id+'/Summary-Players.csv','rt')
    sum_reader=csv.reader(summary,delimiter=',')
    actions=0
    dropout=1
    for row in ireader:
    	if row[2] == player_code and row[4]=='anagrams' and row[5]=='Anagrams' and row[9]=='True':
    		dropout=0
    		for item in sum_reader:
    			if item[2]==player_code:
    				actions=1
    		if actions==0:
    			dropout=2
    return dropout

## ------------------------------
def getLetterData(ireader,player_code):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    letters=0
    for row in ireader:
    	if row[0] == player_code and row[5]=='False':
    		letters=letters+1
    return letters     
    
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
    if (len(sys.argv) != 6):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ### Command line arguments.
    user_letters = sys.argv[1]
    time_spent = sys.argv[2]
    letter_tran = sys.argv[3]
    neighbors = sys.argv[4]
    session_id=sys.argv[5]
    ### Echo inputs.
    print ("  input file containing team words (team_words file): ",user_letters)
    print ("  input file containing team words (time_spent file): ",time_spent)
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/'+session_id+'/'+'/session'):
    	os.makedirs(os.getcwd()+'/'+session_id+'/'+'/session')
    #as csvfile
    uletters=open(user_letters,'rt')
    tspent=open(time_spent,'rt')
    ltran=open(letter_tran,'rt')
    ne=open(neighbors,'rt')
    #as csvfile
    

    #dropout analysis#
    contribution=open('Dropout.csv', 'a+')
    
    
    letters_reader=csv.reader(uletters,delimiter=',')
    tspent_reader=csv.reader(tspent,delimiter=',')
    ltran_reader=csv.reader(ltran,delimiter=',')
    ne_reader=csv.reader(ne,delimiter=',')
    userletters=getSessionData(letters_reader,session_id)
	#sort data by user
    #user=sorted(userletters, key=operator.itemgetter(2))
    f=open(os.getcwd()+'/'+session_id+'/Initial-Letters-Score.csv', 'w')
    f.write('playerid,playercode,score,dropout,unansweredRequests,neighborsScore,possibleScore\n')
    x=[]
    xlabel=[]
    y=[]
    for index,row in enumerate(userletters):
    	if index==0:
    		playercode=row[3]
    		playerid=row[2]
    		score=0
    		nescore=0
    		pscore=0
    		id=row[0]
    		sizeIndex=len(userletters)-1
    	if playercode!=row[3] or sizeIndex==index:
    		tspent.seek(0)
    		dropout=getDropoutData(tspent_reader,playercode,session_id)
    		ltran.seek(0)
    		letters=getLetterData(ltran_reader,playercode)
    		if sizeIndex==index:
    			score=score+SCORES[row[4].lower()]
    		ne.seek(0)
    		for neigh in ne_reader:
    			if neigh[1]==playercode:
    				n1=neigh[2]
    				n2=neigh[3]
    		uletters.seek(0)
    		for lene in letters_reader:
    			if lene[3]==n1 or lene[3]==n2:
    				nescore=nescore+SCORES[lene[4].lower()]
    				#print(nescore)
    		f.write(str(playerid)+',')
    		f.write(str(playercode)+',')
    		f.write(str(score)+',')
    		f.write(str(dropout)+',')
    		f.write(str(letters)+',')
    		f.write(str(nescore)+',')
    		f.write(str(score+nescore)+'\n')
    		contribution.write(str(session_id)+','+str(playercode)+','+str(score)+','+str(dropout)+','+str(letters)+','+str(nescore)+','+str(score+nescore)+'\n')
    		x.append(playerid)
    		y.append(score)
    		xlabel.append(playerid+':'+playercode)
    		playercode=row[3]
    		playerid=row[2]
    		nescore=0
    		score=0
    		pscore=0
    	score=score+SCORES[row[4].lower()]
    	#print(playercode)
    plt.figure()
    width = .35
    ind = np.arange(len(y))
    plt.bar(ind, y, width=width)
    plt.gcf().subplots_adjust(bottom=0.35)
    plt.title('Session:'+id)
    plt.ylabel(str('Initial Letters Scrabble Score'))
    plt.xlabel(str('Players'))
    plt.xticks(ind + width / 2, xlabel,rotation='vertical')
    #plt.show()
    #plt.savefig(os.getcwd()+'/plot/'+id+'/NormScoreCDF.png')
    plt.savefig(os.getcwd()+'/'+session_id+'/'+'IniLettersScore.png')
    plt.cla()
	    
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
