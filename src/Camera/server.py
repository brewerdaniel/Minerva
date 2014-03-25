#!/usr/bin/env python           # This file creates a python server for the XLoBorg interface

import socket
import struct
import time
from thread import *
import math
import sys

# Initialise the socket
s = socket.socket()
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

print "\nNow listening on port", port

def dataThread(connection) :
    while True :

       client = connection.recv(1024)
       if not client :
          break
       elif client=="cam" :
    	  print "The following data was received - ",client
    	  print "Opening file - ",client
    	  strt=time.time()
    	  img = open("/dev/shm/mjpeg/cam.jpg",'r')
    	  while True:
              strng = img.readline(512)
              if not strng:
                  break
              connection.send(strng)
          img.close()
	  connection.send("end")
    	  print "Data sent successfully in ", time.time()-strt, "s"
       else :
          data=[1,1,1]
          buf = struct.pack('f'*len(data), *data)

       connection.sendall("end")
       
    # Exit loop
    connection.close()

while True:
   c, addr = s.accept()     # Establish connection with client.
   start_new_thread(dataThread,(c,))
   
s.close()                # Close the connection
