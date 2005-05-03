import urllib
import time

import Dcop
from Collection import Collection
from Playlist import Playlist
import Debug

class Player:

    Stopped = 0
    Pause = 1
    Playing = 2
    Unknown = 3

    StatusString = [ 'Stopped', 'Pause', 'Playing', 'Unknown' ]

    def __init__(self):
        self.__status = self.Unknown

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
        while True:
            Dcop.call("playlist playMedia \"%s\"" % url)
            # FIXME: sometimes, the above doesn't work (why?)
            # Trying to fix it by checking that it got the order after the call was made
            time.sleep(2)
            if self.currentSong() == url:
                break
            else:
                Debug.log("ERROR: Huh, something went wrong; trying to queue the song again")
            

    def playRandom(self):
        # FIXME: the history should be saved here
        p = Playlist()
        p.clear()
        c = Collection()
        self.playMedia(c.randomSong())

    def currentCover(self):
        return Dcop.call("player coverImage")

    def currentSong(self):
        return urllib.unquote(Dcop.call("player encodedURL"))[5:]

    def trackCurrentTime(self):
        return int(Dcop.call("player trackCurrentTime"))

    def trackTotalTime(self):
        return int(Dcop.call("player trackTotalTime"))
