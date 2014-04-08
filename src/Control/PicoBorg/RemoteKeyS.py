#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import SocketServer
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Initialise the socket
#s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = ''
#port = 12345
portListen = 9038

# Set which GPIO pins the drive outputs are connected to
FORWARD = 17
BACKWARD = 18
LEFT = 8
RIGHT = 7

# Set all of the drive pins as output pins
GPIO.setup(FORWARD, GPIO.OUT)
GPIO.setup(BACKWARD, GPIO.OUT)
GPIO.setup(LEFT, GPIO.OUT)
GPIO.setup(RIGHT, GPIO.OUT)

# Map of drives to pins
lDrives = [FORWARD, BACKWARD, LEFT, RIGHT]

# Function to set all drives off
def MotorsOff():
    GPIO.output(FORWARD, GPIO.LOW)
    GPIO.output(BACKWARD, GPIO.LOW)
    GPIO.output(LEFT, GPIO.LOW)
    GPIO.output(RIGHT, GPIO.LOW)

# Class used to handle UDP messages
class InstructionHandler(SocketServer.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request          # Read who spoke to us and what they said
        request = request.upper()               # Convert command to upper case
	print request
        driveCommands = request.split(',')      # Separate the command into individual drives
	print driveCommands
        if len(driveCommands) == 1:
            # Special commands
            if request == 'ALLOFF':
                # Turn all drives off
                MotorOff()
                print 'All drives off'
            elif request == 'EXIT':
                # Exit the program
                isRunning = False
            else:
                # Unknown command
                print 'Special command "%s" not recognised' % (request)
        elif len(driveCommands) == len(lDrives):
            # For each drive we check the command
            for driveNo in range(len(driveCommands)):
                command = driveCommands[driveNo]
                if command == 'ON':
                    # Set drive on
                    GPIO.output(lDrives[driveNo], GPIO.HIGH)
                elif command == 'OFF':
                    # Set drive off
                    GPIO.output(lDrives[driveNo], GPIO.LOW)
                elif command == 'X':
                    # No command for this drive
                    pass
                else:
                    # Unknown command
                    print 'Drive %d command "%s" not recognised!' % (driveNo, command)
        else:
            # Did not get the right number of drive commands
            print 'Command "%s" did not have %d parts!' % (request, len(lDrives))

try:
    global isRunning

    # Start by turning all drives off
    MotorsOff()
    raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    remoteKeyServer = SocketServer.TCPServer(('10.0.1.8', portListen), InstructionHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:
        remoteKeyServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print 'Finished'
    MotorsOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print 'Terminated'
    MotorsOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
