# coding=utf-8

import urllib
import urllib2
import socket
from lxml import etree
from app.models.ipModel import Ip
from app.core import tools
from app.models.logModel import Log
import datetime

socket.setdefaulttimeout(3)
test_url = "http://ip.chinaz.com/getip.aspx"


def checkIP(ip, port):
    '''
        检测这个代理ip是否可用
    '''
    proxy = {"http": "http://" + ip + ":" + port}
    try:
        res = urllib.urlopen(test_url, proxies=proxy).read()
        return True
    except Exception, e:
        print "这个代理不能用，错误信息：{}".format(e.message)
        return False


def makeProxies():
    '''
        爬虫可使用的IP构造proxies池
       （每天重新爬虫一次）
    '''

    Ip.drop_collection()

    # 开始爬虫
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    url = 'http://www.xicidaili.com/nn/1'
    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req).read()
    text = etree.HTML(html.decode('utf-8'))

    '''
        parse
    '''
    ip = text.xpath('//tr/td[2]')
    port = text.xpath('//tr/td[3]')
    date = text.xpath('//tr/td[last()]')

    for each in range(0, len(ip)):
        if (checkIP(ip[each].text, port[each].text)):
            save_ip = Ip(ip=ip[each].text,
                         port=port[each].text,
                         date=date[each].text)
            save_ip.save()
            print "存储第{}个IP".format(each)
        else:
            print "第{}个IP不能用！！".format(each)

    print "proxies的构建完成"

    # 记录log
    log = Log(content='proxies的构建完成',
              fromTask='系统',
              parameter='',
              createTime=datetime.datetime.now())
    log.save()
