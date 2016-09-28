# coding=utf-8

import re
from lxml import etree
from app.extension.tools import add_log
from app.spider.spiderModel import Movie
from config import MOVIE_PAGE, MOVIE_API
from collections import defaultdict
from app.spider.spiderModel import Spider
from urllib2 import HTTPError
from datetime import datetime


movie_regex = re.compile(r'http://movie.mtime.com/(\d+)/')
movie_page_regex = re.compile(r'pageindex=(\\)?"(\d+)(\\)?(\\)?"')
# 这是mtime的防爬后的提示关键句
mtime_vcodeValid_regex = re.compile(r'\"vcodeValid\":false,\"isRobot\":true')
favoritedCount_regex = re.compile(r'\"favoritedCount\":(\d+),')
rating_regex = re.compile(r'"rating":(\d.?\d),')
ratingCount_regex = re.compile(r'"ratingCount":(\d+),')
wantToSeeCount_regex = re.compile(r'"wantToSeeCount":(\d+),')
name_regex = re.compile(ur'([\u4e00-\u9fa5]+)\s+(.*)')
people_regex = re.compile(r'http://people.mtime.com/(\d+)/')
date_regex = re.compile(ur'(\d+)年(\d+)月(\d+)日')
detail_country_regex = re.compile(r'\[(.*)\]')


movie_url = 'http://movie.mtime.com/{}/{}'



class Parse(object):
    '''
        爬取标准类
    '''

    def __init__(self, movie_id):
        # defaultdict（在访问dict时如果不存在这个key会自动生成）
        self.id = movie_id
        self._alias = defaultdict(set)
        self.set_url()
        self.d = defaultdict(list)

    def set_url(self, url):
        self.url = url
        # 其中获取评论页或自动跳转走,这里保留原url供解析下一页使用
        self.original_url = url

    def xpath(self):
        '''
            这里引发了一个异常？
        '''
        pass

    def spider(self):
        # 请求头增加cc
        s = Spider(additional_headers={'Cache-Control': 'max-age=0'})
        try:
            s.fetch(self.url)
        except HTTPError as e:
            if e.msg == 'Not Found':
                return
        return etree.HTML(s.content.decode('utf-8'))

    def __call__(self):
        '''
            调用函数(可以直接调用类实例)
        '''
        self.page = self.spider()
        if self.page is None:
            return
        hasnext = self.xpath() is not None
        self.d['movieid'] = self.id
        return self.d, hasnext

    def check_next_page(self):
        '''
            检查是否有下一页
        '''
        return self.page.xpath('//a[@id=\"key_nextpage\\"]')



class FullcreditsParse(Parse):
    '''
        演职人员页面爬虫
    '''
    def set_url(self):
        self.url = movie_url.format(self.id, 'fullcredits.html')

    def xpath(self):
        common = self.page.xpath('//div[@class="credits_list"]')
        type = ['director', 'writer', 'produced', 'cinematography',
                'filmediting', 'originalmusic', 'artdirection',
                'costumedesign', 'assistantdirector']
        if len(type) > len(common):
            # 有些信息不充足
            l = len(common)
        else:
            l = len(type)
        for offset in range(l):
            c = common[offset]
            for i in c.xpath('p'):
                name = i.xpath('a')[0].text
                if name is None:
                    continue
                match = name_regex.findall(name)
                if match:
                    match = match[0]
                    self._alias[match[1]].add(match[0])
                    name = match[1]
                self.d[type[offset]] += [name]

        # 导演信息
        director = common[0]
        img = director.xpath('div/a/img')
        director_dict = {}
        if img:
            director_dict['poster'] = img[0].attrib['src']
        try:
            href = director.xpath('div/a')[0].attrib['href']
            people = people_regex.findall(href)
            # 导演id
            director_dict['mid'] = people[0]
        except IndexError:
            pass
        cn = director.xpath('div/h3/a')
        if cn:
            name = director.xpath('div/p/a')[0].text
            director_dict['name'] = name
            self._alias[name].add(cn[0].text)
        self.d['director'] = [director_dict]
        # 演员信息
        self.get_actor()

    def get_actor(self):
        actor = self.page.xpath('//div[@class="db_actor"]/dl/dd')
        for a in actor:
            one_actor = {}
            path = 'div[@class="actor_tit"]/div/'
            # 演员的个人信息页面链接和 剧中角色姓名的xpath表达式
            try:
                href = a.xpath(path + 'a')[0].attrib['href']
                name_path = 'div[@class="character_tit"]/div/h3'
            except IndexError:
                path = 'div[@class="actor_tit"]/'
                name_path = 'div/div/h3'
                href = a.xpath(path + 'h3/a')[0].attrib['href']
        people = people_regex.findall(href)
        one_actor['mid'] = people[0]
        img = a.xpath(path + 'a/img')
        if img:
            one_actor['poster'] = img[0].attrib['src']
        try:
            name = a.xpath(path + 'h3/a')[0].text
        except IndexError:
            # 只有中文名
            name = None
        one_actor['name'] = name
        cn = a.xpath(path + 'h3/a')
        if cn:
            cnname = cn[0].text
            if name is None:
                name = cnname
            self._alias[name].add(cnname)
        try:
            play = a.xpath(name_path)[-1].text
        except IndexError:
            play = ''
        one_actor['play'] = play
        self.d['actor'] += [one_actor]

class PlotParse(Parse):
    '''
        电影剧情页面爬虫
    '''
    def set_url(self):
        self.url = movie_url.format(self.id, 'plots.html')

    def xpath(self):
        all = self.page.xpath('//div[@class="plots_box"]')
        for elem in all:
            l = []
            all_p = elem.xpath('div/p')
            for p in all_p:
                try:
                    # 第一个字大写特殊处理
                    other = p.xpath('span/text()')[0]
                    txt = other + p.xpath('text()')[1]
                except IndexError:
                    # 非第一段
                    txt = p.xpath('text()')
                    '''
                        这里编码有点不一样
                    '''
                    if txt:
                        txt = txt[0]
                l.append(txt)

            # 保留了多段之间的u'\u3000\u3000'
            self.d['content'] +=l



class ScenesParse(Parse):
    '''
        幕后揭秘页面爬虫
    '''
    def set_url(self):
        self.url = movie_url.format(self.id, 'behind_the_scene.html')

    def xpath(self):
        all = self.page.xpath('//div[@class="revealed_modle"]')
        if not all:
            return
        for elem in all:
            xpath = ''
            try:
                title = elem.xpath(xpath + 'h3')[0].text
            except IndexError:
                xpath = 'div/'
                title = elem.xpath(xpath + 'h3')[0].text
            l = []
            l.extend(filter(lambda x: x.strip(), elem.xpath(xpath + 'div/p/text()|div/dl/dd/text()|div/dd/text()')))
            self.d['scene'] += [{'title': title, 'content': l}]



class DetailsParse(Parse):
    '''
        电影细节页面爬虫
    '''
    def set_url(self):
        self.url = movie_url.format(self.id, 'details.html')

    def xpath(self):
        part = self.page.xpath('//dl[@class="wp50 fl"]')
        dateXpath = self.page.xpath('//div[@class="datecont"]')
        languageXpath = self.page.xpath('//div[@class="countryname"]')

        # 更多中文外文名字和片长
        aliases = part[0].xpath('dd')
        for each in aliases:
            l = each.xpath('strong')[0].text
            movieinfo = {'cnalias': None,'enalias': None,'time': None}
            if (l == u'更多中文名：'):
                movieinfo['cnalias'] = [a.text.strip() for a in each.xpath('p')]
            elif (l == u'更多外文名：'):
                movieinfo['enalias'] = [a.text.strip() for a in each.xpath('p')]
            elif (l == u'片长：'):
                movieinfo['time'] = each.xpath('p')[0].text

        # 上映地区和时间
        release = []
        for each in range(1, len(dateXpath)):
            dict = {}
            dict['cncountry'] = languageXpath[each].xpath('p')[0].text.strip()
            dict['encountry'] = languageXpath[each].xpath('p/span')[0].text.strip()
            dict['date'] = make_datetime(dateXpath[each].text.strip())
            release.append(dict)

        # 制作/发行
        part = self.page.xpath('//dl[@id="companyRegion"]/dd/div/div[@class="fl wp49"]')
        detail = defaultdict(list)
        for p in part:
            if p.xpath('h4')[0].text == u'制作公司':
                cur_type = 'make'
            else:
                cur_type = 'publish'
            for p2 in p.xpath('ul/li'):
                name = p2.xpath('a')[0].text
                country_info = p2.xpath('span')[0].text
                match = detail_country_regex.findall(country_info)
                if match:
                    detail[cur_type] += [{'name':name, 'country':match[0]}]
                else:
                    detail[cur_type] += [{'name':name}]

        self.d['detail'] += [{'detail':detail,'release':release,'movieinfo':movieinfo}]



class AwardsParse(Parse):
    '''
        获奖情况爬虫
    '''
    def set_url(self):
        self.url = movie_url.format(self.id, 'awards.html')

    def xpath(self):
        all = self.page.xpath('//div[@id="awardInfo_data"]/dd')
        for elem in all:
            name = elem.xpath('h3/b')[0].text
            info = defaultdict(list)
            year, period, awards = 0, 0, '未知'
            try:
                yp = elem.xpath('h3/span/a')[0].text
            except:
                # 可能获了一个大奖的好几届的奖
                for e in elem.xpath('dl/child::*'):
                    if e.tag == 'dt':
                        if info:
                            self.d['awards'] += [dict(
                                name=name, year=year, period=period, awards=awards
                            )]
                            info = defaultdict(list)



def make_datetime(text):
    '''
        通过中文类型的文本解析成datetime类型的日期结果
    '''
    make = lambda t: datetime(int(t[0]) ,int(t[1]), int(t[2]))
    t = date_regex.findall(text)
    if t:
        if len(t) == 1:
            return make(t[0])
        else:
            return [make(i) for i in t]
    else:
        return datetime.now()


def get_movie_pages(instance):
    '''
        获取该年份下的总页数
    '''
    try:
        return max([int(i[1]) for i in
                    movie_page_regex.findall(instance.content)])
    except ValueError:
        # 被反爬挡住了
        if mtime_vcodeValid_regex.search(instance.content):
            add_log("被反爬机制挡住了~~",
                    "SpiderSystem",
                    "")
            return
        #只有一页
        return 1


def get_movie_ids(instance):
    '''
        获取电影的id
    '''
    if mtime_vcodeValid_regex.search(instance.content):
        add_log("被反爬机制挡住了~~",
                "SpiderSystem",
                "")
        return
    return movie_regex.findall(instance.content)



def checkmatch(regex, instance, type=int):
    '''
        抽象代码做正则表达
    '''
    match = regex.findall(instance.content)
    if not match:
        return 0
    else:
        return type(match[0])



def get_movie_info(id):
    '''
        爬电影评分页面接口
    '''
    s = Movie(params={'Ajax_CallBackArgument1': id,
                      'Ajax_RequestUrl': MOVIE_PAGE.format(
                          id=id,timestamp=Movie.get_timestamp())})
    s.fetch(MOVIE_API)
    favorited = checkmatch(favoritedCount_regex, s)
    rating = checkmatch(rating_regex, s, float)
    ratingcount = checkmatch(ratingCount_regex, s)
    want = checkmatch(wantToSeeCount_regex, s)
    del s,id
    return locals()






