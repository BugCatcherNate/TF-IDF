import create_dictionary as cd
import tokenization as tk
import sys
import time
import numpy as np
from scipy import sparse


def getLines(line, dictionary, linenumber, matrix, buffersize):
    
    line = tk.tokenizeLine(line)
    for token in line:
        if token in dictionary:
            element = dictionary[token]
            incrementMatrix(element, linenumber, matrix)



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

def incrementMatrix(element,linenumber, matrix):
    
    matrix[linenumber,element] += 1

def addToTfMatrix(array, linenumber, matrix):

    array = np.asarray(array)
    np.insert(matrix, linenumber, array, axis=0)


def initializeTfMatrix(numberoflines, length):


    matrix = sparse.lil_matrix((numberoflines, length))
    return matrix

if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])
    
