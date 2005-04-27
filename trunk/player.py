import cgi
import CGI

from Player import Player
from Playlist import Playlist
import browse

def showActions(a):
    s = "<form action='player' method='post'>"
    for k in a.keys():
        s += "<input type='submit' name='action' value='" + k + "' />"
    s += "</form>"
    return s

def play(p, request):
    request.state.start()
    p.play()
    pl = Playlist()
    if not pl.isPlaying():
        p.playRandom()

def stop(p, request):
    request.state.stop()
    p.stop()

def pause(p, request):
    p.playPause()

def prev(p, request):
    p.prev()

def next(p, request):
    p.next()

def serve(request):
    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()

    definedActions =  {
        'Play': { 'action': play },
        'Pause': { 'action': pause },
        'Stop': { 'action': stop },
        'Previous': { 'action': prev },
        'Next': { 'action': next },
        }

    if request.command == "POST":
        form = request.form
        if form.has_key('action'):
            action = form.getvalue('action')
            if definedActions.has_key(action):
                p = Player()
                definedActions[action]['action'](p, request)
            else:
                request.send_error(406, "Unknown action")

    doc += "<h1>Now playing</h1>"
    doc += browse.currentlyPlaying()

    doc += "<h1>Player controls</h1>"
    doc += showActions(definedActions)

    doc += CGI.htmlTail()

    request.serve_string(doc)
