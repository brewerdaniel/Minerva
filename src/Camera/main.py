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


    def update(self) :
        #while True :
        for i in range(10) :
            print 'hey'
            #sleep(0.5)
            self.transfer()
            #wimg.reload()



    def build(self):

        # the root is created in pictures.kv
        root = self.root

        try :
	    wimg = Image(source=self.transfer())
	    root.add_widget(wimg)
	    btn1 = Button(text='Update')
	    btn1.bind(on_press=update)
	    root.add_widget(btn1)	

        except Exception, e:
	    print 'Shit'

if __name__ == '__main__':
    PicturesApp().run()
    client_socket.shutdown(1)
