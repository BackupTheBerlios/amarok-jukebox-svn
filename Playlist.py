import os

import Dcop

class Playlist:

    def __init__(self):
        self._file = os.getenv('HOME')+'/.kde/share/apps/amarok/current.xml'

    def _update(self):
        Dcop.call("playlist saveCurrentPlaylist")

    def add(self, c, url):
        if (c.inCollection(url)):
            Dcop.call("playlist addMedia \"%s\"" % url)
            return True
        else:
            return False

#    def index(self):
#        return os.popen("dcop amarok playlist getActiveIndex" % url)
