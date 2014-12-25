#!/usr/bin/env python

import socket, struct, time, math, sys
from thread import *
from subprocess import call

# Initialise the socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ''
port = 12345

# Try to bind the port to the process
try:
   s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Await connection.
s.listen(5)
number_of_connections=0

print "\nNow listening on port", port

def dataThread(connection) :
    global number_of_connections
    number_of_connections+=1
    while True :

       client = connection.recv(1024)
       if not client :
          break
       elif client=="cam" :
    	  img = open("/dev/shm/mjpeg/cam.jpg",'r')
    	  while True:
              strng = img.readline(65536)
              if not strng:
                  break
              connection.send(strng)
          img.close()

       connection.sendall("end")
       
    # Exit loop
    connection.close()
    number_of_connections-=1


call("sudo raspimjpeg -w 640 -h 360 -wp 512 -hp 384 -d 1 -q 25 -of /dev/shm/mjpeg/cam.jpg &", shell=True)
while True:
   c, addr = s.accept()     # Establish connection with client.
   start_new_thread(dataThread,(c,))
   print number_of_connections   

s.close()                # Close the connection
