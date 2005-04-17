import re
import os
import sys
import BaseHTTPServer
import cgi
from CGIHTTPServer import CGIHTTPRequestHandler

# Request handlers
import browse
import playlist
import player

jukeboxState = None

class MyFieldStorage(cgi.FieldStorage):

    def __init__(self):
        self.list = []

    def append(self, item):
        self.list.append(item)

class HttpRequestHandler(CGIHTTPRequestHandler):

    __internal_path = '/jukebox/'

    def __init__(self, a, b, c):
        global jukeboxState
        self.state = jukeboxState
        CGIHTTPRequestHandler.__init__(self, a, b, c)

    def __absPath(self):
        s = self.path.split("?")
        return s[0]

    def queryParams(self):
        s = self.path.split("?")
        if len(s) <= 1:
            return {}
        else:
            return cgi.parse_qs(s[1])

    def __getFormFields(self):
        qs = self.rfile.read(int(self.headers.getheader('content-length')))
        self.form = MyFieldStorage()
        for key, value in cgi.parse_qsl(qs):
            self.form.append(cgi.MiniFieldStorage(key, value))

    def is_internal(self):
        p = re.compile('^' + self.__internal_path)
        return p.match(self.path)

    def do_HEAD(self):
        if self.is_internal():
            self.send_response(501)
        else:
            CGIHTTPRequestHandler.do_HEAD(self);
            
    def __do_internal(self):
        urls =  {
            'browse': browse,
            'player': player,
            'playlist': playlist,
        }
        p = self.__absPath()
        key = p[len(self.__internal_path):]
        if urls.has_key(key):
            if self.command == 'POST':
                self.__getFormFields()
            self.send_response(200)
            self.wfile.write(urls[key].serve(self))
        else:
            self.send_response(404)

    def do_GET(self):
        if self.is_internal():
            self.__do_internal()
        else:
            CGIHTTPRequestHandler.do_GET(self);

    def do_POST(self):
        if self.is_internal():
            self.__do_internal()
        else:
            CGIHTTPRequestHandler.do_POST(self);

class HttpServer:

    def __init__(self, state):
        global jukeboxState
        jukeboxState = state
        os.chdir(os.path.dirname(sys.argv[0]) + '/www')
        self.__server = BaseHTTPServer.HTTPServer(('',4475), HttpRequestHandler)
    def serve(self):
        self.__server.serve_forever()
