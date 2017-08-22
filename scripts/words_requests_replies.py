# -*- coding:utf-8 -*-

### V. Cedeno
### 06 jun 2017.
### Take experiment 1 output data
### and generate output files for plotting.
### input files:
###     Team_words file
###     Letter_transactions file
###		User_letters file
###		Instructions_anagrams file
###		anagrams file
###		public_goods file
###     
### output files:
### Summary-gbwspag3.csv: Game session statistics
### Summary-Players.csv: Players session statistics
### plot: Folder with combined timelines of words, request and replies for the session and each player(this folder will be used by the plots.py script)
### PlayersInteraction.csv: (file used by the interaction.py script)###     


### Modification History
### --------------------

import sys
import os
import csv
import operator
from datetime import time, datetime, timedelta
from itertools import groupby
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
def getPlayerData(ireader,player_code):
    """
    	ireader: csv file
        session_code: the session_code we want the data from.
    """
    rows=[row for row in ireader if row[3] == player_code]
    return rows
    
## ------------------------------
def getDataPerKey(reader,column,key,timecolumn):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    if timecolumn==0:
    	rows=[row for row in reader if row[column] == key]
    else:
    	rows=[row for row in reader if row[column] == key and datetime.utcfromtimestamp(float(row[timecolumn])).time()>=begin.time() and datetime.utcfromtimestamp(float(row[timecolumn])).time()<=end.time()]
    return rows

## ------------------------------
def getDistancePerKey(reader,column,key,dcolumn):
    """
    	reader: csv file
    	column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    distance=''
    for row in reader:
    	if row[column] == key:
    		distance=row[dcolumn]
    		if distance=='':
    			distance='nan'
    return distance
       
## ------------------------------
def getTimeData(data,column,key,timecolumn):
    """
    	data: rows obtained from getDataPerKey to extract the timestamps
        column: the column we want the data from.
        key: for example session_code or participant_code.
    """
    rows=[datetime.utcfromtimestamp(float(row[timecolumn])) for row in data if row[column] == key and datetime.utcfromtimestamp(float(row[timecolumn])).time()>begin.time() and datetime.utcfromtimestamp(float(row[timecolumn])).time()<=end.time()]
    return rows
    
## ------------------------------
def get_key(d):
    """
    	d:timestamps
    """
    # group by 1 minutes
    if timegroup=='1':
    	#print("minutos")
    	k = d + timedelta(minutes=-(d.minute % 1)) 
    	return datetime(k.year, k.month, k.day, k.hour, k.minute,0)
    if timegroup=='1/60':
    	#print("segundos")
    	k = d + timedelta(seconds=-(d.second % 1)) 
    	return datetime(k.year, k.month, k.day, k.hour, k.minute,k.second)

## ------------------------------
def coordinates(times,name,type):
    """
    	times:timestamps we want to plot
    	name: string of the key (for example session_code or participant_code)
    	type: session or player
    """
    #group by minute
    g = groupby(sorted(times), key=get_key)
    f=open(type+'-'+name+'.csv', 'w')
    #x coordinates, day and time
    countKey=[]
    #y coordinates, number of occurrences in day and time
    count=[]
    for key, items in g:
    	countKey.append(str(key))
    	f.write(str(key)+',')
    	number=len(list(items))
    	count.append(number)
    	f.write(str(number)+'\n')
    f.close()
    return(countKey,count)

## ------------------------------
def wordsLetters(times,name,type):
    """
    	times:timestamps we want to plot
    	name: string of the key (for example session_code or participant_code)
    	type: session or player
    """	
    #group by minute
    sorted_input = sorted(times, key=operator.itemgetter(6))
    rows=[datetime.utcfromtimestamp(float(row[6])) for row in sorted_input if datetime.utcfromtimestamp(float(row[6])).time()>=begin.time() and datetime.utcfromtimestamp(float(row[6])).time()<=end.time()]
    g = groupby(rows, key=get_key)
    f=open(type+'-'+name+'.csv', 'w')
    f.write('timestamp,words,word,numberOfLetters,scrabbleScore\n')
    numword=0
    numlett=0
    scrascore=0
    last_key=begin
    for key, items in g:
    	#print(str(last_key))
    	#print(str(key))
    	if last_key:
    		while (key-last_key).seconds>1:
    			#print((key-last_key).seconds)
    			empty_key=last_key+timedelta(seconds=1)
    			#print(last_key)
    			f.write(str(empty_key)+',')
    			f.write('0,')	
    			f.write(',')
    			f.write('0,')	
    			f.write('0\n')
    			#yield(empty_key,[])
    			last_key=empty_key
    	#yield(key,items)
    	last_key=key
    	f.write(str(key)+',')
    	#if numgroups>1:
    	numLetters=0
    	numItems=0
    	score=0
    	#number=len(list(items))
    	word=''
    	for item in items:
    		numItems=numItems+1
    		numword=numword+1
    		for row in sorted_input:	
    			if item==datetime.utcfromtimestamp(float(row[6])):
    				numLetters=numLetters+len(row[5])
    				numlett=numlett+len(row[5])
    				score=score+scrabble_score(row[5])
    				scrascore=scrascore+scrabble_score(row[5])
    				if word!='':
    					word=word+'-'+row[5]
    				else:
    					word=row[5]
    				
    	#print(str(number))
    	#print(str(numItems))
    	number=numItems
    	f.write(str(number)+',')	
    	f.write(str(word)+',')
    	f.write(str(numLetters)+',')	
    	f.write(str(score)+'\n')
    if len(rows)>0 and key!=end-timedelta(seconds=1):
    	key=end
    	while (key-last_key).seconds>1:
    		#print((key-last_key).seconds)
    		empty_key=last_key+timedelta(seconds=1)
    		#print(last_key)
    		f.write(str(empty_key)+',')
    		f.write('0,')	
    		f.write(',')
    		f.write('0,')
    		f.write('0\n')
    		last_key=empty_key
    f.close()
    return(numword,numlett,scrascore)

## ------------------------------
def requestReplies(times,name,type):
    """
    	times:timestamps we want to plot
    	name: string of the key (for example session_code or participant_code)
    	type: session or player
    """	
    
    #group by minute
    sorted_input = sorted(times, key=operator.itemgetter(7))
    
    rows=[datetime.utcfromtimestamp(float(row[7])) for row in sorted_input]
    if len(rows)>0:
    	g = groupby(rows, key=get_key)
    	f=open(type+'-'+name+'.csv', 'w')
    	f.write('timestamp,requests,replies,playerRequest,letterRequest,playerReply,letterReply\n')
    	numreq=0
    	numrep=0
    	
    	actions=[]
    	last_key=begin
    	for key, items in g:
    		if last_key:
    			while (key-last_key).seconds>1:
    				#print((key-last_key).seconds)
    				empty_key=last_key+timedelta(seconds=1)
    				#print(last_key)
    				f.write(str(empty_key)+',')
    				#print(empty_key)
    				lettersreply=''
    				playersnamerep=''
    				playersnamereq=''
    				#for item in items:
    				replies=0
    				for row in sorted_input:	
    					if row[5]=='True':
    						if empty_key.strftime("%Y-%m-%d %H:%M:%S")==datetime.utcfromtimestamp(float(row[6])).strftime("%Y-%m-%d %H:%M:%S"):
    							#print(item)
    							replies=replies+1
    							if lettersreply!='':
    								lettersreply=lettersreply+'-'+row[2]
    							else:
    								lettersreply=row[2]
    							if playersnamerep!='':
    								playersnamerep=playersnamerep+'-'+row[1]
    							else:
    								playersnamerep=row[1]
    								
    							if playersnamereq!='':
    								playersnamereq=playersnamereq+'-'+row[0]
    							else:
    								playersnamereq=row[0]
    				f.write('0,')	
    				f.write(str(replies)+',')
    				f.write(str(playersnamereq)+',')	
    				f.write(',')
    				f.write(str(playersnamerep)+',')
    				f.write(str(lettersreply)+'\n')
    				#yield(empty_key,[])
    				last_key=empty_key
    		last_key=key
    		#print(key)
    		f.write(str(key)+',')
    		requests=0
    		replies=0
    		#number=len(list(items))
    		letters=''
    		lettersreply=''
    		playersnamereq=''
    		playersnamerep=''
    		for item in items:
    			requests=requests+1
    			numreq=numreq+1
    			for row in sorted_input:	
    				if item==datetime.utcfromtimestamp(float(row[7])):
    					#player=row[1]
    					if letters!='':
    						letters=letters+'-'+row[2]
    					else:
    						letters=row[2]
    					if playersnamereq!='':
    						playersnamereq=playersnamereq+'-'+row[0]
    					else:
    						playersnamereq=row[0]
    						
    					if playersnamerep!='':
    						playersnamerep=playersnamerep+'-'+row[1]
    					else:
    						playersnamerep=row[1]
    					if row[5]=='True':
    						replies=replies+1
    						numrep=numrep+1
    					if row[1]!='':
    						flag=0
    						for act in actions:
    							if act[0]==row[1]:
    								flag=1
    								act[1]=str(act[1])+str(row[2])
    								if row[5]=='True':
    									act[2]=str(act[2])+str(row[2])		
    						if flag==0:
    							if row[5]=='True':
    								actions.append([row[1],str(row[2]),str(row[2])])
    							else:
    								actions.append([row[1],str(row[2]),''])
    					
    				if row[5]=='True':
    					if empty_key.strftime("%Y-%m-%d %H:%M:%S")==datetime.utcfromtimestamp(float(row[6])).strftime("%Y-%m-%d %H:%M:%S"):
    						if lettersreply!='':
    							lettersreply=lettersreply+'-'+row[2]
    						else:
    							lettersreply=row[2]
    						if playersnamerep!='':
    							playersnamerep=playersnamerep+'-'+row[1]
    						else:
    							playersnamerep=row[1]
    			
    		#print(str(number))
    		#print(str(numItems))
    		number=requests
    		
    		f.write(str(number)+',')	
    		f.write(str(replies)+',')	
    		f.write(str(playersnamereq)+',')
    		f.write(str(letters)+',')
    		f.write(str(playersnamerep)+',')
    		f.write(str(lettersreply)+'\n')
    	if key!=end-timedelta(seconds=1):
    		key=end
    		while (key-last_key).seconds>1:
    			#print((key-last_key).seconds)
    			empty_key=last_key+timedelta(seconds=1)
    			#print(last_key)
    			f.write(str(empty_key)+',')
    			
    			lettersreply=''
    			playersnamerep=''
    			playersnamereq=''
    			#for item in items:
    			replies=0
    			for row in sorted_input:	
    				if row[5]=='True':
    					replies=replies+1
    					if empty_key.strftime("%Y-%m-%d %H:%M:%S")==datetime.utcfromtimestamp(float(row[6])).strftime("%Y-%m-%d %H:%M:%S"):
    						#print(item)
    						if lettersreply!='':
    							lettersreply=lettersreply+'-'+row[2]
    						else:
    							lettersreply=row[2]
    						if playersnamerep!='':
    							playersnamerep=playersnamerep+'-'+row[1]
    						else:
    							playersnamerep=row[1]
    								
    						if playersnamereq!='':
    							playersnamereq=playersnamereq+'-'+row[0]
    						else:
    							playersnamereq=row[0]
    								
    			f.write('0,')	
    			f.write(str(replies)+',')
    			f.write(str(playersnamereq)+',')	
    			f.write(',')
    			f.write(str(playersnamerep)+',')
    			f.write(str(lettersreply)+'\n')
    			last_key=empty_key
    	f.close()
    	return(numreq,numrep,actions)    
    else:
    	return(-1,-1,[])
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
    
## ------------------------------
def get_transactions(data):
    """
    	data: transaction data from letter_transactions file
    """
    rows=[row for row in data if not row[7].isalpha() and datetime.utcfromtimestamp(float(row[7])).time()>=begin.time() and datetime.utcfromtimestamp(float(row[7])).time()<=end.time()]
    return rows

### -----------------------------
### Start.
def main():
    if (len(sys.argv) != 11):
    	print ("  Error.  Incorrect usage.")
    	print ("  usage: exec infile outfile.")
    	print ("  Halt.")
    	quit()
    
    startTime = datetime.now()
    
    ### Command line arguments.
    team_words = sys.argv[1]
    letter_transactions = sys.argv[2]
    user_letters = sys.argv[3]
    instructions = sys.argv[4]
    anagrams = sys.argv[5]
    pgoods = sys.argv[6]
    global timegroup
    timegroup = sys.argv[7]
    session = sys.argv[8]
    timeend = sys.argv[9]
    duration = sys.argv[10]
    global begin
    begin=datetime.utcfromtimestamp(float(timeend)-int(duration)-1)
    global end
    end=datetime.utcfromtimestamp(float(timeend))
    
    #wordsSummary=[]
    #playerinfo=[]
    #playerid=''
    #playerLetters=''
    
    ### Echo inputs.
    print ("  input file containing team words (team_words file): ",team_words)
    print ("  input file containing game transactions (letter_transactions file): ",letter_transactions)
     
    ### Output files. 
    if not os.path.exists(os.getcwd()+'/'+session+'/session'):
    	os.makedirs(os.getcwd()+'/'+session+'/session')
    if not os.path.exists(os.getcwd()+'/'+session+'/plot'):
    	os.makedirs(os.getcwd()+'/'+session+'/plot')
    if not os.path.exists(os.getcwd()+'/'+session+'/player'):
    	os.makedirs(os.getcwd()+'/'+session+'/player')
    if not os.path.exists(os.getcwd()+'/'+session+'/player/words'):
    	os.makedirs(os.getcwd()+'/'+session+'/player/words')
    if not os.path.exists(os.getcwd()+'/'+session+'/player/requests-replies'):
    	os.makedirs(os.getcwd()+'/'+session+'/player/requests-replies')
    #if not os.path.exists(os.getcwd()+'/player/replies'):
    #	os.makedirs(os.getcwd()+'/player/replies')
    #as csvfile
    twords=open(team_words,'rt')
    transactions=open(letter_transactions,'rt')
    letters=open(user_letters,'rt')
    
    tinstructions=open(instructions,'rt')
    tanagrams=open(anagrams,'rt')
    tpgoods=open(pgoods,'rt')
    
    words_reader=csv.reader(twords,delimiter=',')
    tran_reader=csv.reader(transactions,delimiter=',')
    letters_reader=csv.reader(letters,delimiter=',')
    
    instructions_reader=csv.reader(tinstructions,delimiter=',')
    anagrams_reader=csv.reader(tanagrams,delimiter=',')
    pgoods_reader=csv.reader(tpgoods,delimiter=',')
	
	#group data by session
    sessions=groupby(sorted(words_reader), key=operator.itemgetter(0))
    for key, items in sessions:
    	if key==session:
        	twords.seek(0)
        	#get team_words by session
        	sessionRows=getDataPerKey(words_reader,0,str(key),6)
        	letterRows=getDataPerKey(letters_reader,0,str(key),0)
        	playerinfo=[]
        	playerletters=''
        	bid=0
        	bname=''
        	for idx,row in enumerate(letterRows):
        		rowid=row[2]
        		if (idx>0 and rowid!=bid):
        			playerinfo.append([bid,bname,playerletters])
        			playerletters=''
        		bid=row[2]
        		bname=row[3]
        		playerletters=playerletters+row[4]
        		if idx==len(letterRows)-1:
        			playerinfo.append([bid,bname,playerletters])
        		
        	#get times from each word by session
        	#times=getTimeData(sessionRows,0,str(key))
        	#creates coordinates and file for # words by session
        	#x,y=coordinates(times,str(key),'session/Words-Session')
        	summary=open(session+'/'+'Summary-'+str(key)+'.csv', 'w')

        	snumwords,snumlett,sscrascore=wordsLetters(sessionRows,str(key),session+'/'+'session/Words-Session')
        	
        	transactions.seek(0)
        	#get times from each transaction by session
        	times=get_transactions(tran_reader)
        	#creates coordinates and file for # transaction by session
        	sreq,srep,sactions=requestReplies(times,str(key),session+'/'+'session/Requests-Replies-Session')
        	
        	summary.write('Session,numberOfWords, numberOfLetters, ScrabbleScore,numberOfRequest,numberOfReplies\n')
        	summary.write(str(key)+','+str(snumwords)+','+str(snumlett)+','+str(sscrascore)+','+str(sreq)+','+str(srep)+'\n')
        	summary.close()
        	#transactions.seek(0)
        	#get transaction replies by session
        	#replies=getDataPerKey(tran_reader,5,'True')
        	#get times from each reply by session
        	#times=getTimeData(replies,5,'True')
        	#creates coordinates and file for # replies by session
        	#x,y=coordinates(times,str(key),'session/Replies-Session')
        	
        	fplot=open(session+'/'+'plot/Session-'+str(key)+'.csv', 'w')
        	fplot.write('timestamp,words,requests,replies,numberOfLetters,scrabbleScore,letterword,player,letterReply,playerReply\n')
        	with open(session+'/'+'session/Words-Session-'+str(key)+'.csv') as f1, open(session+'/'+'session/Requests-Replies-Session-'+str(key)+'.csv') as f2:
        		next(zip(f1, f2))
        		for x, y in zip(f1, f2):
        			ztime=x.split(',')[-5]
        			zwords=x.split(',')[-4]
        			zword=x.split(',')[-3]
        			zletters=x.split(',')[-2]
        			zscore=x.split(',')[-1].split('\n')[-2]

        			zrequests=y.split(',')[-6]
        			zreplies=y.split(',')[-5]
        			zplayers=y.split(',')[-4]
        			zletter=y.split(',')[-3]
        			zplayereply=y.split(',')[-2]
        			zletterreply=y.split(',')[-1].split('\n')[-2]
        			fplot.write(ztime+',')
        			fplot.write(zwords+',')
        			fplot.write(zrequests+',')
        			fplot.write(zreplies+',')
        			fplot.write(zletters+',')
        			fplot.write(zscore+',')
        			fplot.write(zletterreply+',')
        			fplot.write(zplayereply+',')
        			if zletter=='' and zword!='':
        				wletter=zword
        			if zletter!=''and zword=='':
        				wletter=zletter
        			if zletter==''and zword=='':
        				wletter=''
        			if zletter!=''and zword!='':
        				wletter=zletter+'-'+zword
        			fplot.write(wletter+',')
        			fplot.write(zplayers)
        			fplot.write('\n')
        	#get data to plot per player
        	players=groupby(sorted(sessionRows), key=operator.itemgetter(3))
        	
        	wordsSummary=[]
        	for player_code, player_words in players:
        		playerRows=getDataPerKey(sessionRows,3,str(player_code),6)
        		#times=getTimeData(playerRows,3,str(player_code))
        		#creates coordinates and file for # words by player
        		numwords,numlett,scrascore=wordsLetters(playerRows,str(player_code),session+'/'+'player/words/Words-Player')
        		#x,y=coordinates(times,str(player_code),'player/words/Words-Player')
        		wordsSummary.append([str(player_code),numwords,numlett,scrascore])
    transactions.seek(0)
    #group data by players
    next(tran_reader)
    players=groupby(sorted(tran_reader), key=operator.itemgetter(0))
    
    allplayers=open(session+'/'+'PlayersInteraction.csv', 'w')
    #type 1:request, 2:reply, 3 word
    allplayers.write('timestamp,x,playerid,action,playercode,initialLetters,type\n')
    
    summary=open(session+'/'+'Summary-Players.csv', 'w')
    summary.write('id,initialLetters,PlayerID,numberOfWords, numberOfLetters, ScrabbleScore,numberOfRequest,numberOfReplies,Neighbor1,RequestedLettersN1,ReceivedLettersN1,Neighbor2,RequestedLettersN2,ReceivedLettersN2\n')
       
    notconfile=0
    if not os.path.exists(os.getcwd()+'/Contributions.csv'):
    	notconfile=1
    contribution=open('Contributions.csv', 'a+')
    if notconfile==1:
    	contribution.write('session,playerid,playercode,numWords,d1,d2,d3,d2d1,pggcontribution,pggearning\n')
    	
    #Defi score analysis#
    
    
    for player_code, player_words in players:
    	
	#get times from each transaction by player
    	transactions.seek(0)
    	requests=getDataPerKey(tran_reader,0,str(player_code),7)
    	#get times from each reply by player
    	#times=getTimeData(requests,0,str(player_code))

    	#creates coordinates and file for # transaction by player
    	#x,y=coordinates(times,str(player_code),'player/requests/Requests-Player')
    	req,rep,actions=requestReplies(requests,str(player_code),session+'/'+'player/requests-replies/Requests-Replies-Player')
    	if req>=0:
    		numwords=0
    		numlett=0
    		scrascore=0
    		for summ in wordsSummary:
    			if str(player_code)==str(summ[0]):
    				numwords=int(summ[1])
    				numlett=int(summ[2])
    				scrascore=int(summ[3])
    		for info in playerinfo:
    			if info[1]==str(player_code):
    				playerid=info[0]
    				playerLetters=info[2]

    		neigh1=''
    		nlet1=''
    		receivedletters1=''
    		neigh2=''
    		nlet2=''
    		receivedletters2=''
    		for index,act in enumerate(actions):
    			if index==0:
    				neigh1=act[0]
    				nlet1=act[1]
    				receivedletters1=act[2]
    			if index==1:
    				neigh2=act[0]
    				nlet2=act[1]
    				receivedletters2=act[2]

    		
    		tinstructions.seek(0)
    		d1=getDistancePerKey(instructions_reader,1,player_code,18)
    		tanagrams.seek(0)
    		d2=getDistancePerKey(anagrams_reader,1,player_code,18)
    		tpgoods.seek(0)
    		d3=getDistancePerKey(pgoods_reader,1,player_code,19)
    		d2d1='nan'
    		if d2!='nan' and d1!='nan':
    			d2d1=int(d2)-int(d1)
    		tpgoods.seek(0)
    		pggcontribution=getDistancePerKey(pgoods_reader,1,player_code,17)
    		tpgoods.seek(0)
    		pggearning=getDistancePerKey(pgoods_reader,1,player_code,18)
    		
    		summary.write(str(session)+','+str(playerLetters)+','+str(player_code)+','+str(numwords)+','+str(numlett)+','+str(scrascore)+','+str(req)+','+str(rep)+','+str(neigh1)+','+str(nlet1)+','+str(receivedletters1)+','+str(neigh2)+','+str(nlet2)+','+str(receivedletters2)+'\n')
        	
    		contribution.write(str(session)+','+str(playerid)+','+str(player_code)+','+str(numwords)+','+str(d1)+','+str(d2)+','+str(d3)+','+str(d2d1)+','+str(pggcontribution)+','+str(pggearning)+'\n')
        	
    	#transactions.seek(0)
    	#get transaction replies by player
    	#replies=getDataPerKey(tran_reader,0,str(player_code))
    	#get times from each reply by player
    	#times=getTimeData(replies,5,'True')
    	#creates coordinates and file for # replies get by player
    	#x,y=coordinates(times,str(player_code),'player/replies/Replies-Player')
    	
    	if os.path.isfile(os.getcwd()+'/'+session+'/'+'/player/words/Words-Player-'+str(player_code)+'.csv'):
    		for info in playerinfo:
    			if info[1]==str(player_code):
    				playerid=info[0]
    				playerLetters=info[2]
    		fplot=open(session+'/'+'plot/Player-'+str(player_code)+'.csv', 'w')
    		fplot.write('timestamp,words,requests,replies,numberOfLetters,scrabbleScore,letterword,player,letterReply,playerReply\n')
    		with open(session+'/'+'player/words/Words-Player-'+str(player_code)+'.csv') as f1, open(session+'/'+'player/requests-replies/Requests-Replies-Player-'+str(player_code)+'.csv') as f2:
        		next(zip(f1, f2))
        		counter=0
        		
        		for x, y in zip(f1, f2):
        			ztime=x.split(',')[-5]
        			zwords=x.split(',')[-4]
        			zword=x.split(',')[-3]
        			zletters=x.split(',')[-2]
        			zscore=x.split(',')[-1].split('\n')[-2]

        			zrequests=y.split(',')[-6]
        			zreplies=y.split(',')[-5]
        			zplayers=y.split(',')[-4]
        			zletter=y.split(',')[-3]
        			zplayereply=y.split(',')[-2]
        			zletterreply=y.split(',')[-1].split('\n')[-2]
        			
        			fplot.write(ztime+',')
        			fplot.write(zwords+',')
        			fplot.write(zrequests+',')
        			fplot.write(zreplies+',')
        			fplot.write(zletters+',')
        			fplot.write(zscore+',')
        			
        			actionreply=''
        			if zletter=='' and zword!='':
        				wletter=zword
        			if zletter!=''and zword=='':
        				wletter=zletter
        				actionreply='1'
        			if zletter==''and zword=='':
        				wletter=''
        			if zletter!=''and zword!='':
        				wletter=zletter+'-'+zword
        				actionreply='1'
        			fplot.write(wletter+',')
        			fplot.write(zplayers+',')
        			
        			if wletter=='' and zletterreply!='':
        				wletter=zletterreply
        				actionreply='2'
        			if wletter!=''and zletterreply=='':
        				wletter=wletter
        			if wletter==''and zletterreply=='':
        				wletter=''
        			if wletter!=''and zletterreply!='':
        				wletter=zletterreply	
        				
        			fplot.write(zletterreply+',')
        			fplot.write(zplayereply)
        			fplot.write('\n')
        			
        			counter=counter+1
        			allplayers.write(ztime+','+str(counter)+','+playerid+','+wletter+','+str(player_code)+','+playerLetters+','+actionreply+'\n')
        			
    	else:
    		if os.path.isfile(os.getcwd()+'/'+session+'/'+'/player/requests-replies/Requests-Replies-Player-'+str(player_code)+'.csv'):
    			for info in playerinfo:
    				if info[1]==str(player_code):
    					playerid=info[0]
    					playerLetters=info[2]
    			fplot=open(session+'/'+'plot/Player-'+str(player_code)+'.csv', 'w')
    			fplot.write('timestamp,words,requests,replies,numberOfLetters,scrabbleScore,letterword,player\n')
    			r_reader=csv.reader(open(session+'/'+'player/requests-replies/Requests-Replies-Player-'+str(player_code)+'.csv','rt'),delimiter=',')
    			next(r_reader)
    			counter=0
    			for row in r_reader:
    				fplot.write(row[0]+',')
    				fplot.write('0,')
    				fplot.write(row[1]+',')
    				fplot.write(row[2]+',')
    				fplot.write('0,')
    				fplot.write('0,')
    				
    				actionreply=''
    				if(row[6]!='' and row[4]==''):
    					actionP=row[6]
    					actionreply='2'
    				if(row[6]=='' and row[4]!=''):
    					actionP=row[4]
    					actionreply='1'
    				if(row[6]!='' and row[4]!=''):
    					actionP=row[4]+row[6]
    				if(row[6]=='' and row[4]==''):
    					actionP=''
    				fplot.write(actionP+',')
    				fplot.write(row[3])
    				fplot.write('\n')
    				#print(actionP)
    				counter=counter+1
    				allplayers.write(str(row[0])+','+str(counter)+','+str(playerid)+','+str(actionP)+','+str(player_code)+','+playerLetters+','+actionreply+'\n')
        			
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
