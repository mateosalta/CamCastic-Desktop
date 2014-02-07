'''
All UI classes go here...

#TODO when code structure stabalizes, change root passing to only where necessary
or parent finding...
'''

from gi.repository import Gst, Gtk
from gi.repository import GdkX11, GstVideo

#for keypresses in the active window...maybe i'll use Gdk keymaps in other places
from gi.repository import Gdk

from gi.repository import AppIndicator3 as appindicator

class CamcasticIndicator:
  '''
  AppIndicator widget
  '''
  def __init__(self, root):
    self.app = root
    self.ind = appindicator.Indicator.new(
                self.app.name,
                "indicator-messages",
                appindicator.IndicatorCategory.APPLICATION_STATUS)
    self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    self.menu = Gtk.Menu()

    item = Gtk.MenuItem()
    item.set_label("About")
    item.connect("activate", self.app.about_win.cb_show, '')
    self.menu.append(item)

    item = Gtk.MenuItem()
    item.set_label("Configuration")
    item.connect("activate", self.app.conf_win.cb_show, '')
    self.menu.append(item)

    item = Gtk.MenuItem()
    item.set_label("Exit")
    item.connect("activate", self.cb_exit, '')
    self.menu.append(item)

    self.menu.show_all()
    self.ind.set_menu(self.menu)

  def cb_exit(self, w, data, other=''):
    '''
    Got in to the habit of wrapping these callbacks to discard things...
    '''
    Gtk.main_quit()

class CamcasticAboutWin(Gtk.AboutDialog):
  def __init__(self, root):
    super().__init__()
    self.set_name("CamCastic-Desktop")
    self.set_version("0.1")
    self.set_authors(["Andrew King","Mateo Salta"])
    self.connect("delete-event", self.cb_hide, '')
    for blob in self.get_children():
      for blob_a in blob.get_children():
        for blob_b in blob_a.get_children():
          try:
            if blob_b.get_label() == 'gtk-close': blob_b.connect('clicked', self.cb_hide, '')
          except:
            pass

  def cb_show(self, w, data, other=''):
    '''
    Show callback...  added so I can strip arguments
    '''
    self.show_all()

  def cb_hide(self, w, data, other=''):
    '''
    Hide callback... added so I can strip arguments
    '''
    self.hide()
    return True

class CamcasticCameraWin(Gtk.Window):
  def __init__(self, root):
    super().__init__()
    self.app = root
    #TODO this is a block paste from the original conversion...needs work
    self.set_title(self.app.name + 'Camera')
    self.resolution = {
        'width' : Gdk.get_default_root_window().get_width(),
        'height' : Gdk.get_default_root_window().get_height()
        }
    self.set_default_size(self.width, self.height)
    self.set_decorated(False)
    self.set_keep_above(True)
    self.set_property('skip-taskbar-hint', True)
    self.set_double_buffered(False)

    self.pipeline = Gst.parse_launch ("v4l2src ! videoconvert ! xvimagesink")

    self.bus = self.pipeline.get_bus()
    self.bus.add_signal_watch()
    self.bus.connect('message::eos', self.on_eos)
    self.bus.connect('message::error', self.on_error)

    self.bus.enable_sync_message_emission()
    self.bus.connect('sync-message::element', self.on_sync_message)

    self.connect("key-press-event", self.on_keypress)
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
    #self.move(self.resolution['width'] - self.width, self.resolution['height'] - self.height)

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

  def cb_show(self, w, data):
    self.show()

class CamcasticCameraConfigBox(Gtk.VBox):
  '''
  Class to display each camera config
  '''
  def __init__(self):
    vbox = Gtk.VBox(spacing=4)
    hbox = Gtk.HBox(spacing=4)
    scale = Gtk.HScale()
    scale.set_range(0, 100)
    scale.set_value(100)
    scale.set_size_request(320, 35)
    scale.connect("value-changed", self.opac_slider)
    hbox.pack_start(scale, True, True, 10)
    self.entry = Gtk.Entry()
    self.entry2 = Gtk.Entry()

    hbox2 = Gtk.HBox(spacing=4)
    hbox2.pack_start(self.entry, True, True, 10)
    hbox2.pack_start(self.entry2, True, True, 10)
    hbox3 = Gtk.HBox(spacing=4)
    ok = Gtk.Button("Resize")
    '''
    ok.connect("clicked", self.change_size)
    '''

class CamcasticHotkey(Gtk.HBox):
  def __init__(self, keycode='temp', cutname='test'):
    self.key = (keycode, cutname)
    self.pack_start(Gtk.Label(cutname))
    self.pack_start(Gtk.Label(self.__keycode_to_str(keycode)))
  def __keycode_to_str(self, keycode):
    return keycode

class CamcasticHotkeysBox(Gtk.VBox):
  def __init__(self, root):
    self.app = root
    Gtk.Button()

class CamcasticConfigWin(Gtk.Window):
  '''
  Configuration window.

  Will have a camera selection widget and dynamically generated configuration widgets
  for each selected camera.
  '''
  def __init__(self, root):
    super().__init__(Gtk.WindowType.TOPLEVEL)
    self.app = root
    self.set_title(self.app.name + ' Config Window')
    self.set_position(Gtk.WindowPosition.CENTER)
    self.set_size_request(320, 120)
    self.set_resizable(False)
    self.set_keep_above(True)
    rootconfbox = Gtk.VBox()

    '''
    #TODO hotkeys box
    '''

    '''
    #TODO Camera selection box
    '''

    exit_button_box = Gtk.HBox()

    exit = Gtk.Button("Exit")
    exit.connect('clicked', self.cb_hide, '')
    exit_button_box.pack_start(exit, True, True, 10)

    rootconfbox.pack_start(exit_button_box, True, True, 10)
    rootconfbox.show_all()
    self.add(rootconfbox)
    self.connect('delete-event', self.cb_hide, '')

  def add_camera(self, w):
    pass

  def cb_show(self, w, data):
    self.show()

  def opac_slider(self, w):
      #self.win.set_opacity(w.get_value()/100.0)
      #self.pipeline.set_state(Gst.State.PLAYING)
      pass

  def cb_hide(self, w, data, other=''):
    self.hide()
    return True