# -*- coding: utf-8 -*-
"""


tazzhang  2019-5-1
"""
import argparse
import socket
import json
import time

socket.setdefaulttimeout(5)


def time2datestr(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y%m%d %H:%M:%S", timeArray)
    return otherStyleTime


class UdpServer:
    def __init__(self, port):
        self.port = int(port)
        self.statlist = {}
        self.flag = 0
        self.last_dump_time= time.time()
        pass

    def process_msg(self, client_ip, msg):
        try:
            j = json.loads(msg)
            test_type = j["test_type"]
            if client_ip not in self.statlist:
                self.statlist[client_ip] = {}
            self.statlist[client_ip][test_type] = j
            self.flag = 1
        except Exception as e:
            print("json loads error:{0} msg:{1}".format(e, msg))

    def dump_list(self):
        if time.time() - self.last_dump_time <= 5:
            return

        self.last_dump_time = time.time()

        self.flag = 0

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
            width: 200px;
        }
        td
        {
            border: solid #000 1px;
        }
    </style>
        </head>
        <body>
            '''

        for client_ip, d in self.statlist.items():
            html += '''
                <p>{0}</p>
                '''.format(client_ip)
            html += '''
            <table><tr>
                 <td>test_type</td>
                 <td>conn</td>
                 <td>conn_succ</td>
                 <td>conn_fail</td>
                 <td>conn_min_time</td>
                 <td>conn_max_time</td>
                 <td>conn_avg_time</td>
                 <td>send_req</td>
                 <td>succ_count</td>
                 <td>fail_count</td>
                 <td>io_min_time</td>
                 <td>io_max_time</td>
                 <td>io_avg_time</td>
                 <td>begin_timestamp</td>
                 <td>test_time</td>
                 </tr>
            
            '''
            for test_type, j in d.items():
                tm = int(j["begin_timestamp"])
                tm = int(tm / 1000)

                failrate = 0 if j["send_req_count"] == 0 else float(j["fail_count"]) / j["send_req_count"]
                failinfo = "{0}|{1:.2f}".format(j["fail_count"], failrate)

                html += '''
                 <tr>
                 <td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td>
                 <td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td><td>{10}</td><td>{11}</td>
                 <td>{12}</td><td>{13}</td><td>{14}</td>
                 '''.format(j["test_type"],
                            j["connect_count"],
                            j["connect_succ_count"],
                            j["connect_fail_count"],
                            j["connect_min_time"],
                            j["connect_max_time"],
                            j["connect_avg_time"],
                            j["send_req_count"],
                            j["succ_count"],
                            failinfo,
                            j["io_min_time"],
                            j["io_max_time"],
                            j["io_avg_time"],
                            time2datestr(tm),
                            j["test_time"],
                            )

            html += '''
              </table>
               '''
        html += '''
        </body>
        </html>
        '''

        with open("stat.html", "w") as wf:
            wf.write(html)

    def ioctl(self, sock):
        while True:
            try:
                data, client_addr = sock.recvfrom(1024)
                print("recv from {0} {1}".format(client_addr, data))
                client_ip = client_addr[0]
                self.process_msg(client_ip, data)
            except socket.timeout:
                pass
            except Exception as e:
                print("excetipn:{0}".format(e))

            if self.flag == 1:
                self.dump_list()

    def serve_forever(self):
        addr = ("", self.port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(addr)
            print("bind succ in {0}".format(addr))
            self.ioctl(sock)
        finally:
            sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="bind port for udp")
    args = parser.parse_args()
    port = 44340
    if args.port:
        port = int(args.port)
        if port <= 1024 or port >= 65535:
            print("invalid port:{0}".format(port))
            return
        print("will bind port:{0}".format(port))
    else:
        print("use default port:{0}".format(port))

    server = UdpServer(port)
    server.serve_forever()


if __name__ == "__main__":
    main()
