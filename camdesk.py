#!/usr/bin/env python

import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk, Gdk
GObject.threads_init()
Gst.init(None)


class CamDesk(Gtk.Window):
	
    def closeme(self, widget, event) :
        if event.keyval == Gdk.KEY_Escape :
            Gtk.main_quit()

    def startme(self, widget, event) :
        if event.keyval == Gdk.KEY_F1 :
            self.player.set_state(Gst.State.PLAYING)

    def stopme(self, widget, event) :
        if event.keyval == Gdk.KEY_F2 :
            self.player.set_state(Gst.State.NULL)

    def properties(self, widget, event) :
        if event.keyval == Gdk.KEY_F5 :
            #blah
            self.win = Gtk.Window(Gtk.Window.TOPLEVEL)
            self.win.set_title("Properties")
            self.win.set_size_request(320, 120)
            self.win.set_resizable(False)
            self.win.set_keep_above(True)
            self.win.set_property('skip-taskbar-hint', True)
            self.win.connect("destroy", self.closeproperties)
            vbox = Gtk.VBox(spacing=4)
            hbox = Gtk.HBox(spacing=4)
            hbox2 = Gtk.HBox(spacing=4)
            
            check = Gtk.CheckButton("Pin")
            check.set_active(True)
            check.set_size_request(100, 35)
            check.connect("clicked", self.pinning)
            hbox.pack_start(check)
            
            scale = Gtk.HScale()
            scale.set_range(0, 100)
            scale.set_value(100)
            scale.set_size_request(320, 35)
            scale.connect("value-changed", self.opac_slider)
            
            hbox.pack_start(scale)
            
            self.entry = Gtk.Entry()
            self.entry2 = Gtk.Entry()
            self.entry.set_text("width")
            self.entry2.set_text("height")
            hbox2.pack_start(self.entry)
            hbox2.pack_start(self.entry2)
            
            hbox3 = Gtk.HBox(spacing=4)
            ok = Gtk.Button("OK")
            ok.connect("clicked", self.change_size)
            hbox3.pack_start(ok)
            exit = Gtk.Button("Exit")
            exit.connect("clicked", self.closeproperties)
            hbox3.pack_start(exit)
            
            vbox.pack_start(hbox)
            vbox.pack_start(hbox2)
            vbox.pack_start(hbox3)
            
            self.win.add(vbox)
            self.win.show_all()
           
    def pinning(self, checkbox):
        if checkbox.get_active():
            self.set_keep_above(True)
        else:
            self.set_keep_above(False)

    def opac_slider(self, w):
        self.set_opacity(w.get_value()/100.0)
		
    def change_size(self, w):
        width = int(self.entry.get_text())
        height = int(self.entry2.get_text())
        self.set_size_request(width,height)
	 	
    def closeproperties(self, w):
        self.win.hide()
		
    def __init__(self):
        super(CamDesk, self).__init__()
        
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("CamDesk")
        self.set_decorated(False)
        #self.set_has_frame(False)
        self.set_size_request(320, 240)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_property('skip-taskbar-hint', True)
        #Gtk.Window_set_default_icon_from_file('logo.png')
        self.connect("destroy", Gtk.main_quit, "WM destroy")
        self.connect("key-press-event", self.closeme)
        self.connect("key-press-event", self.startme)
        self.connect("key-press-event", self.stopme)
        self.connect("key-press-event", self.properties)
        
        vbox = Gtk.VBox(False, 0)
        self.add(vbox)
        
        self.movie_window = Gtk.DrawingArea()
        vbox.add(self.movie_window)
        self.show_all()
        
        # Set up the Gstreamer pipeline
        self.player = Gst.parse_launch ("v4l2src ! autovideosink")
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.Message.EOS:
            self.player.set_state(Gst.State_NULL)
            self.startcam.set_label("Start")
        elif t == Gst.Message.ERROR:
            err, debug = message.parse_error()
        print("Error: %s" % err, debug)
        self.player.set_state(Gst.State_NULL)
        self.startcam.set_label("Start")
		
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
            message_name = message.structure.get_name()
        if message_name == "prepare-window-handle":
    # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.window.xid)

CamDesk()
#Gtk.gdk.threads_init()
Gtk.main()
