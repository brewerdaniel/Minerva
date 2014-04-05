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

# Load the XLoBorg library
import XLoBorg

# Tell the library to disable diagnostic printouts
XLoBorg.printFunction = XLoBorg.NoPrint

# Start the XLoBorg module (sets up devices)
XLoBorg.Init()

#==============================================================================
# return 1 if system not solving
# nDim - system dimension
# pfMatr - matrix with coefficients
# pfVect - vector with free members
# pfSolution - vector with system solution
# pfMatr becames trianglular after function call
# pfVect changes after function call
#==============================================================================
#
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

#
# Test data 
# 


mX, mY, mZ =  XLoBorg.ReadCompassRaw()


#X1 = np.array([np.fabs(mX), 2424, 2008, 1606, 1950, 2032])
#Y1 = np.array([np.fabs(mY), 2028, 1612, 2021, 2025, 1979])
#Z1 = np.array([np.fabs(mZ), 2059, 2038, 2046, 1622, 2437])
X1 = np.array([np.fabs(mX), -748, 112, 746, 548, -440])
Y1 = np.array([np.fabs(mY), 105, 815, 119, 93, 205])
Z1 = np.array([np.fabs(mZ), 432, 387, -421, 680, -651])

#
# Simple test of calibration code. Compute the calibration values
# for each series and then process each data point.
#




Sens = np.zeros(3)
Offset = np.zeros(3)

if cal (X1, Y1, Z1, Sens, Offset) == 0:
    
    x = (X1[0]-Offset[0])/Sens[0]
    y = (Y1[0]-Offset[1])/Sens[1]
    z = (Z1[0]-Offset[2])/Sens[2]
    
    print("%7.2f %7.2f %7.2f" % (x,y,z))

    print("%7.2f %7.2f %7.2f %10f" % (np.arccos (x) * 180/np.pi,
                                      np.arccos (y) * 180/np.pi,
                                      np.arccos (z) * 180/np.pi,
                                      np.sqrt(x*x + y*y + z*z)))
