#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import struct

# Load the XLoBorg library
import XLoBorg

# Tell the library to disable diagnostic printouts
XLoBorg.printFunction = XLoBorg.NoPrint

# Start the XLoBorg module (sets up devices)
XLoBorg.Init()

s = socket.socket()         # Create a socket object
host = ''#10.0.1.4'#socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print host, port
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   #print 'Got connection from', addr, c
   data = XLoBorg.ReadAccelerometer()
   buf = struct.pack('f'*len(data), *data)
   c.send(buf)
   c.close()                # Close the connection
