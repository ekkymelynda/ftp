import socket
import select
import threading
import os 
import sys

allow_delete = False
currdir = os.path.abspath('.')

class ftpserver(threading.Thread):
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 5000
		self.backlog = 5
		self.size = 1024
		self.threads = []
		threading.Thread.__init__(self)

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)

	def run(self):
		self.open_socket()
		input = [self.server, sys.stdin]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(input, [], [])

			for s in inputready:
				if s == self.server:
					print s 
					c = ftpserverfunc(self.server.accept())
					c.start()
					self.threads.append(c)
				elif s == sys.stdin:
					junk = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()

class ftpserverfunc(threading.Thread):
	def __init__(self, (client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.basewd = currdir
		self.cwd = self.basewd
		self.rest = False
		self.pasv_mode = False
		self.size = 1024

	def run(self):
		self.client.send('220 Welcome!\r\n')
		while True:
			cmd = self.client.recv(self.size)
			if not cmd:
				break
			else:
				print 'recv: ',cmd
				try:
					func=getattr(self, cmd[:4].strip().upper())
					func(cmd)
				except Exception,e:
					print e
					self.client.send('500 Sorry.\r\n')

	def USER(self,cmd):
		self.client.send('331 OK.\r\n')
	def PASS(self,cmd):
		self.client.send('230 OK.\r\n')
	def QUIT(self,cmd):
		self.client.send('221 Goodbye.\r\n')

if __name__=='__main__':
	ftp = ftpserver()
	ftp.daemon = True
	ftp.start()
	raw_input('Enter to end...\n')
	ftp.stop() 

		