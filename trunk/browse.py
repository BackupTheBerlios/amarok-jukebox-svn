import cgi
import CGI
import urllib

from Collection import Collection

def artistsHtml(c):
    s = "<h1>List of artists in collection</h1>"
    s += "<ul id='list'>"
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
    s += "<ul id='list'>"
    for ai, name in c.albumsByArtist(id):
        s += "<li><input type='checkbox' name='album' value=\"%s\" /> <a href=\"browse?album=%s&amp;from=%s\">%s</a></li>" % (ai, ai, id, cgi.escape(name.encode('utf-8')))
    s += "</ul>"
    s += "<input type='submit' name='addAlbums' value='Queue selected entire albums' />"
    s += "</form>"
    return s

def songsByAlbumHtml(c, album, artist):
    artistName = c.getName('artist', artist).encode('utf-8')
    albumName = c.getName('album', album).encode('utf-8')
    cover = c.albumCover(artistName, albumName)
    s = "<p><a href='browse?artist=%s'>Up to list of albums by %s</a></p>" % (artist, artistName)
    s += "<h1>Tracks on %s by %s</h1>" % (albumName, artistName)
    if cover is not None:
        s += "<p class='cover'><img id='cover' src='browse?cover=%s'/></p>" % cgi.escape(cover.encode('utf-8'))
    s += "<form action='playlist#playing' method='post'>"
    s += "<ol id='list'>"
    for url, title in c.songsByAlbum(album):
        s += "<li><input type='checkbox' name='song' value=\"%s\" /> <a href=\"browse?song=%s\">%s</a></li>" % (cgi.escape(url.encode('utf-8')), urllib.quote(url.encode('utf-8')), cgi.escape(title.encode('utf-8')))
    s += "</ol>"
    s += "<input type='submit' name='addSongs' value='Queue selected songs' />"
    s += "</form>"
    return s

def serveCover(request, c, cover):
    if c.isCover(cover):
        request.send_root_file(cover)
    else:
        request.send_error(404, "Cover not found")

def serve(request):
    
    c = Collection()
    qp = request.queryParams()

    if qp.has_key('cover'):
        serveCover(request, c, qp['cover'][0])
        return ''

    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()
    if qp.has_key('artists'):
        doc += artistsHtml(c)
    elif qp.has_key('artist'):
        doc += albumsByArtistHtml(c, qp['artist'][0])
    elif qp.has_key('album'):
        doc += songsByAlbumHtml(c, qp['album'][0], qp['from'][0])
    else:
        request.send_error(406, "What do you want to browse?")

    request.serve_string(doc)
