import BaseHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

class HttpServer:

    def __init__(self):
        self.__server = BaseHTTPServer.HTTPServer(('',4475), CGIHTTPRequestHandler)
    def serve(self):
        self.__server.serve_forever()
