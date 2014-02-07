#!/usr/bin/env python3.3

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject
GObject.threads_init()

from gi.repository import Gst, Gtk

Gst.init(None)

#Config data
from camcasticconfig import CamcasticBaseConfig,\
                            CamcasticShortcuts,\
                            CamcasticCameraConfig,\
                            CamcasticCameras

#Usermode Keylog
from usermodekeylog import HookManager,\
                            pyxhookkeyevent,\
                            pyxhookmouseevent

#User interface
from ui import CamcasticIndicator,\
                CamcasticAboutWin,\
                CamcasticCameraWin,\
                CamcasticCameraConfigBox,\
                CamcasticHotkeysBox,\
                CamcasticConfigWin

class MyApp(Gtk.Application):
  def __init__(self, app_name):
    super().__init__()
    self.name = app_name
    self.conf_win = CamcasticConfigWin(self)
    self.about_win = CamcasticAboutWin(self)
    self.indicator = CamcasticIndicator(self)
    self.config = CamcasticBaseConfig(self)
    self.shortcuts = CamcasticShortcuts(self)
    self.hm = HookManager(self)
    
    #This could be cleaner...  I'll fix it eventually.
    self.hm.KeyDown = self.hm.printevent
    self.hm.KeyUp = self.hm.printevent

  def cb_keypress(self, keypress):
    print(keypress)

  def run(self):
    self.hm.start()
    Gtk.main()
    self.hm.cancel()

if __name__ == '__main__':
  MyApp('CamCastic-Desktop').run()