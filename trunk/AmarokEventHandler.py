import sys
import select
import os
import Debug

from Player import Player
from Playlist import Playlist
import Dcop

class AmarokEventHandler:

    def __init__(self, state):
        self.__running = True;
        self.__player = Player()
        self.__state = state
        Dcop.call("player enableRandomMode false")

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
        Debug.log("Event received: " + s)
        if s.find("engineStateChange: empty" ) >= 0:
            if self.__state.isRunning():
                self.__player.playRandom()
        elif s.find("trackChange" ) >= 0:
            pl = Playlist()
            if not pl.isPlaying():
                self.__player.playRandom()                
