#!/usr/bin/env python3.3

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

class MyIndicator:
  def __init__(self, root):
    self.app = root
    self.ind = appindicator.Indicator.new(
                self.app.name,
                "indicator-messages",
                appindicator.IndicatorCategory.APPLICATION_STATUS)
    self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    self.menu = Gtk.Menu()
    item = Gtk.MenuItem()
    item.set_label("Main Window")
    item.connect("activate", self.app.main_win.cb_show, '')
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

  def cb_exit(self, w, data):
     Gtk.main_quit()

class MyConfigWin(Gtk.Window):
  def __init__(self, root):
    super().__init__()
    self.app = root
    self.set_title(self.app.name + ' Config Window')

  def cb_show(self, w, data):
    self.show()

class MyMainWin(Gtk.Window):
  def __init__(self, root):
    super().__init__()
    self.app = root
    self.set_title(self.app.name)

  def cb_show(self, w, data):
    self.show()

class MyApp(Gtk.Application):
  def __init__(self, app_name):
    super().__init__()
    self.name = app_name
    self.main_win = MyMainWin(self)
    self.conf_win = MyConfigWin(self)
    self.indicator = MyIndicator(self)

  def run(self):
    Gtk.main()

if __name__ == '__main__':
  app = MyApp('Scaffold')
  app.run()