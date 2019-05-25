#!/bin/bash

 nohup python  tcpechoserver.py  2>&1 1>& log/tcpechoserver.log  &

 nohup python  udpechoserver.py   2>&1 1>& log/udpechoserver.log  &

 nohup python  httpserver.py   2>&1 1>& log/httpserver.log  &

 nohup python  netstatsvr.py   2>&1 1>& log/netstatcat.log  &