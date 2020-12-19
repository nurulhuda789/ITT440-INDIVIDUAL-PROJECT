def retrieve(client, reqClient, email):
	index = getIndex(reqClient, email)
	if index == -1:	
		client.send("-ERR message tidak wujud".encode())
	else:
		email = email[index] + "\n."
		client.send("+OK {} character \n{}".format(len(email), email).encode())

def list(client, reqClient, email):
	if len(reqClient) == 4:
		allMessage = ""
		for no, message in enumerate(email):
			no += 1
			line = str(no) + " " + str(len(message)) + "\n"
			allMessage += line
		client.send("+OK {} mesej \n{}.".format(len(email), allMessage).encode())

	else:
		index = getIndex(reqClient, email)
		if index == -1:
			client.send("-ERR mesej tidak wujud".encode())
		else:
			email = email[index]
			client.send("+OK {} {}".format(index + 1, len(email)).encode())
			

def delete(client,reqClient , email, size, deleteMessage):
	index = getIndex(reqClient, email)
	if index == -1:
		client.send("-ERR mesej tidak wujud".encode())
		return size
	else:
		client.send("+OK berjaya buang mesej".encode())
		message = email.pop(index)
		deleteMessage.append(message)
		return size - len(message)
	
def getIndex(reqClient, email):
	index = int (reqClient[5:]) - 1
	if index + 1 > len(email):
		return -1
	else:
		return index
