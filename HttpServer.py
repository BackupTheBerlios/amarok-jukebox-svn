#import posixpath
#import urllib
import os
import BaseHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

# class HttpRequestHandler(CGIHTTPRequestHandler):

#         """Translate a /-separated PATH to the local filename syntax.

#         Components that mean special things to the local file system
#         (e.g. drive or directory names) are ignored.  (XXX They should
#         probably be diagnosed.)

#         """
#         path = posixpath.normpath(urllib.unquote(path))
#         words = path.split('/')
#         words = filter(None, words)
#         path = os.getcwd() + 'www'
#         for word in words:
#             drive, word = os.path.splitdrive(word)
#             head, word = os.path.split(word)
#             if word in (os.curdir, os.pardir): continue
#             path = os.path.join(path, word)
#         return path


class HttpServer:

    def __init__(self):
        os.chdir('www')
        self.__server = BaseHTTPServer.HTTPServer(('',4475), CGIHTTPRequestHandler)
#        self.__server = BaseHTTPServer.HTTPServer(('',4475), HttpRequestHandler)
    def serve(self):
        self.__server.serve_forever()
