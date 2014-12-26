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

class PicturesApp(App):

    def build(self):
        print "build()"
        # the root is created in pictures.kv
        root = self.root

        try :
	    self.wimg = AsyncImage(source='http://djb231.quns.cam.ac.uk/media/cam.jpg')
            root.add_widget(self.wimg)
     #       Clock.schedule_once(self.update)

        except Exception, e:
	    print 'Shit'


    #def update(self, img) :
        #self.wimg.reload()
        #Clock.schedule_once(self.update)



if __name__ == '__main__':
    PicturesApp().run()
