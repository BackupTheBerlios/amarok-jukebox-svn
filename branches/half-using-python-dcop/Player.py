import urllib

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
        self.__dcop = Dcop.init()
        self.__dcop = self.__dcop.player

    def updateStatus(self):
        self.__status = int(self.__dcop.status())

    def status(self):
        return self.__status

    def play(self):
        self.updateStatus()
        if self.__status != self.Playing:
            self.__dcop.play()

    def playPause(self):
        self.updateStatus()
        if self.__status != self.Stopped:
            self.__dcop.playPause()

    def stop(self):
        self.updateStatus()
        if self.__status != self.Stopped:
            self.__dcop.stop()

    def prev(self):
        self.__dcop.prev()

    def next(self):
        self.__dcop.next()

    def currentCover(self):
        return self.__dcop.coverImage()

    def currentSong(self):
        return urllib.unquote(self.__dcop.encodedURL())[5:]

    def trackCurrentTime(self):
        return int(self.__dcop.trackCurrentTime())

    def trackTotalTime(self):
        return int(self.__dcop.trackTotalTime())
