import create_dictionary as cd
import tokenization as tk
import idf 
import sys
import time
import numpy as np
from scipy import sparse


def getLines(line, dictionary, linenumber, matrix, buffersize):
    
    line = tk.tokenizeLine(line)
    tokencount = len(line)
    for token in line:
        if token in dictionary:
            element = dictionary[token]
            # elements.append(element)
            incrementMatrix(element, linenumber, matrix, tokencount)
    # for element
  

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

def incrementMatrix(element,linenumber, matrix, factor):
    
    matrix[linenumber, element] += 1/factor


def initializeTfMatrix(numberoflines, length):


    matrix = sparse.lil_matrix((numberoflines, length), dtype='float')
    return matrix

if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])
    
