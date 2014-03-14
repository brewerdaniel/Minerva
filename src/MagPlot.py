import numpy as np
import time
import matplotlib.pyplot as mplpp
from matplotlib.pylab import subplots,close
from matplotlib import cm

mplpp.switch_backend('TkAgg')  

def randomwalk(dims=(256,256,256),n=1,sigma=5,alpha=0.95,seed=1):
    """ A simple random walk with memory """

    r,c,d = dims
    gen = np.random.RandomState(seed)
    pos = gen.rand(3,n)*((r,),(c,),(d,))
    old_delta = gen.randn(3,n)*sigma

    while 1:

        delta = (1.-alpha)*gen.randn(3,n)*sigma + alpha*old_delta
        pos += delta
        for ii in xrange(n):
            if not (0. <= pos[0,ii] < r) : pos[0,ii] = abs(pos[0,ii] % r)
            if not (0. <= pos[1,ii] < c) : pos[1,ii] = abs(pos[1,ii] % c)
            if not (0. <= pos[2,ii] < d) : pos[2,ii] = abs(pos[2,ii] % d)
        old_delta = delta
        yield pos

def run(niter=1000,doblit=True):
    """
    Visualise the simulation using matplotlib, using blit for 
    improved speed
    """

    fig,ax = subplots(1,1)
    ax.set_aspect('equal')
    ax.set_xlim(0,255)
    ax.set_ylim(0,255)
    ax.hold(True)
    rw = randomwalk()
    x,y,z = rw.next()
    fig.canvas.draw()

    # cache the background
    background = fig.canvas.copy_from_bbox(ax.bbox)
    
    plt = ax.plot(x,y,'o')[0]
    #Axes3D.scatter
    tic = time.time()

    for ii in xrange(niter):

        # update the xy data
        x,y,z = rw.next()
        #Axes3D.scatter
        plt.set_data(x,y)
        
        # restore background
        fig.canvas.restore_region(background)
        
        # redraw just the points
        ax.draw_artist(plt)
        
        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)
        
    close(fig)
    print("Average FPS: %.2f" %(niter/(time.time()-tic)))
