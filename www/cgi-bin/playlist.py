#!/usr/bin/python

import os
import cgi
import CGI

from Collection import Collection
from Playlist import Playlist

def makeList(a):
    if not isinstance(a, list):
        a = [ a ]
    return a

def printSong(s):
    print "<p>Added <q>" + s + "</q></p>"

def addSong(p, c, e):
    [ s ] = p.add(c, e.encode('utf-8'))
    printSong(s)

def addAlbum(p, c, e):
    for s in p.addAlbum(c, int(e)):
        printSong(s)

def main():
    CGI.httpHeaders()
    CGI.htmlHead()

    form = cgi.FieldStorage()

    c = Collection()
    p = Playlist()

    if os.environ['REQUEST_METHOD'] == "POST":
        if form.has_key('addSongs'):
            for e in makeList(form.getvalue('song')):
                addSong(p, c, e)
        elif form.has_key('addAlbums'):
            for e in makeList(form.getvalue('album')):
                addAlbum(p, c, e)

    CGI.htmlTail()

main()
