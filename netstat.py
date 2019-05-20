# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import time
import json
import socket


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))


DEFAULT_TEST_COUNT = 10000


def min_list(alist=[]):
    blist = [i for i in alist if i != 0]
    if not blist:
        return 0
    return min(blist)


class NetStat:
    def __init__(self, test_type="tcp", time_out=5):
        self.test_type = test_type
        self.time_out = time_out
        self.connect_count = 0
        self.connect_succ_count = 0
        self.connect_fail_count = 0

        self.send_req_count = 0
        self.recv_rsp_count = 0
        self.io_time_list = [0]
        self.connect_time_list = [0]
        self.succ_count = 0
        self.fail_count = 0
        self.begin_timestamp = gettickcount()
        self.end_timestamp = 0

    def reset(self):
        self.connect_count = 0
        self.connect_succ_count = 0
        self.connect_fail_count = 0

        self.send_req_count = 0
        self.recv_rsp_count = 0
        self.io_time_list = [0]
        self.connect_time_list = [0]
        self.succ_count = 0
        self.fail_count = 0
        self.begin_timestamp = gettickcount()
        self.end_timestamp = 0

    def getTestKey(self):
        timeArray = time.localtime(time.time())
        otherStyleTime = time.strftime("%m%d%H", timeArray)
        return otherStyleTime

    def setTestInfo(self, connect_num=0, test_num=0):
        self.connect_num = connect_num
        self.test_num = test_num
        self.test_key = self.getTestKey()

    def updateTestKey(self):
        current_test_key = self.getTestKey()
        if current_test_key != self.test_key:
            self.test_key = current_test_key
            self.reset()


    def req(self):
        self.send_req_count += 1

    def rspsucc(self, use_tick):
        self.succ_count += 1
        self.end_timestamp = gettickcount()
        self.io_time_list.append(use_tick)
        self.flush()

    def rspfail(self, use_tick):
        self.fail_count += 1
        self.end_timestamp = gettickcount()
        self.io_time_list.append(use_tick)
        self.flush()

    def conn(self):
        self.connect_count += 1

    def connsucc(self, use_tick):
        self.connect_succ_count += 1
        self.end_timestamp = gettickcount()
        self.connect_time_list.append(use_tick)
        self.flush()

    def connfail(self, use_tick):
        self.connect_fail_count += 1
        self.end_timestamp = gettickcount()
        self.connect_time_list.append(use_tick)
        self.flush()

    def report(self, req="123"):
        address = ("103.21.119.8", 44340)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(req, address)
        except Exception as e:
            print(e)
        finally:
            sock.close()

    def flush(self):
        self.updateTestKey()
        d = {}
        d["test_type"] = "{0}/{1}/{2}/{3}".format(self.test_type, self.connect_num, self.test_num, self.test_key)
        d["connect_count"] = self.connect_count
        d["connect_succ_count"] = self.connect_succ_count
        d["connect_fail_count"] = self.connect_fail_count
        d["connect_min_time"] = min_list(self.connect_time_list)
        d["connect_max_time"] = max(self.connect_time_list)
        d["connect_avg_time"] = sum(self.connect_time_list) / len(self.connect_time_list)

        d["send_req_count"] = self.send_req_count
        d["succ_count"] = self.succ_count
        d["fail_count"] = self.fail_count
        d["io_min_time"] = min_list(self.io_time_list)
        d["io_max_time"] = max(self.io_time_list)
        d["io_avg_time"] = sum(self.io_time_list) / len(self.io_time_list)

        d["begin_timestamp"] = self.begin_timestamp
        d["test_time"] = self.end_timestamp - self.begin_timestamp
        j = json.dumps(d)
        self.report(j)


def main():
    s = NetStat()
    s.conn()
    s.connsucc(4)

    s.conn()
    s.connsucc(6)

    s.req()
    s.rspfail(3)

    s.req()
    s.rspsucc(8)
    s.flush()


if __name__ == '__main__':
    main()
