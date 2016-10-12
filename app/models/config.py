# -*- coding: utf-8 -*-

class Config(object):
    JOBS=[

        # 开启任务扫描(添加到任务列表)
        {
            'id' : 'job1',
            'func' : 'app.task.basic.basic:add_task',
            'args' : (),
            'trigger' : {
                'type' : 'interval',
                'seconds' : 1
            }
        },

        # 开启任务扫描(过期任务踢出任务列表)
        {
            'id': 'job2',
            'func': 'app.task.basic.basic:delete_task',
            'args': (),
            'trigger': {
                'type': 'interval',
                'seconds': 1
            }
        }
    ]

    MONGODB_SETTINGS={
        'db':'Gryffindor-task',
        'hosts':'127.0.0.1',
        'port':27017
    }