#!/usr/bin/python
# TCP client example
import socket,os,time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("10.0.1.8", 5005))
size = 1024

for x in range (1,10) :
    fname = "cam"
    client_socket.send(fname)
    fname = './'+fname+str(x)+".jpg"
    strt=time.time()
    fp = open(fname,'w')
    while True:
        strng = client_socket.recv(512)
	if not strng:
            break
	fp.write(strng)
    fp.close()
    print time.time()-strt
client_socket.send("")
client_socket.close()
exit()
 
