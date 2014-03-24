import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5005))
server_socket.listen(5)
import os


client_socket, address = server_socket.accept()
print "Conencted to - ",address,"\n"
while (1):
	data = client_socket.recv(1024)
	if data=="cam" :
        	img = open("/dev/shm/mjpeg/cam.jpg",'r')
        	while True:
            		strng = img.readline(512)
			if not strng:
                		break
			client_socket.send(strng)
		img.close()
	else :
		client_socket.close()
		exit()
	
