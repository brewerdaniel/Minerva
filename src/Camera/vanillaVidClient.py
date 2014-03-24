#!/usr/bin/python
# TCP client example
import socket,os,sys
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("10.0.1.8", 12345))
k = ' '
size = 1024
iter=0
for i in range(10) :
    client_socket.send("cam")
    fp = open("test"+str(i)+".jpg",'w')
    while True :
        strng = client_socket.recv(512)
	print strng
        if not strng:
	    print "Breaking... ", strng
            break
        fp.write(strng)
        print "A line"
    print "Does it get to here?"
    fp.close()
    print "Data Received successfully"
sys.exit()
#data = 'viewnior '+fname
#os.system(data)
