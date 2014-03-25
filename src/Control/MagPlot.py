#!/usr/bin/env python

"""
Simple script to show the position of the XLoBorg sensor chip.
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

import socket               # Import socket module                                                                           
import struct

O=[[1,0,0],[0,1,0],[0,0,1]]

s = socket.socket()         # Create a socket object 
host = 'djb231.quns.cam.ac.uk'
port = 12345                # Reserve a port for your service.
s.connect((host, port))

<<<<<<< HEAD:src/MagPlot.py
iter=0
=======
>>>>>>> 3636f72200cfe3d7aedbc625dcf2328ba34345ce:src/Control/MagPlot.py

def netRec() :
  s.send("mag")
  data = s.recv(1024)
  return struct.unpack('f'*(len(data)/4), data)

<<<<<<< HEAD:src/MagPlot.py
averageHeading=netRec()

def update_lines(num, axes) :
  vals = list(netRec())
  print vals
  global averageHeading
  global iter
  #iter+=1
  for i in range(3) :
  #  average*=(iter-1)
  #  average+=current
  #  average/=iter
    vals[i]-=averageHeading[i]
    print vals[i], " ", averageHeading[i]

  print vals
  print "************************"
=======

average=[0,0,0]
averageNumber=8
print "Calibration:"
for i in range(averageNumber) :
  print "Position ",i+1
  data = np.array(netRec())
  average+=data
  #average[0]+=data[0]
  #average[1]+=data[1]
  #average[2]+=data[2]
  raw_input()

average=np.array(average)/averageNumber
print average

def update_lines(num, axes) :
  vals = netRec()
  vals-=average
>>>>>>> 3636f72200cfe3d7aedbc625dcf2328ba34345ce:src/Control/MagPlot.py
  vals/=np.sqrt(np.dot(vals,vals))
  print vals
  new_axes=[[vals[0],0,0],[0,vals[1],0],[0,0,vals[2]]]

  for line, axis in zip(axes, new_axes) :
    # NOTE: there is no.set_data() for 3 dim data..
    line.set_data([[0,vals[0]],[0,vals[1]]])
    line.set_3d_properties([0,vals[2]])
  return axes


# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
axes = [ax.plot([0], [0], [0])[0] for index in range(3)]

# Setting the axes properties
ax.set_xlim3d([-2.0, 2.0])
ax.set_xlabel('X')

ax.set_ylim3d([-2.0, 2.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-2.0, 2.0])
ax.set_zlabel('Z')

ax.set_title('Magnetometer Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 1000, fargs=[axes], interval=1, blit=False)

plt.show()

s.send("")
s.close