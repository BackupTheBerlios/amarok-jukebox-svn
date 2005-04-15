#!/usr/bin/python

import signal
import threading
import sys

from AmarokEventHandler import AmarokEventHandler
from HttpServer import HttpServer

class Jukebox:

    def __exit_signal_handler(self, signal, frame):
        print "Exiting..."
        self.__eventHandler.stop()
        sys.exit(0)

    def __init__(self):
        self.__eventHandler = AmarokEventHandler()
        self.__httpServer = HttpServer()
        signal.signal(signal.SIGINT, self.__exit_signal_handler)
        signal.signal(signal.SIGKILL, self.__exit_signal_handler)
        signal.signal(signal.SIGTERM, self.__exit_signal_handler)

    def start(self):
        self.__t = threading.Thread(target = self.__eventHandler.start)
        self.__t.start()
        self.__httpServer.serve()

if __name__ == "__main__":
    jukebox = Jukebox()
    jukebox.start()
