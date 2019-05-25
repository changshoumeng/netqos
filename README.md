# netqos
    网络质量测试,基于python实现的，轻量级网络质量测试程序；使用echo一个字节，进行测试；

    author:tazzhang

# 环境要求
    python2.7.x版本

    python其他版本，还没经过测试；


# 服务部署


#### 1. 部署 tcpechoserver.py

    nohup python  tcpechoserver.py  2>&1 1>& log/tcpechoserver.log  &
    
    外网开通44140 TCP端口

#### 2. 部署 udpechoserver.py

    nohup python  udpechoserver.py   2>&1 1>& log/udpechoserver.log  &

    外网开通44140 UDP端口


#### 3. 部署 httpserver.py

    nohup python  httpserver.py   2>&1 1>& log/httpserver.log  &

    外网开通44340 TCP端口

#### 4. 部署 netstatsvr.py

    nohup python  netstatsvr.py   2>&1 1>& log/netstatsvr.log  &

    外网开通44340 UDP端口


# 测试运行

    python tcpechoclient.py -i 127.0.0.1 -p 44140 -t 100000 -c 1
    python tcpechoclient.py -i 127.0.0.1 -p 44140 -t 100 -c 100
    python udpechoclient.py -i 127.0.0.1 -p 44140 -t 10000
    python httpclient.py  -i 127.0.0.1 -p 44340 -t 1000

# 测试结果
    http://127.0.0.1:44340/stat.html
    
    客户端：10.0.100.2/UDP-guangzhou--1linux2/127.0.0.1=>103.21.119.8:44140

    测试指标	开始时间	结束时间	成功个数	失败个数	最小时延	最大时延	平均时延
    io	20190522 19:38:15	20190522 19:49:02	4852	1|0.02061%	31	46	31
    客户端：10.0.100.2/UDP-zt--1win32/172.16.8.211=>103.21.119.8:44140
    
    测试指标	开始时间	结束时间	成功个数	失败个数	最小时延	最大时延	平均时延
    io	20190522 19:39:08	20190522 19:48:59	607	1|	8	304	24
    客户端：10.0.100.2/TCP-qdsvrsyh-10000-10linux2/172.31.142.209=>103.21.119.8:44140
    
    测试指标	开始时间	结束时间	成功个数	失败个数	最小时延	最大时延	平均时延
    connection	20190522 19:39:19	20190522 19:49:01	453	0|	19	23	19
    io	20190522 19:39:19	20190522 19:49:02	4075	0|	37	59	40
    
    
## Py Cat 安装环境

     sudo yum install python-devel*
     sudo yum install gcc
    sudo yum install  libffi*
    sudo easy_install cffi
    