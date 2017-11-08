import create_dictionary, TermFrequency,tokenization, multiprocessing, time, sys
from scipy.sparse import lil_matrix

def produce(file, q, numberofprocesses, dictionary, dictionarylength, slave):
	
	tokenization.tokenize(file, addToQueue, q )
	for i in range(0, numberofprocesses):
		q.put(None)
	print("becoming consumer")
	consume(q, dictionary, 0, dictionarylength, slave)
		
	
def consume(q, dictionary, i, dictionarylength, slave):

	buffersize = 1000
	local = TermFrequency.initializeTfMatrix(buffersize, dictionarylength)
	linenumber = 0	

	while True:

		lineset = q.get()
		if lineset is None:

			if(linenumber > 0):
				lock.acquire()
				slave.send((local,i))
				lock.release()
			
			slave.send(None)
			print(i, "is done")
			break

		tokens = lineset
		TermFrequency.getLines(tokens, dictionary, linenumber, local)
		linenumber += 1
		if(linenumber == buffersize):
			print(i, "sending")
			lock.acquire()
			slave.send((local,i))
			lock.release()
			local = TermFrequency.initializeTfMatrix(buffersize, dictionarylength)
			linenumber = 0

	

def addToQueue(tokens,linenumber,q):

	q.put(tokens)


if __name__ == "__main__":

	lock = multiprocessing.Lock()
	input_q = multiprocessing.Queue()
	master, slave = multiprocessing.Pipe(False)
	pool = []
	done = 0
	numberofprocesses = multiprocessing.cpu_count()
	numberofprocesses = 2
	print(numberofprocesses)
	dictionary = create_dictionary.getDictFromDisk('dict')
	dictionarylength = len(dictionary)
	# matrix = TermFrequency.initializeTfMatrix(dictionary["0"], dictionarylength)
	start = time.time()
	for i in range(0,numberofprocesses):

		if i == 0:
			process = multiprocessing.Process(target=produce, args=(sys.argv[1], input_q, numberofprocesses, dictionary, dictionarylength, slave))
		else:
			process = multiprocessing.Process(target=consume, args=(input_q, dictionary, i, dictionarylength, slave))
		
		process.start()
		pool.append(process)
	count = 0

	while True:

		local = master.recv()
		if local == None:

			done += 1
			print("dones",done)
			if done == numberofprocesses:
				break
		else:		
			print("recved", local[1])
			count +=1
			print(count * 1000)
			
	for t in pool:
		t.join()
	end = time.time() - start 	

	# print("Current size of tf matrix'",
 #          sys.getsizeof(matrix) / 1000, "Kbytes")
	print(end)
	
	




	