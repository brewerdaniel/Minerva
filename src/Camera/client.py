#!/usr/bin/python
# TCP client example
import socket,os,time,numpy
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("djb231.quns.cam.ac.uk", 12345))
k = ' '
size = 65536

def transfer(filename) :
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
	
    print "Data transfered."


strt=time.time()
i=1
while (time.time()-strt<=10) :
    transfer("cam.jpg")
    i+=1

print "FPS: ", i
