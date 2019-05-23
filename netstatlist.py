# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import time_util
import os
import time


class tl(object):
    def __init__(self, alist=[]):
        self.alist = alist
        self.min = 100000000
        self.max = 0
        self.avg = 0
        self.begin = 0
        self.end = 0
        self.succ = 0
        self.fail = 0
        self.sum = 0
        self.failrate = ""

    def start(self):
        if len(self.alist) < 2:
            return

        self.begin = self.alist[0].timestamp
        self.end = self.alist[-1].timestamp

        for a in self.alist:
            if a.code != 0:
                self.fail += 1
                continue
            self.succ += 1
            self.sum += a.usetick
            if a.usetick > self.max:
                self.max = a.usetick
            if a.usetick < self.min:
                if a.usetick != 0:
                    self.min = a.usetick

        if self.succ > 0:
            self.avg = self.sum / self.succ
            total = self.fail + self.succ
            if self.fail > 0 and total >= 1000:
                n = float(self.fail * 100) / float(total)
                self.failrate = "{0:.5f}%".format(n)


class te(object):
    def __init__(self, timestamp, usetick, code):
        self.timestamp = timestamp
        self.usetick = usetick
        self.code = code

    def __str__(self):
        return "timestamp:{0} usetick:{1} code:{2}".format(self.timestamp, self.usetick, self.code)


class ts(object):
    def __init__(self):
        self.cnnTs = {}
        self.ioTs = {}
        self.keys = []

        self.tm = time_util.ymdh(time.time())
        self.dir = "stat"
        self.f = 0

    def addKey(self, key):
        for k in self.keys:
            if k == key:
                print("repeat key:{0}".format(key))
                return
        self.keys.append(key)
        print("add key:{0}".format(key))


    def delKey(self, key):
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                print("del key:{0}".format(key))
                del self.keys[i]
                return

    def reducelist(self, alist):
        min_pos, max_pos = 0, 0
        min_val = 10000000
        max_val = 0
        for i in range(len(alist)):
            a = alist[i]
            if a.usetick > max_val:
                max_val = a.usetick
                max_pos = i
                continue
            if a.usetick < min_val:
                min_val = a.usetick
                min_pos = i
                continue
        x = min(min_pos, max_pos)
        y = max(min_pos, max_pos)
        b = alist[0:x] + alist[x + 1:y] + alist[y + 1:]
        return b

    def cleanExpireTe(self, alist):
        currenttick = time_util.gettickcount()
        blist = []

        for a in alist:
            if currenttick > a.timestamp + 3600 * 1000 * 2:
                continue
            blist.append(a)
        return blist

    def check(self):
        dels = []
        for k in self.keys:
            if k in self.cnnTs:
                alist = self.cnnTs[k]
                if len(alist) > 0:
                    blist = self.cleanExpireTe(alist)
                    self.cnnTs[k] = blist
                    if len(blist) == 0:
                        dels.append(k)
            if k in self.ioTs:
                alist = self.ioTs[k]
                if len(alist) > 0:
                    blist = self.cleanExpireTe(alist)
                    self.ioTs[k] = blist
                    if len(blist) == 0:
                        dels.append(k)
        if len(dels) == 0:
            return
        for k in dels:
            self.delKey(k)
            if k in self.cnnTs:
                del self.cnnTs[k]
            if k in self.ioTs:
                del self.ioTs[k]

    def cnnTsAdd(self, key, timestamp, usetick, code):
        # print("cnnTs {0} {1} {2} {3}".format(key, timestamp, usetick, code))
        if key not in self.cnnTs:
            self.cnnTs[key] = []
            self.addKey(key)

        tslist = self.cnnTs[key]
        if len(tslist) > 100000:
            tslist = self.reducelist(tslist)
        tslist.append(te(timestamp, usetick, code))
        self.cnnTs[key] = tslist
        self.f = 1

    def ioTsAdd(self, key, timestamp, usetick, code):
        # print("ioTs {0} {1} {2} {3}".format(key, timestamp, usetick, code))
        if key not in self.ioTs:
            self.ioTs[key] = []
            self.addKey(key)

        tslist = self.ioTs[key]
        if len(tslist) > 100000:
            tslist = self.reducelist(tslist)
        tslist.append(te(timestamp, usetick, code))
        self.ioTs[key] = tslist
        self.f = 1

    def formatTs(self, ty, r):
        html = """
              <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}|{5}</td>
                <td>{6}</td>
                <td>{7}</td>
                <td>{8}</td> 
                </tr>
              """.format(
            ty,
            time_util.ymdhms(r.begin / 1000),
            time_util.ymdhms(r.end / 1000),
            r.succ,
            r.fail, r.failrate,
            r.min,
            r.max,
            r.avg
        )

        # print(html)
        return html

    def dumphtml(self):
        if len(self.keys) == 0:
            return

        self.check()

        if self.f == 0:
            return

        html = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>stat</title>
                        <style type="text/css">
                table
                {
                    border-collapse: collapse;
                    border: none;
                    width: 800px;
                }
                td
                {
                    border: solid #000 1px;
                }
            </style>
                </head>
                <body>
                    '''
        for k in self.keys:

            html += '''<p>客户端：{0}</p>'''.format(k)
            html += '''
             <table><tr>
                  <td>测试指标</td>
                  <td>开始时间</td>
                  <td>结束时间</td>
                  <td>成功个数</td>
                  <td>失败个数</td>
                  <td>最小时延</td>
                  <td>最大时延</td>
                  <td>平均时延</td> 
                  </tr>
             '''

            if k in self.cnnTs:
                r = tl(self.cnnTs[k])
                r.start()
                if r.begin > 0:
                    html += self.formatTs("connection", r)

            if k in self.ioTs:
                r = tl(self.ioTs[k])
                r.start()
                if r.begin > 0:
                    html += self.formatTs("io", r)

            html += ''' </table> '''
        html += '''</body></html>'''

        fn = os.path.join(self.dir, "stat.html")
        tm = time_util.ymdh(time.time())
        if os.path.exists(fn):
            if tm != self.tm:
                self.tm = tm
                try:
                    fn2 = os.path.join(self.dir, "stat{0}.html".format(self.tm))
                    os.rename(fn, fn2)
                except Exception as e:
                    print ('rename file fail;{0}'.format(e))
                    pass

        self.f =0
        with open(fn, "w") as wf:
            wf.write(html)




def main():
    t = ts()
    for i in xrange(52):
        t.ioTsAdd("k1", 11111, 11 * i + 1, 0)
    t.dumphtml()
    pass


if __name__ == '__main__':
    main()
