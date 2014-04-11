#!/bin/bash/env python

import RPi.GPIO as GPIO
import XLoBorg
from time import sleep  # pull in the sleep function from time module


# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()


GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM

GPIO.setup(17, GPIO.OUT)# set GPIO 17 as output

led = GPIO.PWM(17, 60)    # create PWM on port 25 at 100 Hertz

led.start(0)              # start white led on 0 percent duty cycle (off)

# now the fun starts, we'll vary the duty cycle to 
# dim/brighten the leds, so one is bright while the other is dim

pause_time = 0.0375           # you can change this to slow down/speed up

try:
    while True:
        ratioMin = min(abs(XLoBorg.ReadAccelerometer()[1])*100,100)
        ratio = max(ratioMin,0.1)
        sleep(0.0125)
        ratioMin = min(abs(XLoBorg.ReadAccelerometer()[1])*100,100)
        ratio += max(ratioMin,0.1)
        sleep(0.0125)
        ratioMin = min(abs(XLoBorg.ReadAccelerometer()[1])*100,100)
        ratio += max(ratioMin,0.1)
	led.ChangeDutyCycle(ratio/3)
        sleep(0.0125)

except KeyboardInterrupt:
    led.stop()            # stop the PWM output
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
