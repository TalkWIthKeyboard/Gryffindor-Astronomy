# coding=utf-8

from app.models.spiderModel import YearFinished,IdFinished,Fullcredits,Plot,Scenes,Details
from app.core.spider.parse import get_movie_pages,get_movie_ids,FullcreditsParse,PlotParse,ScenesParse,DetailsParse
from app.core.spider.basic import get_year,fetch
from app.core.spider.tools import get_unfinished,sleep2
from app.core.tools import add_log
from multiprocessing.dummy import Pool as ThreadPool


def spider():
    '''
        爬虫主函数
    '''
    y_list = []
    y = get_year() + 1
    instance = fetch(y, 1)
    pages = get_movie_pages(instance)
    if pages is None:
        # 可能被挡了，也可能这一页本来就没内容(需要添加log，调整间断时间)
        pass
    ids = get_movie_ids(instance)
    print ids
    if ids is None:
        # 可能被挡了，也可能这一页本来就没内容(需要添加log，调整间断时间)
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
                # 可能被挡住了，等待一段时间
                pass
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
    details_spider('10170')

    # 这一年的任务已经完成
    YearFinished(year=y).save()
    add_log("完成爬取第{}年所有的电影信息".format(y),
            'SpiderSystem',
            '')

def fullcredits_spider(id):
    '''
        演职人员页面爬虫
    '''
    try:
        spider = FullcreditsParse(id)
        spider.set_url()
        ans = spider()
        for each in ans:
            if each != False:
                Fullcredits(**each).save()
    except Exception,e:
        print e

def plot_spider(id):
    '''
        电影剧情页面爬虫
    '''
    try:
        spider = PlotParse(id)
        spider.set_url()
        ans = spider()
        for each in ans:
            if each != False:
                Plot(**each).save()
    except Exception,e:
        print e

def scenes_spider(id):
    '''
        幕后揭秘页面爬虫
    '''
    try:
        spider = ScenesParse(id)
        spider.set_url()
        ans = spider()
        for each in ans:
            if each != False:
                Scenes(**each).save()
    except Exception,e:
        print e

def details_spider(id):
    '''
        电影细节页面爬虫
    '''
    try:
        spider = DetailsParse(id)
        spider.set_url()
        ans = spider()
        for each in ans:
            if each != False:
                Details(**each).save()
    except Exception,e:
        print e


if __name__ == '__main__':
    spider()