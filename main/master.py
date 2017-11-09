import create_dictionary, TermFrequency,tokenization, multiprocessing, time, sys
from scipy import sparse

def produce(file, q, numberofprocesses, dictionary, dictionarylength, slave):
	
	linenumber = 0
	lines = []
	buffersize = 2000
	count = 0
	with open(file, 'r') as myfile:

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
			
			
			print(i, "finished at", count)
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
	done = 0
	numberofprocesses = multiprocessing.cpu_count()
	print(numberofprocesses)
	dictionary = create_dictionary.getDictFromDisk('dict')
	dictionarylength = len(dictionary)
	print(dictionary["0"])
	# matrix = TermFrequency.initializeTfMatrix(dictionary["0"], dictionarylength)
	start = time.time()
	for i in range(0,numberofprocesses):

		if i == 0:
			process = multiprocessing.Process(target=produce, args=(sys.argv[1], input_q, numberofprocesses, dictionary, dictionarylength, outupt_q))
		else:
			process = multiprocessing.Process(target=consume, args=(input_q, dictionary, i, dictionarylength, outupt_q))
		
		process.start()
		pool.append(process)

	A = None
	while True:
		
		B = outupt_q.get()
		if B == None:
			done += 1
			if done == numberofprocesses:
				break
		if A == None:
			A = B
			print("Started")
		elif B != None:
			A = sparse.vstack((A,B))
			print("growing", A.get_shape())

	print(A.get_shape())
	print(A)
	for t in pool:
		t.join()
	end = time.time() - start 	

	print("Current size of tf matrix'",
          sys.getsizeof(A) / 1000, "Kbytes")
	print(end)
	
	




	