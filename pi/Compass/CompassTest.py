from CompassController import *

if __name__ == "__main__":

    compasscontrol = CompassController(20)
    try:
        print("Starting compass controller")
        compasscontrol.start()
        while (True):
            print compasscontrol.heading.degrees
            print compasscontrol.heading.radians
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print "Interrupt received"
   
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print "Stopping compass controller"
        compasscontrol.stopController()
        compasscontrol.join()
        print "Done"
