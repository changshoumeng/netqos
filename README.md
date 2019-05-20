# netqos
    网络质量测试,基于python实现的，轻量级网络质量测试程序；使用echo一个字节，进行测试；


# 环境要求
    python2.7.x版本

    python其他版本，还没经过测试；


# 服务部署


#### 1. 部署 tcpechoserver.py

    nohup python  tcpechoserver.py   2>&1 1>&/dev/null  &
    
    外网开通44140 TCP端口

#### 2. 部署 udpechoserver.py

    nohup python  udpechoserver.py   2>&1 1>&/dev/null  &

    外网开通44140 UDP端口


#### 3. 部署 httpserver.py

    nohup python  httpserver.py   2>&1 1>&/dev/null  &

    外网开通44340 TCP端口

#### 4. 部署 netstatsvr.py

    nohup python  netstatsvr.py   2>&1 1>&/dev/null  &

    外网开通44340 UDP端口


# 测试运行

    python tcpechoclient.py -i 127.0.0.1 -p 44140 -t 100000 -c 1
    python tcpechoclient.py -i 127.0.0.1 -p 44140 -t 100 -c 100
    python udpechoclient.py -i 127.0.0.1 -p 44140 -t 10000
    python httpclient.py  -i 127.0.0.1 -p 44340 -t 1000

# 测试结果
    http://127.0.0.1:44340/stat.html