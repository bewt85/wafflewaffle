#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file, request, response, template
import os, time, uuid
from collections import deque

SECRET_KEY = uuid.uuid4().hex

VOTE_LIFE = 5*60
DAMP_FACTOR = 0.001 ** ( 1.0 / VOTE_LIFE )

HISTORY_LENGTH = 10*60
history = deque([ 0.0 for i in range(HISTORY_LENGTH) ])
lastUpdate = time.time() 

RATE_LIMIT = 10

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
  response.set_cookie('last_POST', '0.0', secret=SECRET_KEY)
  return template('index')

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
  lastUpdate = t
  message = None
  if not request.get_cookie('last_POST', secret=SECRET_KEY):
    message = "Error: Could not find last_POST cookie, try reloading the page"
    response.status = 403
  elif not (t - float(request.get_cookie('last_POST', secret=SECRET_KEY)) > RATE_LIMIT):
    message = "Warning: Please wait %s seconds between requests, ignoring" % RATE_LIMIT
    response.status = 429
  else:
    history[0] += 1
    response.set_cookie('last_POST', str(t), secret=SECRET_KEY)
    response.status = 201
    return {'count': twoSF(history[0]), 'time': t, 'history': map(twoSF, history) }
  return {'error_message': message, 'count': twoSF(history[0]), 'time': t, 'history': map(twoSF, history) }

if __name__ == '__main__':
  run(server='gevent', host='localhost', port=8080, debug=True)
