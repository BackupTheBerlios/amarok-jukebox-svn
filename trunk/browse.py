import cgi
import CGI
import urllib

import Debug
from Collection import Collection
from Player import Player

def artistsHtml():
    c = Collection()
    s = "<h1>List of artists in collection</h1>"
    s += "<ul id='list'>"
    for id, name in c.artists():
        n = cgi.escape(name)
        if n == "":
            n = "<em>Unknown</em>"
        s += "<li><a href=\"browse?artist=%s\">%s</a></li>" % (id , n)
    s += "</ul>"
    return s

def albumsByArtistHtml(id):
    c = Collection()
    s = "<p><a href='browse?artists=1'>Up to list of artists</a></p>"
    s += "<h1>Albums by %s</h1>" % c.getName('artist', id)
    s += "<form action='playlist' method='post'>"
    s += "<ul id='list'>"
    for ai, name in c.albumsByArtist(id):
        s += "<li><input type='checkbox' name='album' value=\"%s\" /> <a href=\"browse?album=%s&amp;from=%s\">%s</a></li>" % (ai, ai, id, cgi.escape(name))
    s += "</ul>"
    s += "<input type='submit' name='addAlbums' value='Queue selected entire albums' />"
    s += "</form>"
    return s

def songsByAlbumHtml(album, artist):
    c = Collection()
    artistName = c.getName('artist', artist)
    albumName = c.getName('album', album)
    s = "<p><a href='browse?artist=%s'>Up to list of albums by %s</a></p>" % (artist, artistName)
    s += "<h1>Tracks on %s by %s</h1>" % (albumName, artistName)
    s += albumCoverP(artistName, albumName)
    s += "<form action='playlist#playing' method='post'>"
    s += "<ol id='list'>"
    for url, title in c.songsByAlbum(album):
        s += "<li><input type='checkbox' name='song' value=\"%s\" /> <a href=\"browse?song=%s\">%s</a>" % (cgi.escape(url), urllib.quote(url), cgi.escape(title))
        coll = Collection()
        d = coll.songDetails(url)
        # FIXME: this is because of http://bugs.kde.org/show_bug.cgi?id=104769
        if d is not None:
            s += " (%s)" % d['length']
        s += "</li>"
    s += "</ol>"
    s += "<input type='submit' name='addSongs' value='Queue selected songs' />"
    s += "</form>"
    return s

def albumCoverMarkup(s):
    try:
        import Image
        try:
            im = Image.open(s)
        except IOError:
            return "<!-- No cover found -->"
        height, width = im.size
        if (height > 150):
            height = "height='150'"
        else:
            height = ""
    except:
        Debug.log("WARNING: install PIL")
        height = "height='150'"
    return "<p class='cover'><img id='cover' %s src='browse?cover=%s'/></p>" % (height, cgi.escape(s))

def albumCoverP(artist, album):
    c = Collection()
    cover = c.albumCover(artist, album)
    if cover is not None:
        return albumCoverMarkup(cover)
    else:
        return ""

def songHtml(song, level = 1, cover = True):
    c = Collection()
    d = c.songDetails(song)
    # FIXME
    if d is None:
        return "<p>Sorry, you've been struck by <a href='http://bugs.kde.org/show_bug.cgi?id=104769'>amaroK bug #104769</a>.</p>"
    s = "<h%d>%s</h%d>" % (level, d['title'], level)
    if cover:
        s += albumCoverP(d['artist'], d['album'])
    s += "<dl>"
    s += "<dt>Artist</dt>"
    s += "<dd>%s</dd>" % d['artist']
    s += "<dt>Album</dt>"
    s += "<dd>%s</dd>" % d['album']
    s += "<dt>Length</dt>"
    s += "<dd>%s</dd>" % d['length']
    s += "<dt>Year</dt>"
    s += "<dd>%s</dd>" % d['year']
    s += "<dt>Genre</dt>"
    s += "<dd>%s</dd>" % d['genre']
    s += "<dt>Bitrate</dt>"
    s += "<dd>%s</dd>" % d['bitrate']
    s += "</dl>"
    s += "<form action='playlist#playing' method='post'>"
    s += "<input type='hidden' name='song' value=\"%s\" />" % cgi.escape(song)
    s += "<input type='submit' name='addSongs' value='Queue song' />"
    s += "</form>"
    return s

def serveCover(request, cover):
    c = Collection()
    if c.isCover(cover):
        request.send_root_file(cover, 600, "image/jpeg")
    else:
        request.send_error(404, "Cover not found")

def currentlyPlaying():
    p = Player()
    p.updateStatus()
    if p.status() == p.Stopped:
        return "<p><em>Nothing</em></p>"
    s = albumCoverMarkup(p.currentCover())
    song = p.currentSong()
    c = Collection()
    s += songHtml(song, level = 2, cover = False)
    remaining = p.trackTotalTime() -  p.trackCurrentTime()
    s += "<p class='current'>Remaining: %s:%02d</p>" % (remaining / 60, remaining % 60)
    return s

def serve(request):
    
    qp = request.queryParams()

    if qp.has_key('cover'):
        serveCover(request, qp['cover'][0])
        return ''

    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()
    if qp.has_key('artists'):
        doc += artistsHtml()
    elif qp.has_key('artist'):
        doc += albumsByArtistHtml(qp['artist'][0])
    elif qp.has_key('album'):
        doc += songsByAlbumHtml(qp['album'][0], qp['from'][0])
    elif qp.has_key('song'):
        doc += songHtml(qp['song'][0])
    else:
        request.send_error(406, "What do you want to browse?")
    doc += CGI.htmlTail()

    request.serve_string(doc)
