# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
from SocketServer import ThreadingTCPServer, StreamRequestHandler
import traceback
import argparse


class MyStreamRequestHandler(StreamRequestHandler):
    StreamRequestHandler.timeout = 5

    def handle(self):
        print("accept {0}".format(self.client_address))
        while True:
            try:
                data = self.rfile.read(1)
                if not data:
                    print("closed {0}".format(self.client_address))
                    return
                print("receive from {0} {1}".format(self.client_address, data))
                self.wfile.write(data)
            except:
                traceback.print_exc()
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="listening port")
    args = parser.parse_args()
    port = 44140
    if args.port:
        port = int(args.port)
        if port <= 1024 or port >= 65535:
            print("invalid port:{0}".format(port))
            return
        print("will listen port:{0}".format(port))
    else:
        print("use default port:{0}".format(port))

    address = ("", port)
    server = ThreadingTCPServer(address, MyStreamRequestHandler)
    print("listening....")
    server.serve_forever()


if __name__ == "__main__":
    main()
