import time
import threading
import math
import XLoBorg

# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

#class for holding temperature values
class Heading():
    def __init__(self, radians):
        self.radians = radians
    @property
    def degrees(self):
        return math.degrees(self.radians)
    @property
    def radians(self):
        return self.radians

class CompassController(threading.Thread):
    def __init__(self, frequency):
        threading.Thread.__init__(self)

        self.x_offset = -618.954
        self.y_offset = 733.05
        self.timeInterval = 1.0/float(frequency)

         #update the heading
        self.updateHeading()
       
        #set to not running
        self.running = False
       
    def run(self):
        #loop until its set to stopped
        self.running = True
        while(self.running):
            #update temperature
            self.updateHeading()
            #sleep
            time.sleep(self.timeInterval)
        self.running = False
       
    def stopController(self):
        self.running = False

    def calibrateCompass(self):
        self.running = False
        x_sum=0
        y_sum=0
        for i in range(0,300):
            data = XLoBorg.ReadCompassRaw()
            x_sum += data[0]
            y_sum += data[1]
            time.sleep(0.1)

        self.x_offset = x_sum/300.0
        self.y_offset = y_sum/300.0
        self.running = True

    def updateHeading(self):
        data = XLoBorg.ReadCompassRaw()

        x_out = data[0] - self.x_offset
        y_out = data[1] - self.y_offset
        z_out = data[2]
        
        normal_x = x_out/math.sqrt(x_out**2 + y_out**2)
        normal_y = y_out/math.sqrt(x_out**2 + y_out**2)
        
        self.bearing  = math.atan2(normal_y, normal_x) 
        if (self.bearing < 0):
            self.bearing += 2 * math.pi

        self.heading = Heading(self.bearing)

        self.updateSuccess = True

