import socket
import uuid
import sys
import struct
import getpass

def gethostname():
    return socket.getfqdn(socket.gethostname())


def getipbyname(hostname):
    if not hostname:
        return "127.0.1.10"
    try:
        return socket.gethostbyname(hostname)
    except Exception as e:
        print("getipbyname {0} -> {1}".format(hostname, str(e)))
        return "127.0.1.20"


def getmacaddress():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def getsystem():
    return sys.platform


def ipstr2netint(ipstr):
    return struct.unpack("I", socket.inet_aton(ipstr))[0]


def ipstr2hostint(ipstr):
    return socket.ntohl(ipstr2netint(ipstr))


def netint2ipstr(netint):
    return socket.inet_ntoa(struct.pack('I', netint))


def hostint2ipstr(hostint):
    return netint2ipstr(socket.htonl(hostint))


def is_win32():
    return sys.platform == 'win32'


def clientinfo():
    hostname = gethostname()
    ip = getipbyname(hostname)
    mac = getmacaddress()
    system = getsystem()


def main():
    hostname = gethostname()
    ip = getipbyname(hostname)
    mac = getmacaddress()
    system = getsystem()
    print(hostname)
    print(ip)
    print(mac)
    print(system)
    user_name = getpass.getuser()
    print(user_name)
    hostname = socket.gethostname()



if __name__ == '__main__':
    main()
