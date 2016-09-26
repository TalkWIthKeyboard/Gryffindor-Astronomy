# coding=utf-8

from app.models.spiderDataModel import YearFinished
from config import (MIN_YEAR, SEARCH_PAGE, SEARCH_API)
from spiderModel import Search
from spiderParse import get_movie_pages,get_movie_ids

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
    pages = get_movie_pages(instance)
    if pages is None:
        '''
            可能被挡了，也可能这一页本来就没内容
            (需要添加log，调整间断时间)
        '''
        pass
    ids = get_movie_ids(instance)
    if ids is None:
        '''
            可能被挡了，也可能这一页本来就没内容
            (需要添加log，调整间断时间)
        '''
        pass

    y_list.extend(ids)
    if not y_list:
        '''
            这一年没有电影
            (需要添加log)
        '''
        YearFinished(year=y).save()
        '''
            间隔时间，搜索下一年
        '''
        return spider()










