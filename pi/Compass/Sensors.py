# The sensors class for Minerva
#
# This class should interface all sorts of things
import time, math, sys, os, XLoBorg, re, threading
import RPi.GPIO as GPIO
import numpy as np
from thread import *
from subprocess import call
from gps import *

XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

#class Navigation(threading.Thread) :
#    def __init__(self) :
#        # Initialise the XLoBorg library
#        try :
#
#
#        except:
#            print "Whoops!"

def heading() :
    A = XLoBorg.ReadAccelerometer()
    M = XLoBorg.ReadCompassRaw()
    
    g = 9.81
    
        # hard iron estimate
    Vx, Vy, Vz = (-618, 700.00, 1427.00)
    
        # tilt-compensated e-Compass code
    Ax, Ay, Az = A
    Mx, My, Mz = M
    Ax *= g
    Ay *= g
    Az *= g
    
        # subtract the hard iron offset
    Mx -= Vx    # see Eq 16
    My -= Vy    # see Eq 16
    Mz -= Vz    # see Eq 16
    
        # calculate current roll angle
    roll = math.atan2(Ay, Az)    # Eq 13
    roll_d = 180*roll/math.pi
    #print roll_d
    
        # calculate sin and cosine of roll angle Phi
    sin_roll = math.sin(roll)    # Eq 13: sin = opposite / hypotenuse
    cos_roll = math.cos(roll)    # Eq 13: cos = adjacent / hypotenuse
    
        # de-rotate by roll angle Phi
    By = ((My * cos_roll - Mz * sin_roll))    # Eq 19 y component
    Mz = ((My * sin_roll + Mz * cos_roll))    # Bpy*sin(Phi)+Bpz*cos(Phi)
    Az = ((My * sin_roll + Mz * cos_roll))    # Eq 15 denominator
    
        # calculate current pitch angle Theta
    pitch = math.atan2(-Ax, Az)    # Eq 15
    pitch_d = 180*pitch/math.pi
    #print pitch_d
    
        # restrict pitch angle to range -90 to 90 degrees
    if (pitch > math.pi/2) :
        pitch = (math.pi - pitch_d)
    if (pitch < -math.pi/2) :
        pitch = (-math.pi - pitch_d)
        
        # calculate sin and cosine of pitch angle Theta
    sin_pitch = math.sin(pitch)    # Eq 15: sin = opposite / hypotenuse
    cos_pitch = math.cos(pitch)    # Eq 15: cos = adjacent / hypotenuse
    
        # correct cosine if pitch not in range -90 to 90 degrees
    if (cos_pitch < 0) :
        cos_pitch = -cos_pitch
    
        # de-rotate by pitch angle Theta
    Bx = (Mx * cos_pitch + Mz * sin_pitch)    # Eq 19: x component
    Bz = (-Mx * sin_pitch + Mz * cos_pitch)    # Eq 19: z component
    
    nBx = Bx/math.sqrt(Bx**2+By**2)
    nBy = By/math.sqrt(Bx**2+By**2)
        # calculate current yaw = e-compass angle Psi
    yaw = math.atan2(-nBy, nBx)  # Eq 22
    yaw_d = 180*yaw/math.pi
    print "{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.1f}".format(-nBy, nBx, -By, Bx, yaw_d)

#print yaw_d
    
    return yaw_d

try:
    while (True):
        heading()
        time.sleep(0.1)

except KeyboardInterrupt:
    print "Bye!"
