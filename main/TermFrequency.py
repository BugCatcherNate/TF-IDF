import create_dictionary as cd
import tokenization as tk
import sys
import time
import numpy as np


def getLines(tokens, linenumber, dictionary, matrix):

    for token in tokens:
        if token in dictionary:
            element = dictionary[token]
            addToTfMatrix(element, linenumber, matrix)


def main(file, dictionaryname):

    starttime = time.time()
    dictionary = cd.getDictFromDisk(dictionaryname)
    matrix = initializeTfMatrix(dictionary["0"], len(dictionary))
    tk.tokenize(file, getLines, dictionary, matrix)
    end = time.time() - starttime
    print("Time for TF matrix:", end)


def addToTfMatrix(element, linenumber, matrix):
	#print(linenumber)
	if linenumber < 31081:

		matrix[linenumber, element] += 1


def initializeTfMatrix(numberoflines, dictlength):


    
    matrix = np.zeros((numberoflines, dictlength))
    print(matrix.shape)
    return matrix

if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])
    initializeTfMatrix(sys.argv[1])
