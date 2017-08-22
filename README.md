To run scripts:

Data folder (inputData)

sessionId: 1  	 

endTime: 1502215380 

duration: 304

===Script Name: words_requests_replies.py===

Input example:

python words_requests_replies.py TeamWords.csv LetterTransactions.csv UserLetters.csv instructions_anagrams.csv anagrams.csv public_goods.csv 1/60 1 1502215380 304

Output:
1) Summary-gbwspag3.csv: Game session statistics
2) Summary-Players.csv: Players session statistics
3) plot: Folder with combined timelines of words, request and replies for the session and each player(this folder will be used by the plots.py script)
4) PlayersInteraction.csv: (file used by the interaction.py script)
5) Contributions.csv: (file used by the difi1difi2.py script)

===Script Name: plots.py===

Input Example:
 
python plots.py 1 1502215380 304

Output:
1) Users interaction plot

==Script Name: interaction.py==
Input Example: 

python interaction.py 1 1502215380 304

Output:
Users interaction plot

===Script Name: initialLetters.py===

Input Example: 

python initialLetters.py UserLetters.csv TimeSpent.csv Lettertransactions.csv Neighbors.csv 1

Output:
1)Histogram for the initial letter score per player
2)Contributions file used by difi.oy script

===Script Name: difi1difi2.py===

Input Example: 

python difi.py Lettertransactions.csv

Output:
1)d1vsd2 Color by requests sent
2)d1vsd2 Color by requests received
3)d1vsd2 Color by replies sent
4)d1vsd2 Color by replies received
5)d1vsd2 Color by fraction requests
6)d1vsd2 Color by fraction replies
7)d1vsd2 Color by number of words

===Script Name: difiVariousValues.py===

Input Example:
 
python difiVariousValues.p Lettertransactions.csv UserLetters.csv

Output:
### x values: words, requests, replies, fraction requests, fraction replies, 
### scrabble score, all scrabble score, number of duplicated words
### y value: difi2-difi1
### y value: difi2
### y value: pggc

===Script Name: dropout.py===

Input Example: 

python dropout.py Neighbors.csv

Output:
1) initial scrabble score vs. dropout fraction
2) initial and all scrabble score vs. dropout fraction
3) dropout neighbors vs. dropout fraction

===Script Name: duplication.py===

Input Example: 

python duplication.py TeamWords.csv UserLetters.csv LetterTransactions.csv 

Output:
1) letters in a word vs. words duplicated by team (also by player)
2) letters in a word vs. words that could have been duplicated by team (also by player)
3) letters in a word vs. Fraction of words that the team could have duplicated

===Script Name: delta.py===


Input Example: 

update starttime list with session id and start time.

python delta.py TeamWords.csv LetterTransactions.csv 

Output:
1) delta time successive replies vs. count
2) delta time replies vs words+requests made by player
3) delta time replies vs words made by player

