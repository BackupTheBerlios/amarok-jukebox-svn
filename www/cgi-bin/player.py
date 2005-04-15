#!/usr/bin/python

import os
import sys
import cgi
import CGI

from Player import Player

def showActions(a):
    print "<form action='" + os.path.basename(sys.argv[0]) + "' method='post'>"
    for k in a.keys():
        print "<input type='submit' name='action' value='" + k + "' />"
    print "</form>"

def main():
    CGI.httpHeaders()
    CGI.htmlHead()
    form = cgi.FieldStorage()

    p = Player()

    definedActions =  {
        'Play': { 'action': p.play },
        'Pause': { 'action': p.playPause },
        'Stop': { 'action': p.stop },
        'Previous': { 'action': p.prev },
        'Next': { 'action': p.next },
        }

    if os.environ['REQUEST_METHOD'] == "GET":
        showActions(definedActions)
    elif os.environ['REQUEST_METHOD'] == "POST":
        if form.has_key('action'):
            action = form.getvalue('action')
            if definedActions.has_key(action):
                definedActions[action]['action']()
            else:
                print "Error!"
        showActions(definedActions)

    CGI.htmlTail()

main()
