#!/usr/bin/python

import os
import cgi
import CGI

import libxml2
import libxslt

from Collection import Collection
from Playlist import Playlist
from Player import Player

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

def playlistToHtml(s, p):
    styledoc = libxml2.parseFile('../playlistToHtml.xsl')
    style = libxslt.parseStylesheetDoc(styledoc)
    doc = libxml2.parseFile(s)
    result = style.applyStylesheet(doc, None)
    print style.saveResultToString(result)

def main():

    form = cgi.FieldStorage()

    c = Collection()
    p = Playlist()
    player = Player()

    CGI.httpHeaders()

    CGI.htmlHead()
        
    if os.environ['REQUEST_METHOD'] == "POST":
        if form.has_key('addSongs'):
            for e in makeList(form.getvalue('song')):
                if e is not None:
                    addSong(p, c, e)
        elif form.has_key('addAlbums'):
            for e in makeList(form.getvalue('album')):
                if e is not None:
                    addAlbum(p, c, e)
        elif form.has_key('clear'):
            p.clear()
        elif form.has_key('clearAndStop'):
            p.clear()
            player.stop()

    f = p.update()
    playlistToHtml(f, p)
    CGI.htmlTail()


main()
