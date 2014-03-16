"""
Simple script to show the position of the XLoBorg sensor chip.
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Load the XLoBorg library
#import XLoBorg

# Tell the library to disable diagnostic printouts
#XLoBorg.printFunction = XLoBorg.NoPrint

# Start the XLoBorg module (sets up devices)
#XLoBorg.Init()
initPos=[0,0,0.9]#XLoBorg.ReadAccelerometer()

O=[[1,0,0],[0,1,0],[0,0,1]]

def xyzVals(num) :
  pos = [0.0, 0.4, 0.6]#XLoBorg.ReadAccelerometer()

  if (np.dot(pos,pos)>1) :
      pos/=np.dot(pos,pos)

  a, b = [-np.arcsin(pos[1]), np.arcsin(pos[0])]
  
  Rx=[[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]]
  Ry=[[np.cos(b),0,np.sin(b)],[0,1,0],[-np.sin(b),0,np.cos(b)]]
  #Rz=[[np.cos(c),-np.sin(c),0],[np.sin(c),np.cos(c),0],[0,0,1]]

  vals=np.dot(np.dot(O,Rx),Ry)

  return vals

def update_lines(num, axes) :
  new_axes=xyzVals(num)
  for line, axis in zip(axes, new_axes) :
    # NOTE: there is no.set_data() for 3 dim data..
    line.set_data([[0,axis[0]],[0,axis[1]]])
    line.set_3d_properties([0,axis[2]])
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

ax.set_title('Accelerometer Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 100, fargs=[axes], interval=1, blit=False)

plt.show()
