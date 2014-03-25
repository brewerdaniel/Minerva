#!/usr/bin/env python           # This file creates a python server for the XLoBorg interface

import socket
import struct
import time
from thread import *
import math
import sys
import XLoBorg

# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

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
       elif client=="accel" :
          data = XLoBorg.ReadAccelerometer()
          time.sleep(0.0125)
          data=[x + y for x, y in zip(data, XLoBorg.ReadAccelerometer())]
          time.sleep(0.0125)
          data=[x + y for x, y in zip(data, XLoBorg.ReadAccelerometer())]
          data=[x/3 for x in data]
          buf = struct.pack('f'*len(data), *data)
       elif client=="mag" :
          data = XLoBorg.ReadCompassRaw()
          time.sleep(0.0125)
          data=[x + y for x, y in zip(data, XLoBorg.ReadCompassRaw())]
          time.sleep(0.0125)
          data=[x + y for x, y in zip(data, XLoBorg.ReadCompassRaw())]
          data=[x/3 for x in data]
          buf = struct.pack('f'*len(data), *data)
       elif client=="temp" :
          data = XLoBorg.ReadTemperature()
          time.sleep(0.0125)
          data+=XLoBorg.ReadTemperature()
          time.sleep(0.0125)
          data+=XLoBorg.ReadTemperature()
          data/=3.0
          buf = struct.pack('f', *data)
       else :
          data=[1,1,1]
          buf = struct.pack('f'*len(data), *data)

       connection.sendall(buf)
       
    # Exit loop
    connection.close()

while True:
   c, addr = s.accept()     # Establish connection with client.
   start_new_thread(dataThread,(c,))
   
s.close()                # Close the connection
