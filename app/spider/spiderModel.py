# coding=utf-8
'''
    爬虫相关类的定义
'''

import urllib
import urllib2
import cookielib
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from gzip import GzipFile
from app.extension.tools import get_user_agent,deflate
from datetime import datetime
from collections import OrderedDict


class ContentEncodingProcessor(urllib2.BaseHandler):
    '''
        构造有解压功能的handler
    '''
    cookiejar = None

    def __init__(self, cookie_support, additional_headers):
        self.additional_headers = additional_headers
        if cookie_support:
            '''
               CookieJar类是用来保存cookie
            '''
            self.cookiejar = cookielib.CookieJar()

    def http_request(self, req):
        req.add_header('Accept-Encoding','gzip, deflate')
        req.add_header('User-Agent', get_user_agent)
        req.add_header('Accept-Language',
                       'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
        if self.additional_headers is not None:
            req.headers.update(self.additional_headers)
        if self.cookiejar is not None:
            self.cookiejar.add_cookie_header(req)
        return req

    def http_response(self, req, resp):
        if self.cookiejar is not None:
            self.cookiejar.extract_cookies(resp , req)
        # 页面没有压缩
        if resp.headers.get("content-encoding") not in ('gzip', 'deflate'):
            return  resp
        old_resp = resp
        content = resp.read()

        # gzip压缩
        if resp.headers.get("content-encoding") == 'gzip':
            gz = GzipFile(
                fileobj=StringIO(content),
                mode="r"
            )

        # deflate压缩
        elif resp.headers.get("content-encoding") == 'deflate':
            gz = StringIO(deflate(content))
        resp = urllib2.addinfourl(
            gz, old_resp.headers, old_resp.url, old_resp.code)
        resp.msg = old_resp.msg
        return resp


class Spider(object):
    '''
        基础爬虫类
        fetch为爬虫入口，返回结果html
    '''
    def __init__(self,
                 cookie_support=True,
                 additional_headers=None,
                 params={}):
        self.cookie_support = cookie_support
        self.additional_headers = additional_headers
        self.params = params

    def make_query(self):
        return {}

    def fetch(self,url):
        opener = urllib2.build_opener(
            ContentEncodingProcessor(self.cookie_support,
                                     self.additional_headers),
            urllib2.HTTPHandler
        )
        urllib2.install_opener(opener)
        params = urllib.urlencode(self.make_query())
        if params:
            url = '{}?{}'.format(url, params)
        req = urllib2.Request(url)
        self.content = urllib2.urlopen(req).read()

    @classmethod
    def get_timestamp(cls):
        now = datetime.now()
        timestamp = ''
        for i in (now.year, now.month, now.day, now.hour, now.minute,
                  now.second, str(now.microsecond)[:5]):
            timestamp += str(i)
        return timestamp

class Search(Spider):
    '''
        搜索电影列表用的爬虫
    '''
    def make_query(self):
        params = self.params
        if not isinstance(params, OrderedDict):
            d = OrderedDict()
            d['Ajax_CallBack'] = params['Ajax_CallBack']
            d['Ajax_CallBackType'] = params['Ajax_CallBackType']
            d['Ajax_CallBackMethod'] = params['Ajax_CallBackMethod']
            d['Ajax_CrossDomain'] = params['Ajax_CrossDomain']
            d['Ajax_RequestUrl'] = params['Ajax_RequestUrl']
            d['t'] = self.get_timestamp()
            for i in range(20):
                param = 'Ajax_CallBackArgument' + str(i)
                d[param] = params.get(param, 0)
            return d
        else:
            return params

class Movie(Spider):
    '''
        搜索单个电影信息用的爬虫
    '''
    def make_query(self):
        params = self.params
        if not isinstance(params, OrderedDict):
            d = OrderedDict()
            d['Ajax_CallBack'] = True
            service = 'Mtime.Community.Controls.CommunityPages.DatabaseService'
            d['Ajax_CallBackType'] = service
            d['Ajax_CallBackMethod'] = 'LoadData2'
            d['Ajax_CrossDomain'] = 1
            d['Ajax_RequestUrl'] = params['Ajax_RequestUrl']
            d['Ajax_CallBackArgument0'] = 1
            d['Ajax_CallBackArgument1'] = params['Ajax_CallBackArgument1']
            return d
        else:
            return params

class Comment(Spider):
    '''
        搜索电影影评用的爬虫
    '''
    def make_query(self):
        params = self.params
        if not isinstance(params, OrderedDict):
            d = OrderedDict()
            d['Ajax_CallBack'] = True
            d['Ajax_CallBackType'] = 'Mtime.Library.Services'
            d['Ajax_CallBackMethod'] = 'GetMovieReviewAndTweetCountInfo'
            d['Ajax_CrossDomain'] = 1
            d['Ajax_RequestUrl'] = params['Ajax_RequestUrl']
            d['t'] = self.get_timestamp()
            d['Ajax_CallBackArgument0'] = params['Ajax_CallBackArgument0']
            d['Ajax_CallBackArgument1'] = params['Ajax_CallBackArgument1']
            return d
        else:
            return params
