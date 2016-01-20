#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

LISTEN_PORT = 80

if __name__ == '__main__':
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", LISTEN_PORT), Handler)

    print "Serving at port", LISTEN_PORT
    httpd.serve_forever()
