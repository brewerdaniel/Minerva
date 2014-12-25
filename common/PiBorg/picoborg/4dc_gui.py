#!/usr/bin/env python
# coding: latin-1

# Import libary functions we need (we are using wiringpi so we can use the PWM)
import wiringpi
import Tkinter
import tkMessageBox

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

# Define some constants to make code clearer
GPIO_INPUT = 0
GPIO_OUTPUT = 1
GPIO_PWM = 2

# Internal state for managing a PWM line
global pwmOn
global pwmLevel
pwmOn = False
pwmLevel = 1023

# Class respresenting the GUI dialog
class PicoBorg_tk(Tkinter.Tk):
    # Constructor (called when the object is first created)
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.OnExit) # Call the OnExit function when user closes the dialog
        self.Initialise()

    # Initialise the dialog
    def Initialise(self):
        self.title('PicoBorg Example GUI')
        # Setup a grid of 4 buttons which command each drive, plus a PWM slider for drive 2
        self.grid()
        self.but1 = Tkinter.Button(self, text = '1', command = self.but1_click)
        self.but1['fg'] = '#FFFFFF'
        self.but1['font'] = ("Arial", 60, "bold")
        self.but1.grid(column = 0, row = 0, rowspan = 2, sticky = 'NSEW')
        self.but2 = Tkinter.Button(self, text = '2', command = self.but2_click)
        self.but2['fg'] = '#FFFFFF'
        self.but2['font'] = ("Arial", 60, "bold")
        self.but2.grid(column = 1, row = 0, rowspan = 1, sticky = 'NSEW')
        self.sld2 = Tkinter.Scale(self, from_ = 0, to = 1023, orient = Tkinter.HORIZONTAL, command = self.sld2_move)
        self.sld2.set(pwmLevel)
        self.sld2.grid(column = 1, row = 1, rowspan = 1, sticky = 'NSEW')
        self.but3 = Tkinter.Button(self, text = '3', command = self.but3_click)
        self.but3['fg'] = '#FFFFFF'
        self.but3['font'] = ("Arial", 60, "bold")
        self.but3.grid(column = 2, row = 0, rowspan = 2, sticky = 'NSEW')
        self.but4 = Tkinter.Button(self, text = '4', command = self.but4_click)
        self.but4['fg'] = '#FFFFFF'
        self.but4['font'] = ("Arial", 60, "bold")
        self.but4.grid(column = 3, row = 0, rowspan = 2, sticky = 'NSEW')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(0, weight = 4)
        self.grid_rowconfigure(1, weight = 1)
        # Set the size of the dialog
        self.resizable(True, True)
        self.geometry('800x200')
        # Setup the GPIO pins
        self.SetupGpio()
        # Set the button colours based on drive level
        self.SetColourDrive(self.but1, DRIVE_1)
        self.SetColourDrive(self.but2, DRIVE_2)
        self.SetColourDrive(self.but3, DRIVE_3)
        self.SetColourDrive(self.but4, DRIVE_4)

    # Setup the GPIO drives as outputs and turn them all off
    def SetupGpio(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(DRIVE_1, GPIO_OUTPUT)
        wiringpi.pinMode(DRIVE_2, GPIO_PWM)
        wiringpi.pinMode(DRIVE_3, GPIO_OUTPUT)
        wiringpi.pinMode(DRIVE_4, GPIO_OUTPUT)
        self.MotorOff()
        tkMessageBox.showinfo("PicoBorg", "You can now turn on the power")

    # Called when the user closes the dialog
    def OnExit(self):
        # Turn drives off, release GPIO and end the program
        self.MotorOff()
        tkMessageBox.showinfo("PicoBorg", "Turn the power off now")
        self.quit()

    # Turn all the drives off
    def MotorOff(self):        
        wiringpi.digitalWrite(DRIVE_1, 0)
        pwmOn = False
        wiringpi.pwmWrite(DRIVE_2, 0)
        wiringpi.digitalWrite(DRIVE_3, 0)
        wiringpi.digitalWrite(DRIVE_4, 0)

    # Set a button to be coloured based on a GPIO state
    def SetColourDrive(self, button, drive):
        global pwmOn
        if drive == DRIVE_2:
            # PWM drive, see if it is flagged as on
            if pwmOn:
                button['bg'] = '#008000'
            else:
                button['bg'] = '#400000'
        else:
            # Digital drive, read current status
            if wiringpi.digitalRead(drive) == 0:
                button['bg'] = '#400000'
            else:
                button['bg'] = '#008000'
        button['activebackground'] = button['bg']

    # Toggle a drive pin on/off
    def ToggleDrive(self, button, drive):
        global pwmOn
        global pwmLevel
        if drive == DRIVE_2:
            # PWM drive, see if it is flagged as on and toggle between level and 0
            if pwmOn:
                pwmOn = False
                wiringpi.pwmWrite(drive, 0)
            else:
                pwmOn = True
                wiringpi.pwmWrite(drive, pwmLevel)
        else:
            # Digital drive, toggle based on current status
            if wiringpi.digitalRead(drive) == 0:
                wiringpi.digitalWrite(drive, 1)
            else:
                wiringpi.digitalWrite(drive, 0)
        self.SetColourDrive(button, drive)
        
    # Called when but1 is clicked
    def but1_click(self):
        self.ToggleDrive(self.but1, DRIVE_1)

    # Called when but2 is clicked
    def but2_click(self):
        self.ToggleDrive(self.but2, DRIVE_2)
    
    # Called when sld2 is moved
    def sld2_move(self, value):
        global pwmOn
        global pwmLevel
        pwmLevel = int(value)
        if pwmOn:
            wiringpi.pwmWrite(DRIVE_2, pwmLevel)

    # Called when but3 is clicked
    def but3_click(self):
        self.ToggleDrive(self.but3, DRIVE_3)

    # Called when but4 is clicked
    def but4_click(self):
        self.ToggleDrive(self.but4, DRIVE_4)

# if we are the main program (python was passed a script) load the dialog automatically
if __name__ == "__main__":
    app = PicoBorg_tk(None)
    app.mainloop()

