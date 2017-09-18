#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib, Gio
import requests
import random


class XKCDReader(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name("xkcdreader")
        GLib.set_prgname('xkcdreader')
        json = self.get_current()
        self.number = int(json["num"])
        self.title = json["title"]
        self.highest_number = self.number
        img, self.hoover = self.parse_json(json)
        self.pixbuf = self.get_image(img)
        self.connect("activate", self.on_activate)

    def exit(self, *args):
        self.quit()

    def on_activate(self, app):
        self.win = Gtk.ApplicationWindow(Gtk.WindowType.TOPLEVEL, application=app)
        self.win.set_title("XKCD Reader - {}".format(self.title))
        self.win.set_icon_name('xkcdreader')
        self.win.set_border_width(12)
        self.win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        #self.win.set_resize_mode(Gtk.ResizeMode.IMMEDIATE);


        # boxes
        vboxall = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vboxmain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vboxpicture = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        hboxbuttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vboxbuttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.win.add(vboxall)

        #buttons
        buttoncurrent = Gtk.Button("   Current", image=Gtk.Image(stock=Gtk.STOCK_NEW))
        buttoncurrent.set_always_show_image (True)
        buttonprev = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_BACK))
        buttonnext = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_FORWARD))
        buttonrandom = Gtk.Button("   Random", image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
        buttonrandom.set_always_show_image(True)

        #number entry_changed
        self.numberentry = Gtk.Entry()
        self.numberentry.set_max_length(4)
        self.numberentry.set_width_chars(4)
        self.numberentry.set_max_width_chars(4)
        self.numberentry.set_text(str(self.number))
        
        #image
        self.image = Gtk.Image()
        self.image.set_from_pixbuf(self.pixbuf)
        pixbuf_height = self.pixbuf.get_height()
        pixbuf_width = self.pixbuf.get_width()
        self.image.set_tooltip_text(self.hoover)
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(pixbuf_width, pixbuf_height)
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.add_with_viewport(self.image)
        vboxpicture.pack_start(self.scrolled_window, True, True, 0)
        vboxpicture.set_margin_bottom(20)


        #pack buttons
        hboxbuttons.pack_start(buttoncurrent, False, False, 12)
        hboxbuttons.pack_start(buttonprev, False, False, 0)
        hboxbuttons.pack_start(self.numberentry, False, False, 2)
        hboxbuttons.pack_start(buttonnext, False, False, 0)
        hboxbuttons.pack_start(buttonrandom, False, False, 12)
        #hboxbuttons.set_margin_left(2000)
        #hboxbuttons.set_margin_right(2000)
        halign = Gtk.Alignment.new(0.5, 0, 0, 0)
        halign.add(hboxbuttons)
        vboxbuttons.pack_start(halign, False, True, 0)


        # button cancel
        buttonclose = Gtk.Button("_Exit", use_underline=True)
        buttonclose.get_style_context().add_class("destructive-action")


        hboxcancel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hboxcancel.set_margin_right(10)
        hboxcancel.pack_end(buttonclose, False, False, 0)
        hboxcancel.set_margin_top(10)
        vboxall.pack_end(hboxcancel, False, False, 6)


        # packing
        vboxall.pack_start(vboxmain, True, True, 0)
        vboxmain.pack_end(vboxbuttons, False, False, 0)
        vboxmain.pack_start(vboxpicture, False, False, 0)
        

        #signals
        buttonclose.connect("clicked", self.exit)
        self.numberentry.connect("activate", self.number_changed)
        buttonprev.connect("clicked", self.on_prev_clicked)
        buttonnext.connect("clicked", self.on_next_clicked)
        buttoncurrent.connect("clicked", self.on_current_clicked)
        buttonrandom.connect("clicked", self.on_random_clicked)


        self.win.show_all()
        self.add_window(self.win)

    def parse_json(self, json):
        r = requests.get(json["img"])
        image = r.content
        hoover_text = json["alt"]
        return image, hoover_text

    def get_current(self):
        url = requests.get("http://xkcd.com/info.0.json")
        json = url.json()
        return json
    
    def get_number(self, number):
        url = requests.get("https://xkcd.com/{}/info.0.json".format(number))
        json = url.json()
        return json

    def get_image(self, image):
        loader = GdkPixbuf.PixbufLoader()
        loader.write(image)
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf
        
    def change_image(self):
        json = self.get_number(self.number)
        img, self.hoover = self.parse_json(json)
        self.pixbuf = self.get_image(img)
        pixbuf_height = self.pixbuf.get_height()
        pixbuf_width = self.pixbuf.get_width()
        off_height = 180
        off_width = 24
        buf_height = pixbuf_height + off_height
        buf_width = pixbuf_width + off_width
        pixbuf_width = self.pixbuf.get_width()
        screen = Gdk.Screen.get_default()
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        
        if buf_height > screen_height and buf_width < screen_width:
            self.scrolled_window.set_size_request(pixbuf_width, screen_height - off_height)
        elif buf_height < screen_height and buf_width > screen_width:
            self.scrolled_window.set_size_request(screen_width - off_width, pixbuf_height)
        elif buf_height > screen_height and buf_width > screen_width:
            self.scrolled_window.set_size_request(screen_width - off_width, screen_height - off_height)
        else:
            self.scrolled_window.set_size_request(pixbuf_width, pixbuf_height)

        self.image.set_from_pixbuf(self.pixbuf)
        self.image.set_tooltip_text(self.hoover)
        self.win.set_title("XKCD Reader - {}".format(json["title"]))
        height = self.win.get_preferred_height().natural_height
        width = self.win.get_preferred_width().natural_width
        self.win.resize(width, height)
        


    def on_next_clicked(self, widget):
        self.number += 1
        if self.number > self.highest_number:
            self.number = self.highest_number
        self.change_image()
        self.numberentry.set_text(str(self.number))

    def on_prev_clicked(self, widget):
        self.number += -1
        if self.number == 0:
            self.number = 1
        self.change_image()
        self.numberentry.set_text(str(self.number))

    def on_current_clicked(self, widget):
        self.number = self.highest_number
        self.change_image()
        self.numberentry.set_text(str(self.number))

    def on_random_clicked(self, widget):
        self.number = random.randint(1,win.highest_number)
        self.change_image()
        self.numberentry.set_text(str(self.number))

    def number_changed(self, widget):
        try:
            val = int(widget.get_text())
            if val > self.highest_number:
                val = self.highest_number
            self.number = val
            self.change_image()
            widget.set_text(str(val))
        except ValueError:
            widget.set_text('')

if __name__ == "__main__": 
    win = XKCDReader()
    win.run(None)
