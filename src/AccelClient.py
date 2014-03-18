#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import struct

s = socket.socket()         # Create a socket object
host = 'djb231.quns.cam.ac.uk'#socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
data=s.recv(1024)
s.close                     # Close the socket when done

print struct.unpack('f'*(len(data)/4), data)
