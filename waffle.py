#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file
import os, time

VOTE_LIFE = 5*60
DAMP_FACTOR = 0.001 ** ( 1.0 / VOTE_LIFE )

count = 0.0
lastRequest = time.time() 

def getLatestCount(count, lastUpdate, now):
  return count * DAMP_FACTOR ** (now - lastUpdate)

def twoSF(count):
  return "{0:.2f}".format(count)

@get('/')
def index():
  index_dir = os.path.dirname(__file__)
  return static_file('index.html', index_dir)

@get('/count')
def getCount():
  global count
  global lastRequest 
  t = time.time()
  count = getLatestCount(count, lastRequest, t)
  lastRequest = t
  return {'count': twoSF(count), 'time': t }

@post('/count')
def incCount():
  global count
  global lastRequest 
  t = time.time()
  count = 1 + getLatestCount(count, lastRequest, t)
  lastRequest = t
  return {'count': twoSF(count), 'time': t }

run(server='gevent', host='localhost', port=8080, debug=True)
