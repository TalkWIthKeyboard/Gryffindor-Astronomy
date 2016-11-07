# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/files')

'''
状态量
'''

TASK_STOP = 0
TASK_RUNNING = 1
TASK_HANG = 2

SYSTEM_STOP = 0
SYSTEM_RUNNING = 1



'''
爬虫常量
'''

# 爬取页面间的间隔, 单位s
INTERVAL = 16
# 提示验证码的重试间隔
VERIFY_INTERVAL = 1200

#爬取得年份设置
MIN_YEAR = 1980

# 电影查询, 根据年代, 电影名
SEARCH_PAGE = 'http://movie.mtime.com/movie/search/section/#sortType=8&viewType=1&year={year}'  # noqa

# MTIME的搜索结果是通过api和javascript动态添加的
SEARCH_API = 'http://service.channel.mtime.com/service/search.mcs'

# 获取电影基本信息
MOVIE_API = 'http://service.mtime.com/database/databaseService.m'

MOVIE_PAGE = 'http://movie.mtime.com/{id}/&t={timestamp}'

# 获取评论的评论转发赞
COMMENT_API = 'http://service.library.mtime.com/Movie.api'