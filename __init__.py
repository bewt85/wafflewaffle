#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

count = 0

from bottle import route, run

@route('/')
def inc():
  global count
  count += 1
  return "Count %s" % count

run(server='gevent', host='localhost', port=8080, debug=False)
