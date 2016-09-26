# coding=utf-8

import re

movie_regex = re.compile(r'http://movie.mtime.com/(\d+)/')
movie_page_regex = re.compile(r'pageindex="(\d+)"')
# 这是mtime的防爬后的提示关键句
mtime_vcodeValid_regex = re.compile(r'\"vcodeValid\":false,\"isRobot\":true')

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
            print "被挡了~~~~"
            return
        #只有一页
        return 1

def get_movie_ids(instance):
    '''
        获取电影的id
    '''
    if mtime_vcodeValid_regex.search(instance.content):
        print "被挡了~~~~"
        return
    return movie_regex.search(instance.content)