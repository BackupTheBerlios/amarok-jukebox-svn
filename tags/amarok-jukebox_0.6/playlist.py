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

def addSong(p, e):
    [ s ] = p.add(e)
    return printSong(s)

def addAlbum(p, e):
    r = ""
    for s in p.addAlbum(int(e)):
        r += printSong(s)
    return r

def playlistToHtml(s, p):
    styledoc = libxml2.parseFile('../playlistToHtml.xsl')
    style = libxslt.parseStylesheetDoc(styledoc)
    doc = libxml2.parseFile(s)
    result = style.applyStylesheet(doc, None)
    return style.saveResultToString(result)

def serve(request):

    p = Playlist()
    player = Player()

    doc = CGI.httpHeaders()
    doc += CGI.htmlHead({ 'style':['../playlist.css'] })

    if request.command == "POST":
        form = request.form
        if form.has_key('addSongs'):
            for e in makeList(form.getvalue('song')):
                if e is not None:
                    doc += addSong(p, e)
        elif form.has_key('addAlbums'):
            for e in makeList(form.getvalue('album')):
                if e is not None:
                    doc += addAlbum(p, e)
        elif form.has_key('clear'):
            p.clear()
        elif form.has_key('clearAndStop'):
            p.clear()
            request.state.stop()
            player.stop()

    f = p.update()
    doc += playlistToHtml(f, p)
    doc += CGI.htmlTail()

    request.serve_string(doc)
