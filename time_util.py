import time


def gettickcount():
    current_time = time.time()
    return int(round(current_time * 1000))

def ymdhms(timeStamp):
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y%m%d %H:%M:%S", timeArray)


def ymdh(timeStamp):
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y%m%d%H", timeArray)