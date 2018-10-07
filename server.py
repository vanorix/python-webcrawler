from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib

class Queue:

  #Constructor creates a list
  def __init__(self):
      self.queue = list()

  #Adding elements to queue
  def enqueue(self,data):
      #Checking to avoid duplicate entry (not mandatory)
      if data not in self.queue:
          self.queue.insert(0,data)
          return True
      return False

  #Removing the last element from the queue
  def dequeue(self):
      if len(self.queue)>0:
          return self.queue.pop()
      return ("Queue Empty!")

  #Getting the size of the queue
  def size(self):
      return len(self.queue)

  #printing the elements of the queue
  def printQueue(self):
      return self.queue

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/SOII',)

class MyServer(SimpleXMLRPCServer):
	def serve_forever(self):
		self.quit = 0
		while not self.quit:
			self.handle_request()

#************************************************
g_queue = Queue() #Global queue

stub = 0 #global stub variable

server = MyServer(("localhost", 3000), requestHandler=RequestHandler)
#************************************************


def putWork(url, deepness, term):
    global g_queue
    g_queue.enqueue({'url': url, 'deepness': deepness, 'term': term })
    return True
    
server.register_function(putWork)

def getWork():
    global g_queue
    return g_queue.dequeue()

server.register_function(getWork)

server.serve_forever()  

# server.register_function(getWork)

# service = threading.Thread(target=server.serve_forever, name='Server')
# service.setDaemon(True)

# service.start()