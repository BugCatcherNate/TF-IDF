import wikipedia, os.path, hashlib, comparestrings, create_dictionary as cd, Create_IDF as cidf, pickle

corpus = 'test'

def addtoCorpus(text, corpus):

	cd.singleAdd(corpus,text)
	cidf.singleConsume(corpus, text)
def checktext(text, corpus):

	hexdictionary = "../output/Dictionaries/"+corpus+"_hash.p"

	if os.path.isfile(hexdictionary):
		hexdict = pickle.load(open(hexdictionary, "rb"))
	else:
		hexdict = []
	m = hashlib.md5()
	m.update(text.encode('utf-8'))
	key = m.hexdigest()
	if key not in hexdict:
		print("expanding corpus")
		addtoCorpus(text,corpus)
		hexdict.append(key)
		pickle.dump(hexdict, open(hexdictionary, "wb"))

		
while True:
	subject = input("what would you like to test?:")
	text = wikipedia.summary(subject, sentences=2)
	print(text)
	checktext(text, corpus)
	userdef = input("Please define " + subject +" in your own words:")
	comparestrings.main(corpus, text, userdef)

