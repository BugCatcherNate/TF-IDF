import tokenization
import sys
import pickle
import os.path


def createdictionary(tokens, dictionary, lines):

    notempty = False
    for word in tokens:
        count = len(dictionary)-1
        notempty = True
        if word not in dictionary:
            dictionary[word] = count
    if notempty == True:
        lines += 1
    return lines 	

def getDictFromDisk(dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    if os.path.isfile(dictionary):
     
        dict = pickle.load(open(dictionary, "rb"))
    else:
        
        dict = {}
        dict['0'] = 0

    return dict 

def singleAdd(dictname, line):

    dictionary = getDictFromDisk(dictname)
    count = dictionary['0']
   
    tokens = tokenization.tokenizeLine(line)

    count = createdictionary(tokens, dictionary, count)
    dictionary['0'] = count
   
    saveDictToDisk(dictionary, dictname)

def saveDictToDisk(dict, dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    pickle.dump(dict, open(dictionary, "wb"))


def main(dictname):

    dictionary = getDictFromDisk(dictname)
    count = dictionary['0']
    for filename in os.listdir("../input"):
        if str(filename).endswith(".txt"):
            with open(os.path.join("../input", filename), 'r') as myfile:

                for line in myfile:

                    tokens = tokenization.tokenizeLine(line)

                    count = createdictionary(tokens, dictionary, count)
    dictionary['0'] = count
  
    saveDictToDisk(dictionary, dictname)
    return dictionary


if __name__ == '__main__':

    main(sys.argv[1])
