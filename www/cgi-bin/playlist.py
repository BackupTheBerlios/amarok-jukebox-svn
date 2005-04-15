#!/usr/bin/python

import os
import cgi
import CGI

from Collection import Collection
from Playlist import Playlist

CGI.httpHeaders()

CGI.htmlHead()

form = cgi.FieldStorage()

c = Collection()
p = Playlist()

if os.environ['REQUEST_METHOD'] == "POST":
    if form.has_key('addSongs'):
        songs = form.getvalue('song')
        if not isinstance(songs, list):
            songs = [ songs ]
        for s in songs:
            print p.add(c, s.encode('utf-8'))
    if form.has_key('addAlbum'):
        print "Not implemented"


CGI.htmlTail()
