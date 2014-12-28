import time
import timeit
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

        self.max_offsets = [-431, 819, 2000]
        self.min_offsets = [-850, 432, 1000]
        self.offset_calculations = 1
        self.offset_sums = [-618, 733.00, 1437.00]
        self.offsets = [-618, 733.00, 1437.00]
        self.timeInterval = 1.0/float(frequency)
        self.K = 0.98

         #update the heading
        data = XLoBorg.ReadCompassRaw()
        
        x_out = data[0] - self.offsets[0]
        y_out = data[1] - self.offsets[1]
        z_out = data[2] - self.offsets[2]
        
        normal_x = x_out/math.sqrt(x_out**2 + y_out**2)
        normal_y = y_out/math.sqrt(x_out**2 + y_out**2)
        
        self.bearing  = math.atan2(normal_y, normal_x) 
        if (self.bearing < 0):
            self.bearing += 2 * math.pi

        self.lastBearing = self.bearing

        self.heading = Heading(self.lastBearing)

        self.updateSuccess = True
       
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

        self.offsets[0] = x_sum/300.0
        self.offsets[1] = y_sum/300.0
        self.running = True

    def getReading(self):
        Mx, My, Mz = XLoBorg.ReadCompassRaw()
        
        recalculate_offsets = False
        
        if (Mx > self.max_offsets[0]):
            self.max_offsets[0] = Mx
            recalculate_offsets = True
        if (My > self.max_offsets[1]):
            self.max_offsets[1] = My
            recalculate_offsets = True
        if (Mz > self.max_offsets[2]):
            self.max_offsets[2] = Mz
            recalculate_offsets = True
            
        if (Mx < self.min_offsets[0]):
            self.min_offsets[0] = Mx
            recalculate_offsets = True
        if (My < self.min_offsets[1]):
            self.min_offsets[1] = My
            recalculate_offsets = True
        if (Mz < self.min_offsets[2]):
            self.min_offsets[2] = Mz
            recalculate_offsets = True
  
        if (recalculate_offsets):
            self.offset_calculations += 1
            self.offsets[0] = (self.offset_sums[0] + (self.max_offsets[0] + self.min_offsets[0])/2)/self.offset_calculations
            self.offset_sums[0] += (self.max_offsets[0] + self.min_offsets[0])/2
            self.offsets[1] = (self.offset_sums[1] + (self.max_offsets[1] + self.min_offsets[1])/2)/self.offset_calculations
            self.offset_sums[1] += (self.max_offsets[1] + self.min_offsets[1])/2
            self.offsets[2] = (self.offset_sums[2] + (self.max_offsets[2] + self.min_offsets[2])/2)/self.offset_calculations
            self.offset_sums[2] += (self.max_offsets[2] + self.min_offsets[2])/2
            recalculate_offsets = False
            
        Mx -= self.offsets[0]
        My -= self.offsets[1]
        Mz -= self.offsets[2]
        
        return [Mx, My, Mz]

    def updateHeading(self):
        x_out, y_out, z_out = self.getReading()
        
        normal_x = x_out/math.sqrt(x_out**2 + y_out**2)
        normal_y = y_out/math.sqrt(x_out**2 + y_out**2)
        
        self.bearing  = math.atan2(normal_y, normal_x) 
        if (self.bearing < 0):
            self.bearing += 2 * math.pi

        self.lastBearing = self.K*self.lastBearing + (1-self.K)*self.bearing

        self.heading = Heading(self.lastBearing)

        self.updateSuccess = True

