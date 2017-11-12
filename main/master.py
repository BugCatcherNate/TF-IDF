import create_dictionary, TermFrequency,tokenization, multiprocessing, time, sys, os
from scipy import sparse
import numpy as np

def produce(q, numberofprocesses, dictionary, dictionarylength, slave, buffersize, done_count):
	
	linenumber = 0
	lines = []
	buffersize = int(buffersize)

	for filename in os.listdir("../input"):
		
		if str(filename).endswith(".txt"):

			with open(os.path.join("../input", filename), 'r') as myfile:

				for line in myfile:
			
					lines.append(line)
					linenumber += 1
					q.put(line)
				
	for i in range(0, numberofprocesses):
		q.put(None)
	consume(q, dictionary, 0, dictionarylength, slave, done_count)
		
	
def consume(q, dictionary, i, dictionarylength, slave, done_count):

	localidf = np.zeros((dictionarylength), dtype = np.int)
	while True:
		
		lineset = q.get()
	
		if lineset is None:
			
			slave.put(localidf)
		
			print(i,"Sending")
			break
		else:
			TermFrequency.idf(lineset, dictionary, localidf)
			
def addToQueue(tokens,linenumber,q):

	q.put(tokens)

def reader(output_q, done_count, corpus, dictionarylength):

	idf = readIDF(corpus, dictionarylength)
	done = 0
	while True:

		B = output_q.get()
		idf = np.add(idf, B)
		done += 1
		if done == numberofprocesses -1:
			break
	saveIDF(idf, corpus)
	print("Current siave of idf matrix", (idf.nbytes)/ 1000000, "mbytes")

def resizeIDF(idf, dictionarylength):

	if dictionarylength > idf.size:
		toadd = dictionarylength - idf.size
		idf = np.hstack([idf, np.zeros((toadd), dtype = np.int)])
	return idf

def saveIDF(idf, corpus):

	idfname = "../output/Matrices/"+str(corpus)+"_idf"
	np.save(idfname, idf)
	
def readIDF(corpus, dictionarylength):

	idfname = "../output/Matrices/"+str(corpus)+"_idf.npy"

	try:
		idf = np.load(idfname)
		print("idfloadedsize", idf.size)
		idf = resizeIDF(idf, dictionarylength)
		print("After", idf.size)
	except:
		idf = np.zeros((dictionarylength), dtype = np.int)
	return idf

if __name__ == "__main__":

	lock = multiprocessing.Lock()
	input_q = multiprocessing.Queue()
	output_q = multiprocessing.Queue()
	done_count = multiprocessing.Value('i',0)
	pool = []
	corpus = sys.argv[1]
	numberofprocesses = int(sys.argv[3])
	print("Number of processes initialized:", numberofprocesses)
	dictionary = create_dictionary.getDictFromDisk(corpus)

	if not dictionary:
		print("Error: Dictionary", "'"+corpus+"'", "does not exist")
		print("Exiting")
		exit()
	buffersize = sys.argv[2]
	
	done = 0
	dictionarylength = len(dictionary)
	
	start = time.time()
	for i in range(0,numberofprocesses):

		if i == 0:
			process = multiprocessing.Process(target=produce, args=(input_q, numberofprocesses, dictionary, dictionarylength, output_q, buffersize, done_count))
		elif i == 1:
			process = multiprocessing.Process(target=reader, args=(output_q, done_count, corpus, dictionarylength))
		else:
			process = multiprocessing.Process(target=consume, args=(input_q, dictionary, i, dictionarylength, output_q, done_count))
		pool.append(process)
		
	for process in pool:
		process.start()
	for process in pool:
		process.join()
	end = time.time() - start 
	
	print(end)

	
	




	