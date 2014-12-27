#!/usr/bin/env python
 
import XLoBorg
from time import *

XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.tempOffest = 25
XLoBorg.Init()
if XLoBorg.foundAccelerometer and XLoBorg.foundCompass:
    mx_tot=0
    my_tot=0
    mz_tot=0
    count=1
    try:
        while(True):
            mx, my, mz = XLoBorg.ReadCompassRaw()
            mx_tot += mx
            my_tot += my
            mz_tot += mz
            count += 1
            print 'mX = %+06d, mY = %+06d, mZ = %+06d' % (mx, my, mz)
            sleep(0.1)

    except KeyboardInterrupt:
        print "{0:.2f} {1:.2f} {2:.2f}".format(mx_tot/count, my_tot/count, mz_tot/count)
        print "Done"
else:
    print 'Did not find both chips, run ~/xloborg/XLoBorg.py for more details'
