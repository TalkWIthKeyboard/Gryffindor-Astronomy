#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import zlib
from config import INTERVAL

def get_user_agent():
    '''
        构造请求代理
    '''
    platform = random.choice(['Macintosh', 'Windows', 'X11'])
    if platform == 'Macintosh':
        os = random.choice(['68K', 'PPC'])
    elif platform == 'Windows':
        os = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0',
                            'Windows NT 5.0', 'Windows NT 5.1',
                            'Windows NT 5.2', 'Windows NT 6.0',
                            'Windows NT 6.1', 'Windows NT 6.2',
                            'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
    elif platform == 'X11':
        os = random.choice(['Linux i686', 'Linux x86_64'])

    browser = random.choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(random.randint(500, 599))
        version = str(random.randint(0, 24)) + '.0' + \
                str(random.randint(0, 1500)) + '.' + \
                str(random.randint(0, 999))
        return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + \
               '.0 (KHTML, live Gecko) Chrome/' + version + ' Safari/' + webkit
    elif browser == 'firefox':
        year = str(random.randint(2000, 2016))
        month = random.randint(1, 12)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        day = random.randint(1, 30)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day
        version = random.choice(map(lambda x: str(x) + '.0', range(1, 16)))
        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + \
               gecko + ' Firefox/' + version
    elif browser == 'ie':
        version = str(random.randint(1, 10)) + '.0'
        engine = str(random.randint(1, 5)) + '.0'
        option = random.choice([True,False])
        if option:
            token = random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'WOW64',
                                   'Win64; IA64', 'Win64; x64']) + '; '
        elif option is False:
            token = ''
        return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + \
               '; ' + token + 'Trident/' + engine + ')'


def deflate(data):
    '''
        deflate解压
    '''
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def get_unfinished(has, last):
    '''
        去重处理（获取last里面没有而has里面有的数据列表）
    '''
    # 集合的处理
    return list(set(last).difference(set(has)))


def sleep2(interval=None):
    '''
        sleep一定的时间
    '''
    num = interval if interval is not None else INTERVAL
    time.sleep(num)