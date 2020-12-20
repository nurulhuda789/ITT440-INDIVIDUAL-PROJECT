import socket
import os
import sys
from function import * 
import time
def pop3server():

	
	host = ''
	port = 8995 #authentication port for POP

	# maximum timeout
	if len(sys.argv) == 3:
		maxTime = int(sys.argv[2]) * 60
	else:
		maxTime = 20 * 60

	
	pop3Server = socket.socket()
	pop3Server.bind((host, port))
	pop3Server.listen(5)
	print('Bersambung dengan port {}: {}'.format(host, port))

	# variables
	user = "huda"
	password = "huda789" 
	email = ["Hai Huda,\n Jom pergi bercuti ke Langkawi, \nAina", "Assalamualaikum, cik Huda. Anda dijemput hadir ke Majlis Hari Lahir Encik Mohd Amin pada tarikh 12 Julai 2021. Kehadiran cik amatlah dialu-alukan, \nSetiausaha ANEEQ SDN BHD", "Dear Huda, your order for phone case has arrived at Mylia Store"]
	lengthMessage = 0
	deleteMessage = []
	for message in email:
		lengthMessage += len(message)

	
	auth_stage = True
	user_auth = False
	
	while True:

		client, address = pop3Server.accept()
		print('Terima sambungan dari CLIENT {}:{}'.format(address[0], address[1]))
		client.send('######################SELAMAT DATANG KE POP3 SERVER#######################\n\nHAI NURUL HUDA\n'.encode())
		while True:

			try:
				client.settimeout(maxTime)
				
				reqClient = client.recv(1024).decode('utf8')
				
				if auth_stage:

					# user
					if reqClient[0:4] == 'USER':
						if reqClient[5:] == user:
							user_auth = True
							client.send("+OK huda".encode())
						else:
							client.send("-ERR tiada mailbox untuk {} ".format(reqClient).encode())

					# password
					elif reqClient[0:4] == 'PASS':
						if user_auth:
							if reqClient[5:] == password:
								auth_stage = False
								client.send("+OK {} Berjaya log in".format(user).encode())
							else:
								client.send("-ERR salah kata laluan".encode())
						else:
							client.send("-ERR masukkan user lagi sekali".encode())

					# error command
					else:
						client.send("-ERR salah command".encode())

				else:
					#  status
					if reqClient == "STAT":
						client.send("+OK {} {}".format(len(email), lengthMessage).encode())

					# list 
					elif reqClient.startswith("LIST"):
						list(client, reqClient, email)
					# retrieve 
					elif reqClient[0:4] == "RETR" and len(reqClient) > 5:
						retrieve(client, reqClient, email)

					# delete 
					elif reqClient[0:4] == "DELE" and len(reqClient) > 5:
						lengthMessage = delete(client, reqClient, email, lengthMessage, deleteMessage)

					# reset 
					elif reqClient == "RSET":
						for message in deleteMessage:
							email.append(message)
							lengthMessage += len(message)
						deleteMessage = []
						client.send("+OK maildrop ada  {} mesej ({} octets)".format(len(email), lengthMessage).encode())

					# quit
					elif reqClient == "QUIT":
						if lengthMessage == 0:
							client.send("+OK {}\'s Keluar dari POP3 Server (tiada mesej)".format(user).encode())
						else:
							client.send("+OK {}\'s Keluar dari POP3 Server ({} mesej)".format(user, len(email)).encode())
						break

					# error command
					else:
						client.send("-ERR salah command".encode())
	
			# inactivity timout occurs
			except socket.timeout:
				print("Client tak aktif")
				client.send("Inactivity Timeout".encode())
				break

		
		client.close()
		print("POP3 Server Close")
		auth_stage = True
		user_auth = False
		deleted = []
pop3server()
