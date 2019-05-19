# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""

import httplib
import time
import netstat

gNetStat = netstat.NetStat(test_type="http", time_out=5)


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


def ioctl(ip, port, uri):
    is_ok, use_tick, rsp, err = False, 0, "", ""
    t1 = gettickcount()
    try:
        gNetStat.req()
        http_client = httplib.HTTPConnection(ip, port, timeout=5)
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
            return
        print("http test ok", i, use_tick, rsp)


def main():
    ip = "127.0.0.1"
    port = 44340
    uri = ""
    httptest(ip, port, uri, netstat.DEFAULT_TEST_COUNT)


if __name__ == '__main__':
    main()
