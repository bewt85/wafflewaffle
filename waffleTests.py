#!/usr/bin/env python

import unittest
import time
from collections import deque
import waffle
from copy import deepcopy

waffle.DAMP_FACTOR = 0.5 
waffle.HISTORY_LENGTH = 5*60

class UpdateHistory(unittest.TestCase):
  

  def setUp(self):
    self.lastUpdate = 0.0
    self.history = deque([ 0.0 for i in range(waffle.HISTORY_LENGTH) ])

  def assertListsAlmostEqual(self, l1, l2, places=7):
    self.assertEqual(len(l1), len(l2))
    for (e1, e2) in zip(l1, l2):
      self.assertAlmostEqual(e1, e2, places)

  def test_no_count(self):
    initial_history = deepcopy(self.history)
    now = self.lastUpdate + 1.0
    history = waffle.updatedHistory(self.history, self.lastUpdate, now)
    self.assertListsAlmostEqual(initial_history, self.history, places=4)

  def test_one_count_half_second(self):
    self.history[0] = 1.0
    now = self.lastUpdate + 0.5
    expected = [ 0 for i in self.history ]
    expected[0] = waffle.DAMP_FACTOR ** 0.5
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, now)
    self.assertListsAlmostEqual(list(self.history), expected, places=4)

  def test_one_count_one_point_five_seconds(self):
    self.history[0] = 1.0
    now = self.lastUpdate + 1.5
    expected = [ 0 for i in self.history ]
    expected[:2] = [ waffle.DAMP_FACTOR ** 1.5, waffle.DAMP_FACTOR ** 1 ]
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, now)
    self.assertListsAlmostEqual(list(self.history), expected, places=4)
    
  def test_one_count_two_checks(self):
    self.history[0] = 1.0
    firstCheck = self.lastUpdate + 0.5
    secondCheck = self.lastUpdate + 1.5
    expected = [ 0 for i in self.history ]
    expected[0] = waffle.DAMP_FACTOR ** 0.5
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, firstCheck)
    self.assertListsAlmostEqual(list(self.history), expected, places=4)
    self.lastUpdate = firstCheck
    
    expected[:2] = [ waffle.DAMP_FACTOR ** 1.5, waffle.DAMP_FACTOR ** 1 ]
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, secondCheck)
    self.assertListsAlmostEqual(list(self.history), expected, places=4)
    
  def test_two_count_two_checks(self):
    self.history[0] = 1.0
    firstCheck = self.lastUpdate + 0.5
    secondCheck = self.lastUpdate + 1.5
    expected = [ 0 for i in self.history ]
    expected[0] = 1 + waffle.DAMP_FACTOR ** 0.5
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, firstCheck)
    self.history[0] += 1
    self.assertListsAlmostEqual(list(self.history), expected, places=4)
    self.lastUpdate = firstCheck
    
    expected[:2] = [ waffle.DAMP_FACTOR ** 1 + waffle.DAMP_FACTOR ** 1.5, waffle.DAMP_FACTOR ** 0.5 + waffle.DAMP_FACTOR ** 1 ]
    self.history = waffle.updatedHistory(self.history, self.lastUpdate, secondCheck)
    self.assertListsAlmostEqual(list(self.history), expected, places=4)
    

if __name__ == '__main__':
  unittest.main()
