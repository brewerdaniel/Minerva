'''
Pictures demo
=============

This is a basic picture viewer, using the scatter widget.
'''

import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock


import socket,os,time, select

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("djb231.quns.cam.ac.uk", 12345))
size = 65536
client_socket.setblocking(0)
client_socket.settimeout(0.3)

class PicturesApp(App):

    alreadyUpdating=False
    index=0

    def transfer(self) :
	filename="/tmp/cam.jpg.tmp"
        fp = open(filename,'w')
        strt = time.time()
        client_socket.send("cam")
        while True :
            try :
                ready = select.select([client_socket], [], [], 0.2)
                if ready[0]:
                    strng = client_socket.recv(size)
                    if not strng[-3:]=='end' :
                        fp.write(strng)
                    else :
                        fp.write(strng[:-3])
                        break
                else :
                    print "Socket busy."
            except Exception, e :
                print "Transfer failed."
        fp.close()
        newFilename="/tmp/cam.jpg"
        os.rename(filename,newFilename)
	return newFilename

    def build(self):
        print "build()"
        # the root is created in pictures.kv
        root = self.root

        try :
            print self.transfer()
	    self.wimg = Image(source=self.transfer())
            root.add_widget(self.wimg)
            Clock.schedule_once(self.update)

        except Exception, e:
	    print 'Shit'


    def update(self, img) :
        if self.index%10==0 :
            print "\n"
            self.index=0
        self.index+=1
        try :
            if not self.alreadyUpdating :
                self.alreadyUpdating=True
                self.transfer()
                self.wimg.reload()
                self.alreadyUpdating=False

        except Exception, e :
            print "I wonder what causes this..."
            print e
 
        Clock.schedule_once(self.update)



if __name__ == '__main__':
    PicturesApp().run()
    client_socket.send("end")
    client_socket.shutdown(1)
