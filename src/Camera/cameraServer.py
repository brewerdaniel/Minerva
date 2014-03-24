#!/usr/bin/env python           # This file creates a python server for the XLoBorg interface

import socket
import time
from thread import *
import sys

# Initialise the socket
s = socket.socket()
host = ''
port = 5005

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
       elif client=="cam": 
          img = open("/dev/shm/mjpeg/cam.jpg",'r')
          while True:
             strng = img.readline(512)
             if not strng:
                break
           
             connection.sendall(strng)
          img.close()
       else :
          break
       
    # Exit loop
    connection.close()

while True:
   c, addr = s.accept()     # Establish connection with client.
   start_new_thread(dataThread,(c,))
   
s.close()                # Close the connection
