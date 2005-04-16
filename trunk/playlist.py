import CGI
import sys

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
    return "<p>Added <q>" + s + "</q></p>"

def addSong(p, c, e):
    [ s ] = p.add(c, e.encode('utf-8'))
    return printSong(s)

def addAlbum(p, c, e):
    r = ""
    for s in p.addAlbum(c, int(e)):
        r += printSong(s)
    return r

def playlistToHtml(s, p):
    styledoc = libxml2.parseFile('../playlistToHtml.xsl')
    style = libxslt.parseStylesheetDoc(styledoc)
    doc = libxml2.parseFile(s)
    result = style.applyStylesheet(doc, None)
    return style.saveResultToString(result)

def serve(request):

    c = Collection()
    p = Playlist()
    player = Player()

    doc = CGI.httpHeaders()
    doc += CGI.htmlHead({ 'style':['../playlist.css'] })

    if request.command == "POST":
        form = request.form
        if form.has_key('addSongs'):
            for e in makeList(form.getvalue('song')):
                if e is not None:
                    doc += addSong(p, c, e)
        elif form.has_key('addAlbums'):
            for e in makeList(form.getvalue('album')):
                if e is not None:
                    doc += addAlbum(p, c, e)
        elif form.has_key('clear'):
            p.clear()
        elif form.has_key('clearAndStop'):
            p.clear()
            player.stop()

    f = p.update()
    doc += playlistToHtml(f, p)
    doc += CGI.htmlTail()

    return doc
