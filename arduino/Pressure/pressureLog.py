#!/usr/bin/python
import Adafruit_BMP.BMP085 as BMP085
import logging, time

logging.basicConfig(filename='pressure.log',level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

try :
    while True :
        logging.info('\t{0:0.4f}'.format(sensor.read_temperature())+'\t{0:0.1f}'.format(sensor.read_pressure()))
        time.sleep(3)

except KeyboardInterrupt :
    print 'Bye bye!'
