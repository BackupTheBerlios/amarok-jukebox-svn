import sys
import select
import os
import Debug

from Playlist import Playlist
import Dcop

class AmarokEventHandler:

    def __init__(self, state):
        self.__running = True;
        self.__playlist = Playlist()
        self.__state = state
        dcop = Dcop.init()
        dcop.player.enableRandomMode(False)

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
            Debug.log("Playlist is empty!")
            if self.__state.isRunning():
                Debug.log("Queuing random song")
                self.__playlist.playRandom()
            else:
                Debug.log("Not running")
        elif s.find("trackChange" ) >= 0:
            if not self.__playlist.isPlaying():
                Debug.log("Queuing random song")
                self.__playlist.playRandom()
