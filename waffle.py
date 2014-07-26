#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

count = 0

from bottle import route, run, get, post, static_file
import os

@get('/')
def index():
  index_dir = os.path.dirname(__file__)
  return static_file('index.html', index_dir)

@get('/count')
def getCount():
  global count
  return {'count': count}

@post('/count')
def incCount():
  global count
  count += 1
  return {'count': count}

run(server='gevent', host='localhost', port=8080, debug=True)
