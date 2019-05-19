# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import argparse
import socket


class UdpServer:
    def __init__(self, port):
        self.port = int(port)
        pass

    def ioctl(self, sock):
        while True:
            try:
                data, client_addr = sock.recvfrom(1024)
                print("recv from {0} {1}".format(client_addr, data))
                sock.sendto(data, client_addr)
            except socket.timeout:
                pass
            except Exception as e:
                print("excetipn:{0}".format(e))

    def serve_forever(self):
        addr = ("", self.port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(addr)
            print("bind succ in {0}".format(addr))
            self.ioctl(sock)
        finally:
            sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="bind port for udp")
    args = parser.parse_args()
    port = 44140
    if args.port:
        port = int(args.port)
        if port <= 1024 or port >= 65535:
            print("invalid port:{0}".format(port))
            return
        print("will bind port:{0}".format(port))
    else:
        print("use default port:{0}".format(port))

    server = UdpServer(port)
    server.serve_forever()


if __name__ == "__main__":
    main()
