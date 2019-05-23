import struct


def sizeof(s=""):
    type_dic = {
        "c": 1,
        "b": 1,
        "B": 1,
        "h": 2,
        "H": 2,
        "i": 4,
        "I": 4,
        "Q": 8,
    }
    a = 0
    for ch in s:
        if ch not in type_dic:
            continue
        a += type_dic[ch]
    return a


class STRING_DATA(object):
    def __init__(self, string=""):
        self.string = string

    def pack(self):
        size = len(self.string)
        fmt = ">H%ds" % (size)
        data = struct.pack(fmt, size, self.string)
        return data

    def unpack(self, data):
        if len(data) < 2:
            return 0

        size, = struct.unpack(">H", data[:2])
        if size == 0:
            return 2
        fmt = ">%ds" % (size)
        self.string, = struct.unpack(fmt, data[2:2 + size])
        return 2 + size


class ClientLogPkg(object):
    def __init__(self):
        self.timestamp = 0
        self.localip = 0
        self.remoteip = 0
        self.remoteport = 0
        self.usetick = 0
        self.code = 0
        self.comment = ""
        self.appkey = ""
        self.system = ""
        self.msg = ""
        self.args = ""
        
    def __str__(self):
        s="timestamp:{0}".format(self.timestamp)
        s += " localip:{0}".format(self.localip)
        s += " remoteip:{0}".format(self.remoteip)
        return s

    def pack(self):
        fmt = ">QIIHII"
        data = struct.pack(fmt, self.timestamp, self.localip, self.remoteip, self.remoteport, self.usetick, self.code)
        data += STRING_DATA(self.comment).pack()
        data += STRING_DATA(self.appkey).pack()
        data += STRING_DATA(self.system).pack()
        data += STRING_DATA(self.msg).pack()
        data += STRING_DATA(self.args).pack()
        return data

    def unpack(self, data):
        fmt = ">QIIHII"
        size1 = sizeof(fmt)
        # print(size1)
        if len(data) < size1:
            return 0
        head = data[:size1]
        self.timestamp, self.localip, self.remoteip, self.remoteport, self.usetick, self.code = struct.unpack(fmt, head)
        body = data[size1:]

        comment = STRING_DATA()
        size2 = comment.unpack(body)
        if size2 <= 0:
            return 0
        self.comment = comment.string
        body = body[size2:]

        appkey = STRING_DATA()
        size3 = appkey.unpack(body)
        if size3 <= 0:
            return 0
        self.appkey = appkey.string
        body = body[size3:]

        system = STRING_DATA()
        size4 = system.unpack(body)
        if size4 <= 0:
            return 0
        self.system = system.string
        body = body[size4:]

        msg = STRING_DATA()
        size5 = msg.unpack(body)
        if size5 <= 0:
            return 0
        self.msg = msg.string
        body = body[size5:]

        args = STRING_DATA()
        size6 = args.unpack(body)
        if size6 <= 0:
            return 0
        self.args = args.string
        return size1 + size2 + size3 + size4 + size5 + size6


def main():
    p = ClientLogPkg()
    p.timestamp = 1111112
    p.localip = 32333
    p.comment = "HEELL"
    p.appkey = "dafdsfsdf"

    b = p.pack()

    p2 = ClientLogPkg()
    d2 = p2.unpack(b)

    print(d2)
    pass


if __name__ == '__main__':
    main()
