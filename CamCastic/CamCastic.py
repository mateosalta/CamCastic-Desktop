#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')

#For threading support
from gi.repository import GObject

GObject.threads_init()

#For the as of this moment not working video...
from gi.repository import Gst, Gtk
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

#for keypresses
from gi.repository import Gdk

Gst.init(None)

from gi.repository import Gtk

class StatusIcon(Gtk.StatusIcon):
    def __init__(self, rootwin):
        Gtk.StatusIcon.__init__(self)
        self.rootwin = rootwin
        self.set_from_stock(Gtk.STOCK_HOME) 
        self.connect("popup-menu", self.right_click_event)

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()
 
        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)

        settings = Gtk.MenuItem()
        settings.set_label("Settings")
        settings.connect("activate", self.rootwin.properties_wrap)

        quit = Gtk.MenuItem()
        quit.set_label("Quit") 
        quit.connect("activate", self.rootwin.quit)
 
        self.menu.append(settings)
        self.menu.append(about)
        self.menu.append(quit)
 
        self.menu.show_all()
 
        def pos(menu, icon):
                return (Gtk.StatusIcon.position_menu(menu, icon))
 
        self.menu.popup(None, None, pos, self, button, time)

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("CamCastic-Desktop")
        about_dialog.set_version("0.1")
        about_dialog.set_authors(["Andrew King","Mateo Salta"])

        about_dialog.run()
        about_dialog.destroy()

class Player(object):
    def __init__(self):
        self.win = Gtk.Window()
        self.status_icon = StatusIcon(self)
        self.resolution = {
            'width' : Gdk.get_default_root_window().get_width(),
            'height' : Gdk.get_default_root_window().get_height()
            }
        self.height = int(self.resolution['height']/3)
        self.width = int(self.height/3*4)
        self.win.connect('destroy', self.quit)
        self.win.set_default_size(self.width, self.height)
        self.win.set_decorated(False)
        self.win.set_keep_above(True)
        self.win.set_property('skip-taskbar-hint', True)
        self.win.set_double_buffered(False)

        self.pipeline = Gst.parse_launch ("v4l2src ! videoconvert ! xvimagesink")

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        self.win.connect("key-press-event", self.on_keypress)
        self.on_keypress_dict = {
            Gdk.KEY_Escape : Gtk.main_quit,
            Gdk.KEY_F1 : self.pipeline.set_state,
            Gdk.KEY_F2 : self.pipeline.set_state,
        }
        self.state_args = {
            Gdk.KEY_Escape : Gtk.main_quit,
            Gdk.KEY_F1 : Gst.State.PLAYING,
            Gdk.KEY_F2 : Gst.State.NULL
        }
        self.win.move(self.resolution['width'] - self.width, self.resolution['height'] - self.height)

    def on_keypress(self, widget, event):
        '''
        A case switch statement to eliminate the
        five checks kludginess
        '''
        print('In keypress')
        if event.keyval == Gdk.KEY_F5: self.properties(widget, event)
        else: 
            try:
                self.on_keypress_dict[event.keyval](self.state_args[event.keyval])
            except KeyError:
                pass

    def properties_wrap(self, arg):
        self.properties(None, None)

    def properties(self, widget, event):
        try:
            self.prop_win.show()
        except:
            self.prop_win = Gtk.Window(Gtk.WindowType.TOPLEVEL)
            self.prop_win.set_position(Gtk.WindowPosition.CENTER)
            self.prop_win.set_decorated(False)
            self.prop_win.set_title("Properties")
            self.prop_win.set_size_request(320, 120)
            self.prop_win.set_resizable(False)
            self.prop_win.set_keep_above(True)
            self.prop_win.set_property('skip-taskbar-hint', True)
            self.prop_win.connect("destroy", self.closeproperties)
            vbox = Gtk.VBox(spacing=4)

            hbox = Gtk.HBox(spacing=4)
            check = Gtk.CheckButton("Pin")
            check.set_active(True)
            check.set_size_request(100, 35)
            check.connect("clicked", self.pinning)
            hbox.pack_start(check, True, True, 10)
            scale = Gtk.HScale()
            scale.set_range(0, 100)
            scale.set_value(100)
            scale.set_size_request(320, 35)
            scale.connect("value-changed", self.opac_slider)
            hbox.pack_start(scale, True, True, 10)
            self.entry = Gtk.Entry()
            self.entry2 = Gtk.Entry()

            self.entry.set_text(str(self.width))
            self.entry2.set_text(str(self.height))


            hbox2 = Gtk.HBox(spacing=4)
            hbox2.pack_start(self.entry, True, True, 10)
            hbox2.pack_start(self.entry2, True, True, 10)
            hbox3 = Gtk.HBox(spacing=4)
            ok = Gtk.Button("OK")
            ok.connect("clicked", self.change_size)
            hbox3.pack_start(ok, True, True, 10)
            exit = Gtk.Button("Exit")
            exit.connect("clicked", self.closeproperties)
            hbox3.pack_start(exit, True, True, 10)
            vbox.pack_start(hbox, True, True, 10)
            vbox.pack_start(hbox2, True, True, 10)
            vbox.pack_start(hbox3, True, True, 10)
            self.prop_win.add(vbox)
            self.prop_win.show_all()

    def pinning(self, checkbox):
        if checkbox.get_active():
            self.set_keep_above(True)
        else:
            self.set_keep_above(False)

    def opac_slider(self, w):
        self.win.set_opacity(w.get_value()/100.0)
        self.pipeline.set_state(Gst.State.PLAYING)
                
    def change_size(self, w):
        print('in change size')
        self.width = int(self.entry.get_text())
        self.height = int(self.entry2.get_text())
        self.win.resize(self.width,self.height)
        self.win.move(self.resolution['width'] - self.width, self.resolution['height'] - self.height)
        self.win.show_all()

    def closeproperties(self, w):
        self.prop_win.hide()

    def run(self):
        self.win.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.win.get_property('window').get_xid()

        print('in get_xid')
        self.pipeline.set_state(Gst.State.READY)
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_window_handle(self.xid)
            print('prepped')

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,        
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


p = Player()
p.run()


