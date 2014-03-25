#!/usr/bin/python
# TCP client example
import socket,os,time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("djb231.quns.cam.ac.uk", 12345))
k = ' '
size = 1024

iter=0

#while(1):
def transfer(filename) :
    iter = 0
    client_socket.send("cam")
    fp = open(filename,'w')
    while True:
        strng = client_socket.recv(512)
	#print strng
        if (strng=="end"):
            break
            print "hmmm"	
        fp.write(strng)
	iter+=1

    fp.close()
    print "Data Received successfully"


strt=time.time()
for i in range(1,10) :
    transfer("./test"+str(i)+".jpg")

print time.time()-strt

#data = 'viewnior '+fname
#os.system(data)
