#!/usr/bin/env python3

import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk
from pydbus import SessionBus
import threading

class SpotifyController(object):

    title = ""
    artist = ""
    album = ""

    def received_properties_changed_callback(self, spotify, props, bullshitstring):
        title = (props['Metadata'])['xesam:title']
        artist = (props['Metadata'])['xesam:artist'][0]
        album = (props['Metadata'])['xesam:album']
        self.metaLabel.set_label('{0} - {1} | [{2}]'.format(title, artist, album))

    def run_loop():
        self.loop.run()

    def __init__(self):
        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        buttonBox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        prevButton = Gtk.Button.new_with_label("Prev")
        playPauseButton = Gtk.Button.new_with_label("Play/Pause")
        nextButton = Gtk.Button.new_with_label("Next")
        prevButton.connect("clicked",self.on_prev_clicked)
        playPauseButton.connect("clicked", self.on_playPause_clicked)
        nextButton.connect("clicked", self.on_next_clicked)
        buttonBox.pack_end(prevButton, True, False, 0)
        buttonBox.pack_end(playPauseButton, True, False, 0)
        buttonBox.pack_end(nextButton, True, False, 0)
        self.box.pack_start(buttonBox, True, False, 2)
        self.metaLabel = Gtk.Label('{0} - {1} | [{2}]'.format(self.title, self.artist, self.album))
        self.metaLabel.set_selectable(False)
        self.box.pack_start(self.metaLabel, True, False, 2)
        self.loop = GObject.MainLoop()
        bus = SessionBus()
        self.spotify = bus.get('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        #title = self.spotify.Metadata['xesam:title']
        #artist = self.spotify.Metadata['xesam:artist'][0]
        #album = self.spotify.Metadata['xesam:album']
        self.spotify.onPropertiesChanged = self.received_properties_changed_callback
        t = threading.Thread(target=self.run_loop)
    
    
    def on_prev_clicked(self, button):
        self.spotify.Previous()
    
    def on_playPause_clicked(self, button):
        self.spotify.PlayPause()

    def on_next_clicked(self, button):
        self.spotify.Next()


class budgiespotifycontroller(GObject.GObject, Budgie.Plugin):
    """ The entrypoint for the applet
    """

    __gtype_name__ = "budgiespotifycontroller"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        return budgiespotifycontrollerApplet(uuid)

class budgiespotifycontrollerApplet(Budgie.Applet):
    """Budgie.Applet is a Gtk.Bin"""

    box = None

    def __init__(self, uuid):
        Budgie.Applet.__init__(self)

        self.app = SpotifyController()
        self.box = self.app.box
        self.add(self.box)
        self.show_all()
