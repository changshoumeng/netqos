import httplib
import net_util


def http_get(host, port=80, uri=""):
    http_client = httplib.HTTPConnection(host, port, timeout=30)
    http_client.request('GET', uri)
    r = http_client.getresponse()
    if 200 != r.status:
        return r.status, r.reason
    rsp = r.read()
    return 0, rsp


def main():
    host = "ip.cn"
    ip = net_util.getipbyname(host)
    print ip
    uri = "/"
    status, rsp = http_get(host, port=80, uri=uri)
    print(status)
    print(rsp)


if __name__ == '__main__':
    main()
