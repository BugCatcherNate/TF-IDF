import re, time, string, sys

ignore = str.maketrans(dict.fromkeys(string.punctuation))

def tokenize(file, fun, *args):
	starttime = time.time()

	tokens = []

	with open(file, 'r') as myfile:

		for line in myfile:
	
			line = line.split(" ")

			for word in line:
				word = (word.translate(ignore)).lower()
				if word.isalpha():
					fun(word, *args)
			
				
	end = time.time() -starttime
	print("Tokenizaiton time", end)	

def getTokenList(token, tokens):

	tokens.append(token)
	

if __name__ == "__main__":

	tokens = []
	tokenize(sys.argv[1],getTokenList, tokens)
	print(tokens)



