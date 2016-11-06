# coding=utf-8

from app.models.spiderModel import YearFinished, IdFinished, Fullcredits, Plot, Scenes, Details, Awards, Comment, Score, BasicInfo
from app.core.spider.parse import (get_movie_pages, get_movie_ids, get_movie_info,
                                   FullcreditsParse, PlotParse, ScenesParse, DetailsParse, AwardsParse, CommentParse, BasicInfoParse)
from app.core.spider.basic import get_year, fetch
from app.core.spider.tools import get_unfinished, sleep2
from app.core.tools import add_log

def spider():
    '''
        电影爬虫主函数
    '''
    y_list = []
    y = get_year() + 1
    flag = False

    add_log('开始爬取第{}年所有的电影信息\n'.format(y),'spider','')
    instance = fetch(y, 1)
    pages = get_movie_pages(instance)
    if pages is None:
        return spider()
    ids = get_movie_ids(instance)
    if ids is None:
        return spider()

    y_list.extend(ids)
    if not y_list:
        YearFinished(year=y).save()
        sleep2()
        return spider()
    pages = 1
    if pages > 1:
        p = 2
        while p <= pages:
            flag = True
            instance = fetch(y, p)
            ids = get_movie_ids(instance)
            if ids is None:
                continue
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
    add_log('第{}年有{}个的电影信息,实爬虫{}个\n'.format(y, len(to_process), len(y_list)), 'spider', '')
    '''
        对to_process进行电影爬虫
    '''
    num = 0
    for each in to_process:
        num += 1
        # 演职人员页面爬虫
        spider_by_db_id(FullcreditsParse, Fullcredits, each)
        # 电影剧情页面爬虫
        spider_by_db_id(PlotParse, Plot, each)
        # 幕后揭秘页面爬虫
        spider_by_db_id(ScenesParse, Scenes, each)
        # 获奖情况爬虫
        spider_by_db_id(AwardsParse, Awards, each)
        #  电影评论爬虫
        spider_by_db_id(CommentParse, Comment, each)
        details_spider(each)
        score_spider(each)
        basic_spider(each)

    # 这一年的任务已经完成
    if flag:
        YearFinished(year=y).save()
        IdFinished(year=y, ids=to_process).save()
        add_log('完成爬取第{}年所有的电影信息\n'.format(y), 'spider', '')
    else:
        add_log('爬取第{}年所有的电影信息失败，重新爬\n'.format(y), 'spider', '')
    spider()

'''
    模块爬虫任务
    （方便主爬虫函数直接调用，也方便后面改为多线程）
'''

def spider_by_db_id(spider_class, db, id):
    '''
    爬虫结果存到相对应的表
    :param db: 表名
    :param id: 电影id
    :return:
    '''
    try:
        spider = spider_class(id)
        ans = spider()
        for each in ans:
            if each != False:
                db(**each).save()
    except Exception,e:
        print e

def details_spider(id):
    '''
        电影细节页面爬虫
    '''
    try:
        spider = DetailsParse(id)
        ans = spider()
        for each in ans:
            if each != False:
                detail = each['detail']
                movieid = each['movieid']
                for detail_each in detail:
                    if detail_each != False:
                        detail_each['movieid'] = movieid
                        Details(**detail_each).save()
    except Exception,e:
        print e

def score_spider(id):
    '''
        电影得分爬虫
    '''
    try:
        score = get_movie_info(id)
        Score(**score).save()
    except Exception,e:
        print e

def basic_spider(id):
    '''
        电影基本信息爬虫
    '''
    try:
        spider = BasicInfoParse(id)
        ans = spider()
        for each in ans:
            if each != False:
                obj_each = {}
                obj_each['info'] = each['info'][0]
                obj_each['movieid'] = each['movieid']
                BasicInfo(**obj_each).save()
    except Exception,e:
        print e
        basic_spider(id)


