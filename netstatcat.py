# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import argparse
import socket

import protocol
import net_util

import cat
import os

socket.setdefaulttimeout(5)


class UdpServer:
    def __init__(self, port):
        self.port = int(port)
        pass

    def process_msg(self, client_ip, msg):
        p = protocol.ClientLogPkg()
        if p.unpack(msg) <= 0:
            return

        key = "{0}:{1}{2}({3})=>{4}:{5}".format(p.appkey,
                                                p.system,
                                                client_ip,
                                                net_util.netint2ipstr(p.localip),
                                                net_util.netint2ipstr(p.remoteip),
                                                p.remoteport,
                                                )

        status = "0" if p.code == 0 else "1"
        try:
            trans = cat.Transaction("netqos_test", key)
            trans.set_status(status)
            trans.set_duration(p.usetick)
            trans.set_timestamp(p.timestamp)
        finally:
            trans.complete()

    def ioctl(self, sock):
        while True:
            try:
                data, client_addr = sock.recvfrom(1024)
                # print("recv from {0} {1}".format(client_addr, len(data)  ))
                client_ip = client_addr[0]
                self.process_msg(client_ip, data)
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
    fn = "/data/appdatas/cat/client.xml"
    if not os.path.exists(fn):
        print("not exist file:{0},to support cat".format(fn))
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="bind port for udp")
    args = parser.parse_args()
    port = 44340
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
