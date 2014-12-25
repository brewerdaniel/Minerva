#!/bin/bash/env python

import RPi.GPIO as GPIO
import XLoBorg
from time import sleep  # pull in the sleep function from time module


# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()


GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM

GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)# set GPIO 17 as output

xAxis = GPIO.PWM(17, 60)    # create PWM on port 25 at 100 Hertz
yAxis = GPIO.PWM(22, 60)    # create PWM on port 25 at 100 Hertz


xAxis.start(0)              # start white led on 0 percent duty cycle (off)
yAxis.start(0)


# now the fun starts, we'll vary the duty cycle to 
# dim/brighten the leds, so one is bright while the other is dim

pause_time = 0.0125           # you can change this to slow down/speed up

try:
    while True:
        xRatio=0
        yRatio=0
        for x in range(10) :
            data = XLoBorg.ReadAccelerometer()
            xRatioMin = min(abs(data[0])*100,100)
            yRatioMin = min(abs(data[1])*100,100)
            xRatio += xRatioMin if xRatioMin>5 else 0.0
            yRatio += yRatioMin if yRatioMin>5 else 0.0
            sleep(pause_time)
	xAxis.ChangeDutyCycle(xRatio/10)
        yAxis.ChangeDutyCycle(yRatio/10)

except KeyboardInterrupt:
    xAxis.stop()            # stop the PWM output
    yAxis.stop()
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
