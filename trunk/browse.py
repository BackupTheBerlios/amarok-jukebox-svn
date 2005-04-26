import cgi
import CGI
import urllib

from Collection import Collection

def artistsHtml(c):
    s = "<ul>"
    for id, name in c.artists():
        n = cgi.escape(name.encode('utf-8'))
        if n == "":
            n = "<em>Unknown</em>"
        s += "<li><a href=\"browse?artist=%s\">%s</a></li>" % (id , n)
    s += "</ul>"
    return s

def albumsByArtistHtml(c, id):
    s = "<p><a href='browse?artists=1'>Up to list of artists</a></p>"
    s += "<h1>Albums by %s</h1>" % c.getName('artist', id).encode('utf-8')
    s += "<form action='playlist' method='post'>"
    s += "<ul>"
    for id, name in c.albumsByArtist(id):
        s += "<li><input type='checkbox' name='album' value=\"%s\" /> <a href=\"browse?album=%s\">%s</a></li>" % (id, id , cgi.escape(name.encode('utf-8')))
    s += "</ul>"
    s += "<input type='submit' name='addAlbums' value='Queue selected entire albums' />"
    s += "</form>"
    return s

def songsByAlbumHtml(c, id):
    s = "<h1>Albums by %s</h1>" % c.getName('album', id).encode('utf-8')
    s += "<form action='playlist#playing' method='post'>"
    s += "<ol>"
    for url, title in c.songsByAlbum(id):
        s += "<li><input type='checkbox' name='song' value=\"%s\" /> <a href=\"browse?song=%s\">%s</a></li>" % (cgi.escape(url.encode('utf-8')), urllib.quote(url.encode('utf-8')), cgi.escape(title.encode('utf-8')))
    s += "</ol>"
    s += "<input type='submit' name='addSongs' value='Queue selected songs' />"
    s += "</form>"
    return s

def serve(request):
    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()
    
    c = Collection()
    qp = request.queryParams()

    if request.command == "GET":
        if qp.has_key('artists'):
            doc += artistsHtml(c)
        elif qp.has_key('artist'):
            doc += albumsByArtistHtml(c, qp['artist'][0])
        elif qp.has_key('album'):
            doc += songsByAlbumHtml(c, qp['album'][0])
        else:
            print "Wrong URL!"

    doc += CGI.htmlTail()

    return doc
