import tokenization
import sys
import pickle
import os.path


def createdictionary(tokens, dictionary):

	for word in tokens:
		count = len(dictionary) - 1


		if word not in dictionary:
			dictionary[word] = count
			
	dictionary["0"] += 1


def getDictFromDisk(dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    if os.path.isfile(dictionary):
     
        dict = pickle.load(open(dictionary, "rb"))
    else:
        
        dict = {}
        dict['0'] = 0

    return dict 


def saveDictToDisk(dict, dictname):

    dictionary = "../output/Dictionaries/" + dictname + ".p"

    pickle.dump(dict, open(dictionary, "wb"))


def main(dictname):

    dictionary = getDictFromDisk(dictname)
    for filename in os.listdir("../input"):
        if str(filename).endswith(".txt"):
            with open(os.path.join("../input", filename), 'r') as myfile:

                for line in myfile:

                    tokens = tokenization.tokenizeLine(line)

                    createdictionary(tokens, dictionary)

    print("Current size of dictionary '", dictname, "':",
          sys.getsizeof(dictionary) / 1000000, "Mbytes")
    print(len(dictionary))
    saveDictToDisk(dictionary, dictname)
    return dictionary


if __name__ == '__main__':

    main(sys.argv[1])
