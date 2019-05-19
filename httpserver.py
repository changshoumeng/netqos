# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="listening port")
    args = parser.parse_args()
    port = 44340
    if args.port:
        port = int(args.port)
        if port <= 1024 or port >= 65535:
            print("invalid port:{0}".format(port))
            return
        print("will listen port:{0}".format(port))
    else:
        print("use default port:{0}".format(port))

    HandlerClass = SimpleHTTPRequestHandler
    ServerClass = BaseHTTPServer.HTTPServer
    Protocol = "HTTP/1.0"

    server_address = ('0.0.0.0', int(port))

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print ("Serving HTTP on  {0} {1}".format(sa[0], sa[1]))
    httpd.serve_forever()
    pass


if __name__ == '__main__':
    main()
