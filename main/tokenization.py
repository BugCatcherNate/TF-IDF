import re, time, string, sys

ignore = str.maketrans(dict.fromkeys(string.punctuation))

def tokenize(file):
	starttime = time.time()

	tokens = []

	with open(file, 'r') as myfile:

		for line in myfile:
	
			line = line.split(" ")

			for word in line:
				word = (word.translate(ignore)).lower()
				if word.isalpha():
					tokens.append(word)
				
	end = time.time() -starttime
	print("Tokenizaiton time", end)			
	return tokens

if __name__ == "__main__":

	print(len(tokenize(sys.argv[1])))


