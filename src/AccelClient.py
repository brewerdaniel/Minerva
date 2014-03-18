#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import struct

s = socket.socket()         # Create a socket object
host = 'djb231.quns.cam.ac.uk'#socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service
s.connect((host, port))
for x in range(1000) :
    s.send("Hey")
    data=s.recv(1024)
    print struct.unpack('f'*(len(data)/4), data)

s.send("")

s.close                     # Close the socket when done
