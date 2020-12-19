import socket
import sys

host = '192.168.43.81'
port = 8995
pop3client = socket.socket(socket.AP_INET, socket.SOCK_STREAM)

pop3client.connect((host,port))
print(pop3client.recv(1024).decode())

while True:
	print("Masukkan  command(USER|PASS|STAT|LIST|RETR|DELE|QUIT) : ")
	command = input('')
	pop3client.send(command.encode())
	
	response = pop3client.recv(1024).decode('utf-8')
	print(response)
	if command == "QUIT":
		break

pop3client.close()
