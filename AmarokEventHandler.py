import sys
import select
import os
import time

from Player import Player
from Collection import Collection

class AmarokEventHandler:

    def __init__(self):
        self.__running = True;
        self.__player = Player()
        self.__last = -1

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
        now = time.time()
        if s.find("engineStateChange: empty" ) >= 0:
            # The following is a trick to make stop work; there's got to be a way to talk to this
            # thread
            # Issue: it doesn't work from Amarok itself
            if (now - self.__last >= 5):
                c = Collection()
                self.__player.playMedia(c.randomSong())
            else:
                sys.stderr.write("Too soon: skipping\n")
        else:
            sys.stderr.write("Unknown notification: " + s + " -> ignoring\n")
        self.__last = now
