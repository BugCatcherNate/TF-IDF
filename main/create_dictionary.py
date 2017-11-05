import time, tokenization, sys

def createdictionary(word, dictionary):

	count = len(dictionary)

	if word not in dictionary:
		
		dictionary[word] = count
		count += 1

def main(file):

	dictionary = {}
	tokenization.tokenize(file,createdictionary, dictionary)
	print("Created dictionary of size:", sys.getsizeof(dictionary)/1000000,"Mbytes")




if __name__ == '__main__':
	
	main(sys.argv[1])
	
	