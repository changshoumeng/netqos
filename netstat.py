# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import time
import json
import socket
import protocol
import net_util
import time_util


def packclientlog(appkey, remoteip, remoteport, msg, args, usetick, code, comment=""):
    p = protocol.ClientLogPkg()
    hostname = net_util.gethostname()
    localip = net_util.getipbyname(hostname)
    p.localip = net_util.ipstr2netint(localip)
    p.remoteip = net_util.ipstr2netint(remoteip)
    p.remoteport = remoteport
    p.system = net_util.getsystem()+hostname
    p.appkey = appkey
    p.msg = msg
    p.args = args
    p.code = code
    p.comment = comment
    p.timestamp = time_util.gettickcount()
    p.usetick = usetick
    return p.pack()


class NetStat:
    def __init__(self, appkey="", remoteip="", remoteport=0):
        self.start_timestamp = time_util.gettickcount()
        self.appkey = appkey
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.usetick = 0
        self.timestamp = 0
        self.code = 0
        self.msg = ""
        self.args = ""
        self.comment = ""
        self.f = 0

    def start(self, msg, args=""):
        self.start_timestamp = time_util.gettickcount()
        self.msg = msg
        self.args = args
        self.code = 0
        self.comment = ""
        self.f = 0

    def end(self, ts, code=0, comment=""):
        if self.f == 0:
            self.code = code
            self.comment = comment
            self.timestamp = ts
            self.usetick = self.timestamp - self.start_timestamp
            self.report()
            self.f = 1

    def endSucc(self, tick):
        if self.f == 0:
            self.code = 0
            self.usetick = tick
            self.timestamp = time_util.gettickcount() 
            self.f = 1
            self.report()

    def endFail(self, tick):
        if self.f == 0:
            self.code = 1
            self.usetick = tick
            self.timestamp = time_util.gettickcount()
            self.f = 1
            self.report()

    def __del__(self):
        self.end(time_util.gettickcount(), 0, "")

    def report(self):
        req = packclientlog(self.appkey, self.remoteip, self.remoteport, self.msg, self.args, self.usetick, self.code,
                            comment="")
        address = ("103.21.119.8", 44340)
        #address = ("127.0.0.1", 44340)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(req, address)
            #print(len(req))
        except Exception as e:
            print(e)
        finally:
            sock.close()


def test(i):
    n = NetStat("K1", "23.13.3.3", 3212)
    n.start("conn", "")
    time.sleep(i * 0.1)


def main():
    for i in range(100):
        test(i)


if __name__ == '__main__':
    main()
    print("EXI")
