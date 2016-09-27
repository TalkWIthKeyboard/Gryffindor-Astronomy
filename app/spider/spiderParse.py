# coding=utf-8

import re
from app.extension.tools import add_log
from app.spider.spiderModel import Movie
from config import MOVIE_PAGE, MOVIE_API

movie_regex = re.compile(r'http://movie.mtime.com/(\d+)/')
movie_page_regex = re.compile(r'pageindex=(\\)?"(\d+)(\\)?(\\)?"')
# 这是mtime的防爬后的提示关键句
mtime_vcodeValid_regex = re.compile(r'\"vcodeValid\":false,\"isRobot\":true')
favoritedCount_regex = re.compile(r'\"favoritedCount\":(\d+),')
rating_regex = re.compile(r'"rating":(\d.?\d),')
ratingCount_regex = re.compile(r'"ratingCount":(\d+),')
wantToSeeCount_regex = re.compile(r'"wantToSeeCount":(\d+),')



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




