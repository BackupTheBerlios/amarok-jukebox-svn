import os

import Dcop
import Debug
from Collection import Collection

class Playlist:

    def update(self):
        return Dcop.call("playlist saveCurrentPlaylist")

    def index(self):
        return int(Dcop.call("playlist getActiveIndex"))

    def isPlaying(self):
        return self.index() >= 0

    def __add(self, url):
        Debug.log("Queuing " + url)
        Dcop.call("playlist addMedia \"%s\"" % url)

    def add(self, url):
        c = Collection()
        if (c.inCollection(url)):
            self.__add(url)
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
        Dcop.call("playlist clearPlaylist")
