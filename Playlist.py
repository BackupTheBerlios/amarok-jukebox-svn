import os

import Dcop

class Playlist:

    def update(self):
        return Dcop.call("playlist saveCurrentPlaylist")

    def __add(self, url):
        Dcop.call("playlist addMedia \"%s\"" % url)

    def add(self, c, url):
        if (c.inCollection(url)):
            self.__add(url)
            return [ c.getSongTitle(url) ]
        else:
            return [ ]

    def addAlbum(self, c, id):
        r = [ ]
        for url, title in c.songsByAlbum(id):
            self.__add(url)
            r += [ url ]
        return map(c.getSongTitle, r)

    def clear(self):
        Dcop.call("playlist clearPlaylist")

#    def index(self):
#        return os.popen("dcop amarok playlist getActiveIndex" % url)
