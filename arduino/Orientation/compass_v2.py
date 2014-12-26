

# Initialise the XLoBorg library
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

scale=0.98

x_offset = -618.954
y_offset = 733.05

#Calibration - obtaining hard iron offsets
def calibrate():
    global x_offset
    global y_offset
    x_sum=0
    y_sum=0
    for i in range(0,300):
        data = XLoBorg.ReadCompassRaw()
        x_sum += data[0]
        y_sum += data[1]
        time.sleep(0.1)

    x_offset = x_sum/300.0
    y_offset = y_sum/300.0

#calibrate()
#print "Calibration complete. Sleeping for 10, then taking measurements"
#time.sleep(10)

for i in range(0,1000):
    data = XLoBorg.ReadCompassRaw()
    x_out = data[0] - x_offset
    y_out = data[1] - y_offset
    z_out = data[2]
    
    normal_x = x_out/_np.sqrt(x_out**2 + y_out**2)
    normal_y = y_out/_np.sqrt(x_out**2 + y_out**2)

    bearing  = math.atan2(normal_y, normal_x) 
    if (bearing < 0):
        bearing += 2 * math.pi
        
    print "{0:.8f} {1:.8f} {2:.8f} {3:.8f} {4:.1f}".format(normal_x, normal_y, (data[0]), (data[1]), math.degrees(bearing))
    time.sleep(0.01)
