# coding=utf-8

from app.models.spiderDataModel import YearFinished
from config import (MIN_YEAR, SEARCH_PAGE, SEARCH_API)
from spiderModel import Search

def get_year():
    '''
        获取现在要进行爬虫的年份(最小的)
    '''
    obj = YearFinished.objects
    if obj:
        year = obj.first()
        return year.year
    else:
        return MIN_YEAR - 1

def fetch(year, page):
    '''
        按年份爬虫入口
    '''
    s = Search(params={'Ajax_CallBack': True,
                       'Ajax_CallBackType': 'Mtime.Channel.Pages.SearchService',  # noqa
                       'Ajax_CallBackMethod': 'SearchMovieByCategory',
                       'Ajax_CrossDomain': 1,
                       'Ajax_CallBackArgument8': '',
                       'Ajax_CallBackArgument9': year,
                       'Ajax_CallBackArgument10': year,
                       'Ajax_CallBackArgument14': '1',
                       'Ajax_CallBackArgument16': '1',
                       'Ajax_CallBackArgument17': 8,
                       'Ajax_CallBackArgument18': page,
                       'Ajax_CallBackArgument19': '1',
                       'Ajax_RequestUrl': SEARCH_PAGE.format(year=year)
                       })
    s.fetch(SEARCH_API)
    return s

def spider():
    y_list = []
    y = get_year() + 1
    instance = fetch(y, 1)







