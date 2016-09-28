# coding=utf-8

from app.models.spiderDataModel import YearFinished, IdFinished
from config import (MIN_YEAR, SEARCH_PAGE, SEARCH_API)
from spiderModel import Search
from spiderParse import get_movie_pages,get_movie_ids
from app.extension.tools import get_unfinished,add_log,sleep2
from multiprocessing.dummy import Pool as ThreadPool

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
    '''
        爬虫主函数
    '''
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
    print ids
    if ids is None:
        '''
            可能被挡了，也可能这一页本来就没内容
            (需要添加log，调整间断时间)
        '''
        pass

    y_list.extend(ids)
    if not y_list:
        add_log()
        YearFinished(year=y).save()
        sleep2()
        return spider()
    pages = 1
    if pages > 1:
        p = 2
        while p <= pages:
            instance = fetch(y, p)
            add_log("开始爬取第{}年第{}页的电影信息".format(y,p),
                    'SpiderSystem',
                    '')
            ids = get_movie_ids(instance)
            if ids is None:
                '''
                    可能被挡住了，等待一段时间
                '''
            y_list.extend(ids)
            p += 1
            sleep2()
    # 感觉应该是all
    obj = IdFinished.objects(year=y).first()
    if obj is not None:
        has_finished = obj.ids
    else:
        has_finished = []
    # 这一年新增的
    to_process = get_unfinished(has_finished, y_list)
    '''
        对to_process进行电影爬虫
    '''

    # test = DetailsParse('10150')
    # test.set_url()
    # l = test()


    # 这一年的任务已经完成
    YearFinished(year=y).save()
    add_log("完成爬取第{}年所有的电影信息".format(y),
            'SpiderSystem',
            '')

if __name__ == "__main__":
    spider()














