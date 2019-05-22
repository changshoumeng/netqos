import socket
import uuid
import sys
import struct

def gethostname():
    return socket.getfqdn(socket.gethostname())


def getipbyname(hostname):
    return socket.gethostbyname(hostname)


def getmacaddress():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def getsystem():
    return sys.platform


def ipstr2netint(ipstr):
    return struct.unpack("I", socket.inet_aton(ipstr))[0]


def ipstr2hostint(ipstr):
    return socket.ntohl(IpStr2NetInt(ipstr))


def netint2ipstr(netint):
    return socket.inet_ntoa(struct.pack('I', netint))


def hostint2ipstr(hostint):
    return NetInt2IpStr(socket.htonl(hostint))


def main():
    hostname = gethostname()
    ip = getipbyname(hostname)
    mac = getmacaddress()
    system = getsystem()
    print(hostname)
    print(ip)
    print(mac)
    print(system)


if __name__ == '__main__':
    main()
