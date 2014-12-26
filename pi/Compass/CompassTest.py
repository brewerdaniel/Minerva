from CompassController import *

if __name__ == "__main__":

    #create temp sensor controller, put your controller Id here
    # look in "/sys/bus/w1/devices/" after running
    #  sudo modprobe w1-gpio
    #  sudo modprobe w1-therm
    compasscontrol = CompassController(10)

    try:
        print("Starting compass controller")
        #start up compass controller
        compasscontrol.start()
        #loop forever, wait for Ctrl C
        while (True):
            print compasscontrol.heading.degrees
            print compasscontrol.heading.radians
            time.sleep(1)
                       
    #Ctrl C
    except KeyboardInterrupt:
        print "Cancelled"
   
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #if it finishes or Ctrl C, shut it down
    finally:
        print "Stopping compass controller"
        #stop the controller
        compasscontrol.stopController()
        #wait for the tread to finish if it hasn't already
        compasscontrol.join()
       
    print "Done"
