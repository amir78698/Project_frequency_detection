class thread(threading.Thread): 
	def __init__(self, thread_ID, thread_name): 
		threading.Thread.__init__(self) 
		self.thread_ID = thread_ID 
		self.thread_name = thread_name 
	def run(self): 
		print(self.thread_name) 
		
thread1 = thread(100, "Welcome ") 
thread2 = thread(101, "to ") 
thread3 = thread(102, "Presize ") 

thread = [] 
thread.append(thread1) 
thread.append(thread2) 
thread.append(thread3) 

thread1.start() 
thread2.start() 
for thread in thread: 
	thread.join() 
	
thread3.start() 


print("Exit")