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


import socket,os,time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("djb231.quns.cam.ac.uk", 12345))
size = 65536


class PicturesApp(App):

    def transfer(self) :
	filename="/tmp/cam.jpg"
        client_socket.send("cam")
        fp = open(filename,'w')
        while True:
            strng = client_socket.recv(size)
            if not strng[-3:]=='end' :
                fp.write(strng)
            else :
                fp.write(strng[:-3])
                fp.close()
                break
	return filename

    def build(self):
        print "build()"
        # the root is created in pictures.kv
        root = self.root

        try :
	    self.wimg = Image(source=self.transfer())
            root.add_widget(self.wimg)
            
            #buttonStart = Button(text='Start', font_size=14)
            #buttonStop = Button(text='Stop', font_size=14)
            #buttonStart.bind(on_press=update)
            Clock.schedule_interval(self.update, 1.0 / 5.0)

        except Exception, e:
	    print 'Shit'


    def update(self, img) :
        try :
            self.transfer()
            self.wimg.reload()
        #self.root.add_widget(self.wimg)
        except Exception, e :
            print "I wonder what causes this..."

if __name__ == '__main__':
    PicturesApp().run()
    client_socket.shutdown(1)
