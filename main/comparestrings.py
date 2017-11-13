import sys, create_dictionary as cd, TermFrequency as tf, Create_IDF as cidf, numpy as np
from scipy import sparse
from scipy import spatial as sp


def createTF(string, dictionary):

	matrix = tf.initializeTfMatrix(len(dictionary)-1)
	matrix = tf.getLines(string,dictionary,matrix)	
	return matrix

def cosDifference(A,B):

	return (1-sp.distance.cosine(A,B))*100

def tf_idf(matrix,idf):

	return np.multiply(matrix,idf)

def main(corpus, stringA, stringB):

	dictionary = cd.getDictFromDisk(corpus)
	dictionarylength = len(dictionary)-1
	linenumbers = dictionary["0"]
	if not dictionary:
		print("Error: Dictionary", "'"+corpus+"'", "does not exist")
		print("Exiting")
		exit()
	idf = cidf.readIDF(corpus, dictionarylength)
	vfunction = np.vectorize(cidf.normalizeIDF)
	idf = vfunction(idf,dictionarylength)
	if np.count_nonzero(idf) == 0:
		print("Error: IDF", "'"+corpus+"'", "does not exist")
		print("Exiting")
		exit()
	A = createTF(stringA, dictionary)
	B = createTF(stringB, dictionary)
	A = tf_idf(A, idf)
	B = tf_idf(B, idf)

	print("Strings are", cosDifference(A,B), "% similar")

if __name__ == '__main__':

	corpus = sys.argv[1]
	stringA = sys.argv[2]
	stringB = sys.argv[3]
	main(corpus,stringA, stringB)
