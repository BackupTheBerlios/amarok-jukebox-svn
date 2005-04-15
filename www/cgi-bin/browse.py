#!/usr/bin/python

import os
import cgi
import CGI
import urllib

from Collection import Collection

def artistsHtml(c):
    s = "<ul>"
    for id, name in c.artists():
        s += "<li><a href='browse.py?artist=%s'>%s</a></li>" % (id , cgi.escape(name.encode('utf-8')))
        s += "</ul>"
    return s

def albumsByArtistHtml(c, id):
    s = "<form action='playlist.py' method='post'>"
    s += "<ul>"
    for id, name in c.albumsByArtist(id):
        s += "<li><input type='checkbox' name='album' value='%s' /> <a href='browse.py?album=%s'>%s</a></li>" % (id, id , cgi.escape(name.encode('utf-8')))
    s += "</ul>"
    s += "<input type='submit' name='addAlbums' value='Queue selected entire albums' />"
    s += "</form>"
    return s

def songsByAlbumHtml(c, id):
    s = "<form action='playlist.py' method='post'>"
    s += "<ol>"
    for url, title in c.songsByAlbum(id):
        s += "<li><input type='checkbox' name='song' value='%s' /> <a href='browse.py?song=%s'>%s</a></li>" % (cgi.escape(url.encode('utf-8')), urllib.quote(url.encode('utf-8')), cgi.escape(title.encode('utf-8')))
    s += "</ol>"
    s += "<input type='submit' name='addSongs' value='Queue selected songs' />"
    s += "</form>"
    return s

def main():
    CGI.httpHeaders()
    CGI.htmlHead()
    
    form = cgi.FieldStorage()

    c = Collection()

    if os.environ['REQUEST_METHOD'] == "GET":
        if form.has_key('artists'):
            print artistsHtml(c)
        elif form.has_key('artist'):
            print albumsByArtistHtml(c, form['artist'].value)
        elif form.has_key('album'):
            print songsByAlbumHtml(c, form['album'].value)
        else:
            print "Wrong URL!"

    CGI.htmlTail()

main()
