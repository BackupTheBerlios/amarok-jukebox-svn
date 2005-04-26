#!/usr/bin/python

import signal
import threading
import sys

from State import State
from AmarokEventHandler import AmarokEventHandler
from HttpServer import HttpServer

class Jukebox:

    def __exit_signal_handler(self, signal, frame):
        print "Exiting..."
        self.__eventHandler.stop()
        sys.getdefaultencoding = lambda: 'utf-8' 
        sys.exit(0)

    def __init__(self, port = -1):
        self.state = State()
        self.__eventHandler = AmarokEventHandler(self.state)
        if port == -1:
            self.__httpServer = HttpServer(self.state)
        else:
            self.__httpServer = HttpServer(self.state, port)
        signal.signal(signal.SIGINT, self.__exit_signal_handler)
        signal.signal(signal.SIGKILL, self.__exit_signal_handler)
        signal.signal(signal.SIGTERM, self.__exit_signal_handler)

    def start(self):
        self.__t = threading.Thread(target = self.__eventHandler.start)
        self.__t.start()
        self.__httpServer.serve()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        jukebox = Jukebox()
    else:
        jukebox = Jukebox(int(sys.argv[1]))        
    jukebox.start()
