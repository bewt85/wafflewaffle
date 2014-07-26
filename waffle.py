#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file
import os, time
from collections import deque

VOTE_LIFE = 5*60
DAMP_FACTOR = 0.001 ** ( 1.0 / VOTE_LIFE )

HISTORY_LENGTH = 10*60
history = deque([ 0.0 for i in range(HISTORY_LENGTH) ])
lastUpdate = time.time() 

def updatedHistory(history, lastUpdate, now):
  if int(now) == int(lastUpdate):
    history[0] = getLatestCount(history[0], lastUpdate, now)
    return history
  history[0] = getLatestCount(history[0], lastUpdate, int(lastUpdate)+1)
  lastUpdate = int(lastUpdate) + 1
  for t in range(lastUpdate + 1, int(now)):
    history.pop()
    history.appendleft(getLatestCount(history[0], lastUpdate, t))
    lastUpdate = t
  history.pop()
  history.appendleft(getLatestCount(history[0], lastUpdate, now))
  return history 

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
  global history 
  global lastUpdate 
  t = time.time()
  history = updatedHistory(history, lastUpdate, t)
  lastUpdate = t
  return {'count': twoSF(history[0]), 'time': t, 'history': map(twoSF, history) }

@post('/count')
def incCount():
  global history 
  global lastUpdate 
  t = time.time()
  history = updatedHistory(history, lastUpdate, t)
  history[0] += 1
  lastUpdate = t
  return {'count': twoSF(history[0]), 'time': t, 'history': map(twoSF, history) }

if __name__ == '__main__':
  run(server='gevent', host='localhost', port=8080, debug=True)
