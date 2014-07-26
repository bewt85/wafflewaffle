#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file
import os, time

VOTE_WINDOW = 1
VOTE_LIFE = 5*60
WINDOWS = (VOTE_LIFE / VOTE_WINDOW) + 1
DAMP_FACTOR = 0.001**(1.0/WINDOWS)

def getWindow(t):
  return int(t / VOTE_WINDOW)

count = 0.0
previousWindow = getWindow(time.time()) 

def getLatestCount(count, previousWindow, thisWindow):
  if previousWindow == thisWindow:
    return count
  else:
    return count * DAMP_FACTOR ** (thisWindow - previousWindow)

@get('/')
def index():
  index_dir = os.path.dirname(__file__)
  return static_file('index.html', index_dir)

@get('/count')
def getCount():
  global count
  global previousWindow
  t = time.time()
  thisWindow = getWindow(t)
  count = getLatestCount(count, previousWindow, thisWindow)
  previousWindow = thisWindow
  return {'count': count, 'time': t, 'window': thisWindow}

@post('/count')
def incCount():
  global count
  global previousWindow
  t = time.time()
  thisWindow = getWindow(t)
  count = 1.0 + getLatestCount(count, previousWindow, thisWindow)
  previousWindow = thisWindow
  return {'count': count, 'time': t, 'window': thisWindow}

run(server='gevent', host='localhost', port=8080, debug=True)
