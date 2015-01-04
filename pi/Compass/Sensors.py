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

K = 0.98

max_offsets = [-431, 819, 2000]
min_offsets = [-850, 432, 1000]

offset_calculations = 1

offset_sums = [-618, 700.00, 1427.00]

Vx, Vy, Vz = [-618, 700.00, 1427.00]

last_B = [0.0, 0.0]

def readSensor():

    global Vx
    global Vy
    global Vz
    global max_offsets
    global min_offsets
    global offset_calculations
    global offset_sums

    Mx, My, Mz = XLoBorg.ReadCompassRaw()
    
    recalculate_offsets = False
    
    if (Mx > max_offsets[0]):
        max_offsets[0] = Mx
        recalculate_offsets = True
    if (My > max_offsets[1]):
        max_offsets[1] = My
        recalculate_offsets = True
    if (Mz > max_offsets[2]):
        max_offsets[2] = Mz
        recalculate_offsets = True
  
    if (Mx < min_offsets[0]):
        min_offsets[0] = Mx
        recalculate_offsets = True
    if (My < min_offsets[1]):
        min_offsets[1] = My
        recalculate_offsets = True
    if (Mz < min_offsets[2]):
        min_offsets[2] = Mz
        recalculate_offsets = True
  
    if (recalculate_offsets):
        offset_calculations += 1
        Vx = (offset_sums[0] + (max_offsets[0] + min_offsets[0])/2)/offset_calculations
        offset_sums[0] += (max_offsets[0] + min_offsets[0])/2
        Vy = (offset_sums[1] + (max_offsets[1] + min_offsets[1])/2)/offset_calculations
        offset_sums[1] += (max_offsets[1] + min_offsets[1])/2
        Vz = (offset_sums[2] + (max_offsets[2] + min_offsets[2])/2)/offset_calculations
        offset_sums[2] += (max_offsets[2] + min_offsets[2])/2

    Mx -= Vx
    My -= Vy
    Mz -= Vz

    return [Mx, My, Mz]

def heading() :

    global last_B

    g = 9.81
    
    Ax, Ay, Az = XLoBorg.ReadAccelerometer()
    Ax *= g
    Ay *= g
    Az *= g
    
    roll = math.atan2(Ay, Az)
    roll_d = 180*roll/math.pi

    sin_roll = math.sin(roll)
    cos_roll = math.cos(roll)

    Mx, My, Mz = readSensor()

    By = ((My * cos_roll - Mz * sin_roll))    # Eq 19 y component
    Mz = ((My * sin_roll + Mz * cos_roll))    # Bpy*sin(Phi)+Bpz*cos(Phi)
    Az = ((Ay * sin_roll + Az * cos_roll))    # Eq 15 denominator
    
    pitch = math.atan2(-Ax, Az)
    pitch_d = 180*pitch/math.pi

   # print "{0:.4f} {1:.4f}".format(roll_d, pitch_d)

    if (pitch > math.pi/2) :
        pitch = (math.pi - pitch)
    if (pitch < -math.pi/2) :
        pitch = (-math.pi - pitch)
        
    sin_pitch = math.sin(pitch)
    cos_pitch = math.cos(pitch)
    
    if (cos_pitch < 0) :
        cos_pitch = -cos_pitch
    
    # de-rotate by pitch angle Theta
    Bx = (Mx * cos_pitch + My * sin_pitch * sin_roll + Mz * sin_pitch * cos_roll)    # Eq 19: x component
    Bz = (-Mx * sin_pitch + My * cos_pitch * sin_roll + Mz * cos_pitch * cos_roll)    # Eq 19: z component
    
    nBx = Bx/math.sqrt(Bx**2+By**2)
    nBy = By/math.sqrt(Bx**2+By**2)

    # calculate current yaw = e-compass angle Psi
    bearing = math.atan2(-nBy, nBx)  # Eq 22
    print bearing
    yaw_d = 180*bearing/math.pi
    print "{0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.1f}".format(-nBy, nBx, -By, Bx, yaw_d)

#print yaw_d
    
    return yaw_d

try:
    while (True):
        heading()
        time.sleep(0.1)

except KeyboardInterrupt:
    print "Bye!"
