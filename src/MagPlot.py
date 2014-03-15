"""
Simple script to show the position of the XLoBorg sensor chip.
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def update_lines(num, axes) :
  new_axes=[[1,num*0.01,0],[0,1,0],[0,num*0.01,1]]
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
