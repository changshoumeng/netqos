# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""

import argparse

import socket

import time

import netstat

socket.setdefaulttimeout(5)

gNetStat = netstat.NetStat(test_type="tcp", time_out=5)


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
    gNetStat.conn()
    is_ok, use_tick, s, err = ioconn(address)

    if not is_ok:
        gNetStat.connfail(use_tick)
        print("connect failed ", address, use_tick, err)
        return
    print("connect ok ", address, use_tick)
    gNetStat.connsucc(use_tick)
    try:
        req = "ABCD"
        for i in range(cnt):
            gNetStat.req()
            is_ok, use_tick, rsp, err = ioctl(s, req)
            if not is_ok:
                print("ioctl failed ", i, address, use_tick, err)
                gNetStat.rspfail(use_tick)
                return
            print("ioctl ok ", i, address, use_tick, len(rsp))
            gNetStat.rspsucc(use_tick)

            time.sleep(0.1)
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--host", help="remote host/ip")
    parser.add_argument("-p", "--port", help="remote port")
    args = parser.parse_args()
    if not args.host:
        print("please input remote host/ip")
        return
    if not args.port:
        print("please input remote port")
        return

    address = (args.host, int(args.port))
    print("will connect remote server:{0}".format(address))
    tcptest(address, netstat.DEFAULT_TEST_COUNT)


if __name__ == '__main__':
    main()
