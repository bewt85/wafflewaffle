#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

count = 0

from bottle import route, run, get, post

@get('/')
def index():
  global count
  return "Counter: %s" % count

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
