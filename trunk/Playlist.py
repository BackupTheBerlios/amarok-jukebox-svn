import urllib
import os

import Dcop
import Debug
from Collection import Collection

class Playlist:

    def __init__(self):
        self.__dcop = Dcop.init()
        self.__dcop = self.__dcop.playlist

    def update(self):
        return self.__dcop.saveCurrentPlaylist()

    def index(self):
        return int(self.__dcop.getActiveIndex())

    def isPlaying(self):
        return self.index() >= 0

    def __add(self, url):
        Debug.log("Queuing " + url)
        self.__dcop.addMedia(url)

    def add(self, url):
        c = Collection()
        if (c.inCollection(url)):
            self.__add(urllib.quote(url))
            return [ c.songTitle(url) ]
        else:
            return [ ]

    def addAlbum(self, id):
        c = Collection()
        r = [ ]
        for url, title in c.songsByAlbum(id):
            self.__add(url)
            r += [ url ]
        return map(c.songTitle, r)

    def clear(self):
        self.__dcop.clearPlaylist()

    def playRandom(self):
        # FIXME: the history should be saved here
        self.clear()
        c = Collection()
        self.playMedia(c.randomSong())

    def playMedia(self, url):
        Debug.log("Playing " + url)
        self.__dcop.playMedia(urllib.quote(url))
            
