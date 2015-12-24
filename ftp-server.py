#Tes git
import socket
import select
import threading
import os 
import sys
import time

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
		self.running = True

	def run(self):
		self.client.send('220 Welcome my friend! :v\r\n')
		while self.running:
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
					self.client.send('500 Maaf, sepertinya Anda salah memasukkan sesuatu ._.\r\n')

	
	def USER(self,cmd):
		global flag
		flag = 0
		if cmd.strip().split()[1]=='tities':
			self.client.send('331 Buktikan kalau Anda memang my friend :D.\r\n')
		else:
			self.client.send('331 Buktikan kalau Anda memang my friend :D.\r\n')
			flag = 1
	def PASS(self,cmd):
		if flag == 1:
			self.client.send('530 Yah... Bukan my friend.... :(\r\n')
			#exit()
			self.client.send('Maaf harus menolak Anda.... :"\r\n')
			self.running = False
			self.client.close()
		elif cmd.strip().split()[1]=='namalengkapku':
			self.client.send('230 Huwaaaaaaw! Anda memang my friend :D\r\n')
		else:
			self.client.send('530 Yah... Bukan my friend....\r\n')
			#exit()
			self.client.send('Maaf harus menolak Anda.... :"\r\n')
			self.running = False
			self.client.close()
	def PWD(self,cmd):
		cwd=os.path.relpath(self.cwd,self.basewd)
		if cwd=='.':
			cwd='/'
		else:
			cwd='/'+cwd
		self.client.send('257 \"%s\"\r\n' % cwd)
	def CWD(self,cmd):
		chwd=cmd[4:-2]
		if chwd=='/':
			self.cwd=self.basewd
		elif chwd[0]=='/':
			self.cwd=os.path.join(self.basewd,chwd[1:])
		else:
			self.cwd=os.path.join(self.cwd,chwd)
		self.client.send('250 Sudah diganti my friend ;)\r\n')
	def QUIT(self,cmd):
		self.client.send('221 Goodbye my friend.... :"\r\n')

	#Mengganti nama file (RNTO: 4.1.3)
	def RNTO(self,cmd):
	        fn=os.path.join(self.cwd,cmd[5:-2])
	        os.rename(self.rnfn,fn)
	        self.conn.send('250 File renamed.\r\n')
	def RNFR(self,cmd):
        	self.rnfn=os.path.join(self.cwd,cmd[5:-2])
        	self.conn.send('350 Ready.\r\n')
        
        # Membuat direktori (MKD: 4.1.3)	
        def MKD(self,cmd):
	        dn=os.path.join(self.cwd,cmd[4:-2])
	        os.mkdir(dn)
	        self.conn.send('257 Directory created.\r\n')
        
        # Mendaftar file dan direktori (LIST: 4.1.3)
        def LIST(self,cmd):
	        self.conn.send('150 Here comes the directory listing.\r\n')
	        print 'list:', self.cwd
	        self.start_datasock()
	        for t in os.listdir(self.cwd):
	            k=self.toListItem(os.path.join(self.cwd,t))
	            self.datasock.send(k+'\r\n')
	        self.stop_datasock()
	        self.conn.send('226 Directory send OK.\r\n')
	        
	# HELP: 4.1.3
	def HELP(self,cmd):
		self.conn.send('214-The following commands are recognized:\r\nABOR\r\n ADAT\r\nALLO\r\nAPPE\r\nAUTH\r\nCDUP\r\nCLNT\r\nCWD\r\nDELE\r\nEPRT\r\nEPSV\r\nFEAT\r\nHASH\r\nHELP\r\nLIST\r\nMDTM\r\n')
		

if __name__=='__main__':
	ftp = ftpserver()
	ftp.daemon = True
	ftp.start()
	raw_input('Enter to end...\n')
	#ftp.stop() 

		
