import create_dictionary, idf, TermFrequency,tokenization, multiprocessing, time, sys, os
from scipy import sparse
import numpy as np

def produce(q, numberofprocesses, dictionary, dictionarylength, slave, buffersize):
	
	linenumber = 0
	lines = []
	count = 0
	buffersize = int(buffersize)

	for filename in os.listdir("../input"):
		
		if str(filename).endswith(".txt"):

			with open(os.path.join("../input", filename), 'r') as myfile:

				for line in myfile:
			
					count += 1
					lines.append(line)
					linenumber += 1
					if linenumber == buffersize:
						q.put(lines)
						lines = []
						linenumber = 0
				q.put(lines)
				print(count)
	for i in range(0, numberofprocesses):
		q.put(None)
	print("becoming consumer")
	consume(q, dictionary, 0, dictionarylength, slave)
		
	
def consume(q, dictionary, i, dictionarylength, slave):

	local_collect = None
	linenumber = 0	
	count = 0
	while True:
		
		lineset = q.get()
	
		if lineset is None:
			
			slave.put(local_collect)
			slave.put(None)
			break

		local = TermFrequency.initializeTfMatrix(len(lineset), dictionarylength)
		for line in lineset:
			count += 1
			TermFrequency.getLines(line, dictionary, linenumber, local, len(lineset))
			linenumber += 1
		linenumber = 0
		if local_collect == None:
			local_collect = local
		else:
			local_collect = sparse.vstack((local_collect, local)) 
		
			
def addToQueue(tokens,linenumber,q):

	q.put(tokens)


if __name__ == "__main__":

	input_q = multiprocessing.Queue()
	outupt_q = multiprocessing.Queue() 
	pool = []
	dictionary = create_dictionary.getDictFromDisk(sys.argv[1])
	buffersize = sys.argv[2]
	print(len(dictionary))
	print(dictionary["0"])
	done = 0
	numberofprocesses = multiprocessing.cpu_count()
	dictionarylength = len(dictionary)
	
	start = time.time()
	for i in range(0,numberofprocesses):

		if i == 0:
			process = multiprocessing.Process(target=produce, args=(input_q, numberofprocesses, dictionary, dictionarylength, outupt_q, buffersize))
		else:
			process = multiprocessing.Process(target=consume, args=(input_q, dictionary, i, dictionarylength, outupt_q))
		
		process.start()
		pool.append(process)

	A = None
	idf = None
	while True:
		
		B = outupt_q.get()
		if B == None:
			done += 1
			if done == numberofprocesses:
				break
		if A == None:
			A = B
			print("Started")
			idf = A.getnnz(axis=0)
		elif B != None:
			A = sparse.vstack((A,B))
			idf = np.add(idf, B.getnnz(axis=0))
			

	print(A.get_shape())
	for t in pool:
		t.join()
	end = time.time() - start 	
	print("Current size of tf matrix'",
          (A.data.nbytes) / 1000000, "mbytes")
	print(idf)

	print(end)

	
	




	