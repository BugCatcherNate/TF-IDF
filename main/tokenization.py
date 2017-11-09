import re
import time
import string
import sys

ignore = str.maketrans(dict.fromkeys(string.punctuation))


def tokenize(file, fun, *args):

    starttime = time.time()

    linenumber = 0
    with open(file, 'r') as myfile:

        for line in myfile:
        	linenumber = tokenizeLine(line,linenumber, fun, *args)
        
    endtime = time.time() - starttime
    
    print("Time to create dictionary:",endtime)


def tokenizeLine(line):
	tokens = []
	line = line.split(" ")
	notempy = False
	for word in line:

		word = (word.translate(ignore)).lower()
		if word.isalpha():
			notempy = True
			tokens.append(word)
	return tokens


def getTokenList(token, tokens):

    tokens.append(token)



if __name__ == "__main__":

    tokens = []
    tokenize(sys.argv[1], getTokenList, tokens)
    print(tokens)
