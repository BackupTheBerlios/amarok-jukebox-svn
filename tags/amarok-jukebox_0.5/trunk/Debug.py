import datetime

# This needs to be made configurable

logfile = '/tmp/amarok-jukebox.log'

def log(s):
    f = open(logfile, 'a')
    if f == None:
        return
    f.write("[%s] %s\n" % (datetime.datetime.now(), s))
    f.close()
