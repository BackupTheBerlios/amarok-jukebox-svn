import sys
import select
import os

from Player import Player
from Collection import Collection

class AmarokEventHandler:

    def __init__(self):
        self.__running = True;
        self.__player = Player()

    def start(self):
        while self.__running:
            delay = 1
            fd = sys.stdin.fileno()
            (r,w,e) = select.select( [fd], [], [], delay)
            for File in r:
                if File == fd:
                    line = os.read(fd, 1024)
                    self.__dispatch(line)

    def stop(self):
        self.__running = False

    def __dispatch(self, s):
        if s.find("engineStateChange: empty" ) >= 0:
            print "Playlist empty"
            c = Collection()
            self.__player.playMedia(c.randomSong())
        else:
            print "Unknown notification: " + s + " -> ignoring"
