import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

LIGHT = 22 
TRIG = 23
ECHO = 24
 
print "Distance Measurement In Progress"

GPIO.setup(LIGHT,GPIO.OUT) 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

LED = GPIO.PWM(22, 100)
LED.start(0)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

print "Done waiting."

try :
  pulse_start = time.time()
  pulse_end = time.time()
  
  while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
      
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()
      
    pulse_duration = pulse_end - pulse_start
  
    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    if distance < 100 :
      LED.ChangeDutyCycle(100)
    else :
      LED.ChangeDutyCycle(0)
    
    print "Distance:",distance,"cm"
    
    time.sleep(0.05)

except KeyboardInterrupt :
  GPIO.cleanup()
