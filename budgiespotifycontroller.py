#!/usr/bin/env python3

import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk
from pydbus import SessionBus

class SpotifyController(object):

    def received_properties_changed_callback(spotify, props, bullshitstring):
        title = (props['Metadata'])['xesam:title']
        artist = (props['Metadata'])['xesam:artist'][0]
        album = (props['Metadata'])['xesam:album']
        #print('{0} - {1} | [{2}]'.format(title, artist, album))

    def __init__(self):
        self.box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        prevButton = Gtk.Button.new_with_label("Prev")
        playPauseButton = Gtk.Button.new_with_label("Play/Pause")
        nextButton = Gtk.Button.new_with_label("Next")
        prevButton.connect("clicked",self.on_prev_clicked)
        playPauseButton.connect("clicked", self.on_playPause_clicked)
        nextButton.connect("clicked", self.on_next_clicked)
        self.box.pack_end(prevButton, True, False, 2)
        self.box.pack_end(playPauseButton, True, False, 2)
        self.box.pack_end(nextButton, True, False, 2)
        loop = GObject.MainLoop()
        bus = SessionBus()
        self.spotify = bus.get('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        title = self.spotify.Metadata['xesam:title']
        artist = self.spotify.Metadata['xesam:artist'][0]
        album = self.spotify.Metadata['xesam:album']
        #spotify.onPropertiesChanged = self.received_properties_changed_callback
    
    
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
