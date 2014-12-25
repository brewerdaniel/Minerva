#!/usr/bin/env python           # This file creates a python server for the XLoBorg interface

import socket, struct, time, math, sys, os, XLoBorg, re
from thread import *
from subprocess import call

# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

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

print "\nNow listening on port", port

def dataThread(connection) :
    while True :

       client = connection.recv(1024)
       if not client or client=="end" :
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
       elif client=="CPUtemp" :
          PUProcess = Popen(["cat","/sys/class/thermal/thermal_zone0/temp"],stdout=subprocess.PIPE)
          GPUProcess = Popen(["/opt/vc/bin/vcgencmd","measure_temp"],stdout=subprocess.PIPE)
          CPU, err = CPUProcess.communicate()
          GPU, err = GPUProcess.communicate()
          CPU = float(CPU)
          CPU /= 1000
          GPU = float(re.findall("\d+.\d+", GPU)[0])
          data=[CPU,GPU]
          buf = struct.pack('f*2', *data)

       connection.sendall(buf)
       
    # Exit loop
    connection.close()

while True:
   c, addr = s.accept()     # Establish connection with client.
   start_new_thread(dataThread,(c,))
   
s.close()                # Close the connection
