# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import argparse
import httplib
import time
import netstat

gNetStat = netstat.NetStat(test_type="http", time_out=30)


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def ioctl(ip, port, uri):
    is_ok, use_tick, rsp, err = False, 0, "", ""
    t1 = gettickcount()
    try:
        gNetStat.req()
        http_client = httplib.HTTPConnection(ip, port, timeout=30)
        http_client.request('GET', uri)
        r = http_client.getresponse()
        use_tick = gettickcount() - t1
        if 200 != r.status:
            is_ok = False
            gNetStat.rspfail(use_tick)
            return is_ok, use_tick, "", r.reason
        rsp = r.read()
        if not rsp:
            is_ok = False
            gNetStat.rspfail(use_tick)
            return is_ok, use_tick, "", "data is nil"
        is_ok = True
        gNetStat.rspsucc(use_tick)
        return is_ok, use_tick, rsp, ""
    except Exception as e:
        use_tick = gettickcount() - t1
        is_ok = False
        err = str(e)
        gNetStat.rspfail(use_tick)
    return is_ok, use_tick, rsp, err


def httptest(ip, port, uri, cnt):
    for i in range(cnt):
        is_ok, use_tick, rsp, err = ioctl(ip, port, uri)
        if not is_ok:
            print("http test failed", i, use_tick, err)
            time.sleep(3)
            continue
        print("http test ok", i, use_tick, rsp)
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--host", help="remote host/ip")
    parser.add_argument("-p", "--port", help="remote port")
    parser.add_argument("-t", "--testnum", help="test number")
    args = parser.parse_args()
    if not args.host:
        print("please input remote host/ip")
        return
    if not args.port:
        print("please input remote port")
        return
    testnum = 1000
    if args.testnum:
        testnum = int(args.testnum)

    ip = args.host
    port = int(args.port)
    uri = ""
    gNetStat.setTestInfo(connect_num=0, test_num=testnum)
    httptest(ip, port, uri, testnum)


if __name__ == '__main__':
    main()
