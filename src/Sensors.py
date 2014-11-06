# The sensors class for Minerva
#
# This class should interface all sorts of things
import socket, struct, time, math, sys, os, XLoBorg, re, RPi.GPIO
from thread import *
from subprocess import call

class MinervaSensors(object) :
    def __init__(self) :
        # Initialise the XLoBorg library
        XLoBorg.printFunction = XLoBorg.NoPrint
        XLoBorg.Init()

        # Initialise the GPIO interface
        GPIO.setmode(GPIO.BCM)
        TRIG = 23 
        ECHO = 24
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)


    def accel(self) :
        accel = XLoBorg.ReadAccelerometer()
        time.sleep(0.0125)
        accel =[x + y for x, y in zip(accel, XLoBorg.ReadAccelerometer())]
        time.sleep(0.0125)
        accel =[x + y for x, y in zip(accel, XLoBorg.ReadAccelerometer())]
        accel =[x/3 for x in accel]
        return accel

    def mag(self) :
        M = XLoBorg.ReadCompassRaw()
        time.sleep(0.0125)
        M =[x + y for x, y in zip(M, XLoBorg.ReadCompassRaw())]
        time.sleep(0.0125)
        M =[x + y for x, y in zip(M, XLoBorg.ReadCompassRaw())]
        M =[x/3 for x in M]
        return M

    def heading(self) :
        M = self.mag()
        A = self.accel()
        
        g = 9.81
        
        # hard iron estimate
        Vx, Vy, Vz = (0.0, 0.0, 0.0);
        
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
        roll = atan2(Ay, Az)    # Eq 13
        roll_d = 180*roll/pi
        print roll_d
    
        # calculate sin and cosine of roll angle Phi
        sin_roll = sin(roll)    # Eq 13: sin = opposite / hypotenuse
        cos_roll = cos(roll)    # Eq 13: cos = adjacent / hypotenuse
        
        # de-rotate by roll angle Phi
        By = ((My * cos_roll - Mz * sin_roll))    # Eq 19 y component
        Mz = ((My * sin_roll + Mz * cos_roll))    # Bpy*sin(Phi)+Bpz*cos(Phi)
        Az = ((My * sin_roll + Mz * cos_roll))    # Eq 15 denominator
        
        # calculate current pitch angle Theta
        pitch = atan2(-Ax, Az)    # Eq 15
        pitch_d = 180*pitch/pi
        print pitch_d
    
        # restrict pitch angle to range -90 to 90 degrees
        if (pitch_d > 90) :
            pitch_d = (180 - pitch_d)
        if (pitch_d < -90) :
            pitch_d = (-180 - pitch_d)
                
        # calculate sin and cosine of pitch angle Theta
        sin_pitch = sin(pitch)    # Eq 15: sin = opposite / hypotenuse
        cos_pitch = cos(pitch)    # Eq 15: cos = adjacent / hypotenuse
        
        # correct cosine if pitch not in range -90 to 90 degrees
        if (cos_pitch < 0) :
            cos_pitch = -cos_pitch
    
        # de-rotate by pitch angle Theta
        Bx = (Mx * cos_pitch + Mz * sin_pitch)    # Eq 19: x component
        Bz = (-Mx * sin_pitch + Mz * cos_pitch)    # Eq 19: z component
        
        # calculate current yaw = e-compass angle Psi
        yaw = atan2(-By, Bx)  # Eq 22
        yaw_d = 180*yaw/pi
        print yaw_d
        
        return yaw_d

    def ambi_temp(self) :
        temp = XLoBorg.ReadTemperature()
        time.sleep(0.0125)
        temp+=XLoBorg.ReadTemperature()
        time.sleep(0.0125)
        temp+=XLoBorg.ReadTemperature()
        temp/=3.0
        return temp

    def cpu_temp(self) :
        PUProcess = Popen(["cat","/sys/class/thermal/thermal_zone0/temp"],stdout=subprocess.PIPE)
        GPUProcess = Popen(["/opt/vc/bin/vcgencmd","measure_temp"],stdout=subprocess.PIPE)
        CPU, err = CPUProcess.communicate()
        GPU, err = GPUProcess.communicate()
        CPU = float(CPU)
        CPU /= 1000
        GPU = float(re.findall("\d+.\d+", GPU)[0])
        data=[CPU,GPU]
        return data

    def proximity(self) :
        GPIO.output(TRIG, False)
        time.sleep(0.1)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
            
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171500
        distance = round(distance, 2)

        return distance

    def __enter__(self) :
        return self

    def __exit__(self, type, value, traceback) :
        GPIO.cleanup()
