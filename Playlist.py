import os

import Dcop

class Playlist:

    def __init__(self):
        self.__file = os.getenv('HOME')+'/.kde/share/apps/amarok/current.xml'

    def __update(self):
        Dcop.call("playlist saveCurrentPlaylist")

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

#    def index(self):
#        return os.popen("dcop amarok playlist getActiveIndex" % url)
