import re
import time
import string
import sys

ignore = str.maketrans(dict.fromkeys(string.punctuation))


def tokenizeFile(file, fun, *args):
    starttime = time.time()

    tokens = []

    with open(file, 'r') as myfile:

        for line in myfile:

            tokenizeLine(line, fun, *args)

    end = time.time() - starttime
    print("Tokenizaiton time", end)

def tokenizeLine(line, fun, *args):
	tokens = []
	line = line.split(" ")

	for word in line:

		word = (word.translate(ignore)).lower()
		if word.isalpha():
			tokens.append(word)
	fun(tokens, *args)


def getTokenList(token, tokens):

    tokens.append(token)



if __name__ == "__main__":

    tokens = []
    tokenize(sys.argv[1], getTokenList, tokens)
    print(tokens)
