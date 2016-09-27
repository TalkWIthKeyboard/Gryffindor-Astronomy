#!/usr/bin/env bash
pip install virtualenv
virtualenv flask
flask/bin/pip install --upgrade pip
flask/bin/pip install setuptools --no-use-wheel --upgrade
flask/bin/pip install flask==0.9
flask/bin/pip install flask-login
flask/bin/pip install flask-openid
flask/bin/pip install flask-mail==0.7.6
flask/bin/pip install sqlalchemy==0.7.9
flask/bin/pip install flask-sqlalchemy==0.16
flask/bin/pip install sqlalchemy-migrate==0.7.2
flask/bin/pip install flask-whooshalchemy==0.54a
flask/bin/pip install flask-wtf==0.8.4
flask/bin/pip install pytz==2013b
flask/bin/pip install flask-babel==0.8
flask/bin/pip install flup
flask/bin/pip install Flask-APScheduler
flask/bin/pip install Flask-Celery
flask/bin/pip install pymongo
flask/bin/pip install requests
flask/bin/pip install mongoengine
flask/bin/pip install flask-mongoengine
flask/bin/pip install utils
flask/bin/pip install lxml
