import time
from os import path
from socket import *
serverPort = 12556
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
while 1:
	serverSocket.listen(1)
	print('The server is servicing at', serverPort)
	connectionSocket, addr = serverSocket.accept()
	#print(addr)
	data = connectionSocket.recv(1024).decode()
	print(data)
	filename = (data.split('\n')[0]).split(' ')[1]
	print("File Requested: ", filename.strip('/'))
	#totalpath = "/home/student/PES1498/server"+filename # can be full path also
	totalpath = "server"+filename
	#print(totalpath)
	check = path.exists(totalpath)
	header = ''
	if(check == True):
		try:				
			f = open(totalpath, 'rb')
		except IsADirectoryError:
			f = open(totalpath + "/index.html", 'rb')
		response_data = f.read()
		f.close()
		header += 'HTTP/1.1 200 OK'
		time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		header += 'Date: {now}\n'.format(now=time_now)
		header += 'Server: Simple-Python-Server\n'
		header += 'Connection: close\n\n'
		response = header.encode() + response_data
	else:
		header += 'HTTP/1.1 404 Not Found'
		time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		header += 'Date: {now}\n'.format(now=time_now)
		header += 'Server: Simple-Python-Server\n'
		header += 'Connection: close\n\n'
		response = header.encode() + bytes("<html><body><center><h1>Error 404: File not found</h1></body></html>", 'utf-8')
	connectionSocket.send(response)
	connectionSocket.close()
serverSocket.close()

