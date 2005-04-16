import cgi
import CGI

from Player import Player
from Playlist import Playlist

p = Player()

def showActions(a):
    s = "<form action='player' method='post'>"
    for k in a.keys():
        s += "<input type='submit' name='action' value='" + k + "' />"
    s += "</form>"
    return s

def play():
    p.play()
    pl = Playlist()
    if not pl.isPlaying():
        p.playRandom()

def serve(request):
    doc = CGI.httpHeaders()
    doc += CGI.htmlHead()

    definedActions =  {
        'Play': { 'action': play },
        'Pause': { 'action': p.playPause },
        'Stop': { 'action': p.stop },
        'Previous': { 'action': p.prev },
        'Next': { 'action': p.next },
        }

    if request.command == "POST":
        form = request.form
        if form.has_key('action'):
            action = form.getvalue('action')
            if definedActions.has_key(action):
                definedActions[action]['action']()
            else:
                doc += "Error!"

    doc += showActions(definedActions)

    doc += CGI.htmlTail()

    return doc
