# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""

import argparse
import signal

import os
import socket

import time

import netstat

import multiprocessing

socket.setdefaulttimeout(60)


class GracefulExitException(Exception):
    @staticmethod
    def sigterm_handler(signum, frame):
        raise GracefulExitException()

    pass


class GracefulExitEvent(object):
    def __init__(self):
        self.exit_event = multiprocessing.Event()
        signal.signal(signal.SIGTERM, GracefulExitException.sigterm_handler)
        signal.signal(signal.SIGINT, GracefulExitException.sigterm_handler)
        print("signal.signal(signal.SIGTERM/SIGINT")
        pass

    def is_stop(self):
        return self.exit_event.is_set()

    def notify_stop(self):
        self.exit_event.set()


class CONFIG:
    APPKEY = "TCP"
    address = ("", 0)
    connnum = 10
    graceful_event = GracefulExitEvent()


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def recv_n(s, n):
    rsp = ""
    for i in range(n):
        r = s.recv(1)
        if not r:
            break
        rsp += r
        if len(rsp) >= n:
            break

    return rsp


def ioctl(s, req):
    is_ok, use_tick, rsp, err = False, 0, "", ""
    t1 = gettickcount()
    try:
        s.sendall(req)
        rsp = recv_n(s, len(req))
        t2 = gettickcount()
        use_tick = t2 - t1
        if rsp != req:
            return False, use_tick, rsp, "rsp != req;" + rsp + "|" + req
        is_ok = True
        return is_ok, use_tick, rsp, err
    except Exception as e:
        t2 = gettickcount()
        use_tick = t2 - t1
        is_ok = False
        err = str(e)
    return is_ok, use_tick, rsp, err


def ioconn(address):
    is_ok, use_tick, err = False, 0, ""
    t1 = gettickcount()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(address)
        t2 = gettickcount()
        use_tick = t2 - t1
        is_ok = True
        return is_ok, use_tick, s, err
    except socket.error as e:
        t2 = gettickcount()
        use_tick = t2 - t1
        is_ok = False
        err = str(e)
    return is_ok, use_tick, None, err


def tcptest(address, cnt):
    stat = netstat.NetStat(CONFIG.APPKEY, address[0], address[1])
    stat.start("conn")
    is_ok, use_tick, s, err = ioconn(address)

    if not is_ok:
        stat.endFail(use_tick)
        print("connect failed ", address, use_tick, err)
        return
    print("connect ok ", address, use_tick)
    stat.endSucc(use_tick)

    try:
        req = "ABCD"
        i = 0
        while True:
            i += 1
            if cnt > 0 and i >= cnt:
                break

            stat = netstat.NetStat(CONFIG.APPKEY, address[0], address[1])
            stat.start("io")

            is_ok, use_tick, rsp, err = ioctl(s, req)
            if not is_ok:
                print("ioctl failed ", i, address, use_tick, err)

                stat.endFail(use_tick)
                return
            print("ioctl ok ", i, address, use_tick, len(rsp))
            stat.endSucc(use_tick)
            time.sleep(0.1)
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="client key")
    parser.add_argument("-i", "--host", help="remote host/ip")
    parser.add_argument("-p", "--port", help="remote port")
    parser.add_argument("-c", "--connnum", help="connect number")
    parser.add_argument("-t", "--testnum", help="test number")
    args = parser.parse_args()
    if not args.key:
        print("please input key")
        return

    if not args.host:
        print("please input remote host/ip")
        return
    if not args.port:
        print("please input remote port")
        return

    connnum = 100
    if args.connnum:
        connnum = int(args.connnum)

    testnum = 100
    if args.testnum:
        testnum = int(args.testnum)

    address = (args.host, int(args.port))
    print("will connect remote server:{0} connnum:{1} testnum:{2}".format(address, connnum, testnum))

    if connnum==1:
        CONFIG.APPKEY = "keeplive{0}-{1}-{2}-{3}".format(CONFIG.APPKEY, args.key, connnum, testnum)
    else:
        CONFIG.APPKEY = "mul{0}-{1}-{2}-{3}".format(CONFIG.APPKEY, args.key, connnum, testnum)
    print(CONFIG.APPKEY)

    CONFIG.address = address
    CONFIG.connnum = connnum

    try:
        for i in range(connnum):
            tcptest(address, testnum)
    except  GracefulExitException:
        print("=======worker {0} got graceful exit exception========".format(os.getpid()))
        CONFIG.graceful_event.notify_stop()
        print("===================================================")

    print("=========END===")


if __name__ == '__main__':
    main()
