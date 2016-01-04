import socket
import sys


server_addr = ('127.0.0.1',5000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

sys.stdout.write(client.recv(1024))
sys.stdout.write('>>')

try:
	while True:
		msg = sys.stdin.readline()
		client.send(msg)
		pesan = client.recv(1024)
		sys.stdout.write(pesan)
		if "221" in pesan:
			#sys.stdout.write(pesan)
			client.close()
			sys.exit(0)
			break
		elif "530" in pesan:
			#sys.stdout.write(pesan)
			client.close()
			sys.exit(0)
		if "Entering Passive Mode" in pesan:
			p1 = int(pesan.split(',')[4])
			p2 = int(pesan.split(',')[5].split(')')[0])
			data_port = p1 * 256 + p2
			client1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client1.connect(('127.0.0.1',data_port))
			sys.stdout.write(client1.recv(1024))
		sys.stdout.write('>>')

except KeyboardInterrupt:
	client.close()
	
	sys.exit(0)
