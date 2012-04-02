import unittest
import os.path as path

from devisu.filters import *
from devisu.sources import *

class JSONTweetSourceTestCase(unittest.TestCase):
  
  def test_normal_source(self):
    ts = JSONTweetSource(path.join(path.dirname(__file__),'test_ipad.txt'))
    for tweet in ts.iter_tweets():
      assert 'text' in tweet
  
  def test_get_stats_no_filter(self):
    ts = self.createTestTweetSource()
    # Assert that it returns the full number of tweets (36 in our dataset)
    assert ts.get_stats()['all'] == 36
  
  def test_get_stats_one_filter(self):
    ts = self.createTestTweetSource()
    # Create one filter and add it to the source
    tf = ContainsTextFilter("iPad")
    ts.add_filter(tf)
    stats = ts.get_stats()
    assert stats[tf.get_label()]['iPad'] == 23

  def test_get_stats_one_filter_two_strings_include_tweets(self):  
    ts = self.createTestTweetSource()
    # Create one filter and add it to the source
    tf1 = ContainsTextFilter(["iPad", "Apple"])
    ts.add_filter(tf1)
    stats = ts.get_stats(include_tweets=True)
    # TODO(madmath): Beef up that test to look for specific tweet contents?
    # This filters for either iPad or Apple, and we assert the count for each in our dataset
    assert len(stats[tf1.get_label()]['iPad']) == 23
    assert len(stats[tf1.get_label()]['Apple']) == 3
    
  def test_get_stats_one_filter_two_strings(self):
    ts = self.createTestTweetSource()
    # Create one filter and add it to the source
    tf1 = ContainsTextFilter(["iPad", "Apple"])
    ts.add_filter(tf1)
    stats = ts.get_stats()
    # This filters for either iPad or Apple, and we assert the count for each in our dataset
    assert stats[tf1.get_label()]['iPad'] == 23
    assert stats[tf1.get_label()]['Apple'] == 3
  
  def test_get_stats_one_filter_two_strings_with_possibilities(self):
    ts = self.createTestTweetSource()
    # Create one filter and add it to the source
    tf1 = ContainsTextFilter(["iPad", ["iPad", 'ipad']])
    ts.add_filter(tf1)
    stats = ts.get_stats()
    filter_stats = stats[tf1.get_label()]
    # This filters for either iPad or Apple, and we assert the count for each in our dataset
    # TODO(madmath): Better test set?
    assert filter_stats[tf1.get_pattern_label('iPad')] == 23
    assert filter_stats[tf1.get_pattern_label(["iPad", "ipad"])] == 34
    
  @staticmethod
  def createTestTweetSource():
    return JSONTweetSource(path.join(path.dirname(__file__),'test_ipad.txt'))