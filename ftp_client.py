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
		sys.stdout.write('>>')

except KeyboardInterrupt:
	client.close()
	sys.exit(0)
