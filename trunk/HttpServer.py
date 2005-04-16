import re
import os
import sys
import BaseHTTPServer
import cgi
from CGIHTTPServer import CGIHTTPRequestHandler

# Request handlers
import browse
import playlist

class MyFieldStorage(cgi.FieldStorage):

    def __init__(self):
        self.list = []

    def append(self, item):
        self.list.append(item)



class HttpRequestHandler(CGIHTTPRequestHandler):

    __internal_path = '/jukebox/'

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
            
    def do_GET(self):
        if self.is_internal():
            p = self.__absPath()
            if p == self.__internal_path + 'browse':
                self.send_response(200)
                self.wfile.write(browse.main(self))
            else:
                self.send_response(404)
        else:
            CGIHTTPRequestHandler.do_GET(self);

    def do_POST(self):
        if self.is_internal():
            p = self.__absPath()
            self.__getFormFields()
            if p == self.__internal_path + 'playlist':
                self.send_response(200)
                self.wfile.write(playlist.main(self))
            else:
                self.send_response(404)
        else:
            CGIHTTPRequestHandler.do_POST(self);

class HttpServer:

    def __init__(self):
        os.chdir(os.path.dirname(sys.argv[0]) + '/www')
        self.__server = BaseHTTPServer.HTTPServer(('',4475), HttpRequestHandler)
    def serve(self):
        self.__server.serve_forever()
