import time
import numpy as np
import matplotlib.pyplot as plt

fig=plt.figure()
plt.axis([0,1000,0,1])

i=0
x=list()
y=list()

plt.ion()
plt.show()

tic=time.time()
niter=1000

while i<niter:
    temp_y=np.random.random()
    x.append(i)
    y.append(temp_y)
    plt.scatter(i,temp_y)
    i+=1
    plt.draw()

print "average FPS: %.2f" %(niter/(time.time()-tic))
