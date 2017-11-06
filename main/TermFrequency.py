import create_dictionary as cd
import tokenization as tk
import sys
import time
import numpy as np
from scipy.sparse import lil_matrix


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
    print("Current size of tf matrix'",
          sys.getsizeof(matrix) / 1000000, "Mbytes")
    print(matrix[0])

def addToTfMatrix(element, linenumber, matrix):

	matrix[linenumber-1, element] += 1


def initializeTfMatrix(numberoflines, dictlength):


    matrix = lil_matrix((numberoflines, dictlength))
    print(matrix.shape)
    return matrix

if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])
    
