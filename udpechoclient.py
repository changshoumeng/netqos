# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import argparse
import socket
import time

import netstat

gNetStat = netstat.NetStat(test_type="udp", time_out=5)

socket.setdefaulttimeout(5)


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def recv_n(s, n):
    rsp = ""
    for i in range(n):
        r, server_addr = s.recvfrom(1024)
        if not r:
            break
        rsp += r
        if len(rsp) >= n:
            break

    return rsp, server_addr


class UdpClient:
    def __init__(self, address):
        self.address = address
        pass

    def ioctl(self, s, req):
        is_ok, use_tick, rsp, err = False, 0, "", ""
        t1 = gettickcount()
        try:
            s.sendto(req, self.address)
            rsp, server_addr = recv_n(s, len(req))
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

    def start(self, cnt=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            req = "ABCD"
            i = 0
            while True:
                i += 1
                if cnt > 0 and i >= cnt:
                    break
                gNetStat.req()
                is_ok, use_tick, rsp, err = self.ioctl(sock, req)
                if not is_ok:
                    print("ioctl failed ", i, self.address, use_tick, err)
                    gNetStat.rspfail(use_tick)
                    time.sleep(3)
                    continue
                print("ioctl ok ", i, self.address, use_tick, len(rsp))
                gNetStat.rspsucc(use_tick)
                time.sleep(0.1)

        finally:
            sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="client key")
    parser.add_argument("-i", "--host", help="remote host/ip")
    parser.add_argument("-p", "--port", help="remote port")
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
    testnum = 10000
    if args.testnum:
        testnum = int(args.testnum)

    address = (args.host, int(args.port))
    print("will connect udp server:{0} testnum:{1}".format(address,testnum))

    gNetStat.setTestInfo(client_key=args.key,connect_num=0,test_num=testnum)
    client = UdpClient(address)
    client.start(cnt=testnum)


if __name__ == "__main__":
    main()
