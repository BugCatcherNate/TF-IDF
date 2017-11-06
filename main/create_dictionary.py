import tokenization
import sys
import pickle
import os.path


def createdictionary(word, dictionary):

    count = len(dictionary)

    if word not in dictionary:

        dictionary[word] = count
        count += 1


def getDictFromDisk(dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    if os.path.isfile(dictionary):
     
        dict = pickle.load(open(dictionary, "rb"))
    else:
        
        dict = {}

    return dict 


def saveDictToDisk(dict, dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    pickle.dump(dict, open(dictionary, "wb"))


def main(file, dictname):

    dictionary = getDictFromDisk(dictname)
    tokenization.tokenize(file, createdictionary, dictionary)
    print("Current size of dictionary '", dictname, "':",
          sys.getsizeof(dictionary) / 1000000, "Mbytes")
    saveDictToDisk(dictionary, dictname)


if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])
