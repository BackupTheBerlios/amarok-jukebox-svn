from Player import Player

class State:

    def __init__(self):
        p = Player()
        p.updateStatus()
        self.__running = not p.status() == p.Stopped

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False

    def isRunning(self):
        return self.__running
