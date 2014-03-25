#!/usr/bin/python
# TCP client example
import socket,os,time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("djb231.quns.cam.ac.uk", 12345))
k = ' '
size = 65536
iter=0

def transfer(filename) :
    iter = 0
    client_socket.send("cam")
    fp = open(filename,'w')
    while True:
        strng = client_socket.recv(size)
        if not strng[-3:]=='end' :
            fp.write(strng)
	else :
            strng = strng[:-3]
            fp.write(strng)
            fp.close()
            break

    print "Data Received successfully"


strt=time.time()
i=1
while (time.time()-strt<=1) :
    transfer("./test"+str(i)+".jpg")
    i+=1

print "FPS: ", i
