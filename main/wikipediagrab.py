import wikipedia, comparestrings

corpus = 'test'
while True:
	subject = input("what would you like to test?:")
	text = wikipedia.summary(subject, sentences=2)
	print(text)
	userdef = input("Please define " + subject +" in your own words:")
	comparestrings.main(corpus, text, userdef)

