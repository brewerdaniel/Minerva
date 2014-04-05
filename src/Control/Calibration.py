#!/usr/bin/env python
#
# Automatic 3 axis calibration.
# 
# This method of calibration is an extension of the 2D method described at
# http://www.fatquarterssoftware.com/downloads/AUTOCAL.pdf
# 
# Using this method you do not have to carefully find the minimum and maximum
# responses from the sensor. Just pick 6 reasonably distinct measurement
# sets and go.
# 
# This was originally extended in Oct. 2009 by David W. Schultz, Python conversion
# completed by Daniel J. Brewer, April 2014.
# 

import sys
import math
import numpy as np
import socket
import struct

# x, y, z are vectors of six measurements
# 
# Computes sensitivity and offset such that:
# 
# c = s * A + O
# 
# where c is the measurement, s is the sensitivity, O is the offset,
# and A is the field being measured  expressed as a ratio of the
# measured value to the field strength. aka a direction cosine.
# 
# A is what we really want and it is computed using the equation:
# 
# A = (c - O)/s
#

s = socket.socket()         # Create a socket object 
host = 'djb231.quns.cam.ac.uk'
port = 12345                # Reserve a port for your service.
s.connect((host, port))
Sens = np.zeros(3)
Offset = np.zeros(3)

def cal(x, y, z, S, O) :
    A = np.zeros(25).reshape((5, 5))
    f = np.zeros(5)
    X = np.zeros(5)
    for i in range(5):
        A[i][0] = 2.0*(x[i]-x[i+1])
        A[i][1] = y[i+1]*y[i+1]-y[i]*y[i]
        A[i][2] = 2.0*(y[i]-y[i+1])
        A[i][3] = z[i+1]*z[i+1]-z[i]*z[i]
        A[i][4] = 2.0*(z[i]-z[i+1])
        f[i] = x[i]*x[i]-x[i+1]*x[i+1]
    
    # Solve AX=f 
    X=np.linalg.solve(A, f)
        
    k1 = X[1]
    k2 = X[3]
    O[0] = X[0]
    O[1] = X[2]/k1
    O[2] = X[4]/k2

    S[0] = np.sqrt((x[5]-O[0])*(x[5]-O[0])+k1*(y[5]-O[1])*(y[5]-O[1])+k2*(z[5]-O[2])*(z[5]-O[2]))
    S[1] = np.sqrt(S[0] * S[0] / k1)
    S[2] = np.sqrt(S[0] * S[0] / k2)
    return 0

def netRec() :
    total = np.zeros(3)
    s.send("mag")
    data = s.recv(128)
    total += np.array(struct.unpack('f'*(len(data)/4), data))
    s.send("mag")
    data = s.recv(128)
    total += np.array(struct.unpack('f'*(len(data)/4), data))
    s.send("mag")
    data = s.recv(128)
    total += np.array(struct.unpack('f'*(len(data)/4), data))
    
    return total/3

def magCali() :
    mX, mY, mZ = netRec()

    X = np.array([mX/2, -748, 112, 746, 548, -440])
    Y = np.array([mY/2, 105, 815, 119, 93, 205])
    Z = np.array([mZ/2, 432, 387, -421, 680, -651])
    
    
    if not cal(X, Y, Z, Sens, Offset) :
        return np.array([(X[0]-Offset[0])/Sens[0],
                         (Y[0]-Offset[1])/Sens[1],
                         (Z[0]-Offset[2])/Sens[2]])

    else :
        return np.zeros(3)

def end() :
    s.send("")
    s.close
