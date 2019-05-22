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
            if self.fail > 0:
                n = float(self.fail * 100) / float(self.fail + self.succ)
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

    def addKey(self, key):
        for k in self.keys:
            if k == key:
                return
            self.keys.append(key)

    def cnnTsAdd(self, key, timestamp, usetick, code):
        print("cnnTs {0} {1} {2} {3}".format(key, timestamp, usetick, code))
        if key not in self.cnnTs:
            self.cnnTs[key] = []
            self.addKey(key)

        tslist = self.cnnTs[key]
        if len(tslist) > 100000:
            tslist = tslist[1:]
        tslist.append(te(timestamp, usetick, code))
        self.cnnTs[key] = tslist

    def ioTsAdd(self, key, timestamp, usetick, code):
        print("ioTs {0} {1} {2} {3}".format(key, timestamp, usetick, code))
        if key not in self.ioTs:
            self.ioTs[key] = []
            self.addKey(key)

        tslist = self.ioTs[key]
        if len(tslist) > 100000:
            tslist = tslist[1:]
        tslist.append(te(timestamp, usetick, code))
        self.ioTs[key] = tslist

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

            html += '''<p>{0}</p>'''.format(k)
            html += '''
             <table><tr>
                  <td></td>
                  <td>begin</td>
                  <td>end</td>
                  <td>succ</td>
                  <td>fail</td>
                  <td>min</td>
                  <td>max</td>
                  <td>avg</td> 
                  </tr>
             '''

            if k in self.cnnTs:
                r = tl(self.cnnTs[k])
                r.start()
                html += self.formatTs("conn", r)

            if k in self.ioTs:
                r = tl(self.ioTs[k])
                r.start()
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

        with open(fn, "w") as wf:
            wf.write(html)
