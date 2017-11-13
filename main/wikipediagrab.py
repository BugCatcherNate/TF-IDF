import wikipedia, comparestrings, create_dictionary as cd, Create_IDF as cidf

corpus = 'test'

def addtoCorpus(text, corpus):

	cd.singleAdd(corpus,text)
	cidf.singleConsume(corpus, text)


while True:
	subject = input("what would you like to test?:")
	text = wikipedia.summary(subject, sentences=2)
	print(text)
	addtoCorpus(text, corpus)
	userdef = input("Please define " + subject +" in your own words:")
	comparestrings.main(corpus, text, userdef)

