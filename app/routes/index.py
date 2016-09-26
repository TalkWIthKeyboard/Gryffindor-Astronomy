# -*- coding: utf-8 -*-
from app import app

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/test')
def test():
    print 'test'
    return app.send_static_file('index.html')
