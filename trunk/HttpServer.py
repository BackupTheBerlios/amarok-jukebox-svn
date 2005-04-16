import re
import os
import sys
import BaseHTTPServer
import cgi
from CGIHTTPServer import CGIHTTPRequestHandler

import browse

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

    def is_internal(self):
        p = re.compile('^' + self.__internal_path)
        return p.match(self.path)
            
    def do_GET(self):
        if self.is_internal():
            p = self.__absPath()
            if p == self.__internal_path + 'browse':
                self.send_response(200)
                doc = browse.main(self)
                self.wfile.write(doc)
            else:
                self.send_response(404)
        else:
            CGIHTTPRequestHandler.do_GET(self);

    def do_POST(self):
        if self.is_internal():
            sys.stderr.write("foo")
        else:
            CGIHTTPRequestHandler.do_POST(self);

class HttpServer:

    def __init__(self):
        os.chdir(os.path.dirname(sys.argv[0]) + '/www')
        self.__server = BaseHTTPServer.HTTPServer(('',4475), HttpRequestHandler)
    def serve(self):
        self.__server.serve_forever()
