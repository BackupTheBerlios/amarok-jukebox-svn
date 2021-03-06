import Dcop
from Collection import Collection
import Debug
import urllib

class Player:

    Stopped = 0
    Pause = 1
    Playing = 2

    StatusString = [ 'Stopped', 'Pause', 'Playing', 'Unknown' ]

    def __init__(self):
        self.__status = 3

    def updateStatus(self):
        self.__status = int(Dcop.call("player status"))

    def status(self):
        return self.__status

    def play(self):
        self.updateStatus()
        if self.__status != self.Playing:
            Dcop.call("player play")

    def playPause(self):
        self.updateStatus()
        if self.__status != self.Stopped:
            Dcop.call("player playPause")

    def stop(self):
        self.updateStatus()
        if self.__status != self.Stopped:
            Dcop.call("player stop")

    def prev(self):
        Dcop.call("player prev")

    def next(self):
        Dcop.call("player next")

    def playMedia(self, url):
        Debug.log("Playing " + url)
        Dcop.call("playlist playMedia \"%s\"" % url)

    def playRandom(self, c = None):
        if c is None:
            c = Collection()
        self.playMedia(c.randomSong())

    def currentCover(self):
        return Dcop.call("player coverImage")

    def currentSong(self):
        return urllib.unquote(Dcop.call("player encodedURL"))[5:]
