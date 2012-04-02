import unittest

from devisu.filters import *
from devisu.sources import *
from devisu.tests.sources import JSONTweetSourceTestCase

class FilterTestCase(unittest.TestCase):
  def setUp(self):
    self.ts = JSONTweetSourceTestCase.createTestTweetSource()
  
class ContainsTextFilterTestCase(FilterTestCase):
  
  def test_get_label(self):
    label = "MyLabel"
    tf = ContainsTextFilter(label)
    assert tf.get_label() == "MyLabel"
  
  def test_one_string(self):
    query = 'Apple'
    tf = ContainsTextFilter(query)
    self.ts.add_filter(tf)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      assert query in tweet['text']
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
    
  def test_two_strings_or(self):
     # Can contain either Apple or Display or both, case sensitive
    query = ['Apple', '#ipad']
    tf = ContainsTextFilter(query)
    self.ts.add_filter(tf)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      orcondition = False
      for q in query:
        orcondition |= q in tweet['text']
      assert orcondition
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
  
  def test_two_strings_and(self):
    # Tweet HAS TO contain Apple and Display, case sensitive
    query = ['Apple', 'iPad']
    
    tf1 = ContainsTextFilter(query[0])
    tf2 = ContainsTextFilter(query[1])
    self.ts.add_filters(tf1, tf2)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      andcondition = True
      for q in query:
        andcondition &= q in tweet['text']
      assert andcondition
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
  
  # Filter is case sensitive by default
  def test_case_insensitivity(self):
    query = "iPad" # Query should contain at least one upper case letter for this case to work.
    tf = ContainsTextFilter(query, case_sensitive=False)
    self.ts.add_filter(tf)
    
    i = 0
    case_insensitive = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      if query in tweet['text']:
        continue
      if query.lower() in tweet['text']:
        case_insensitive += 1
    assert case_insensitive > 0
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
    
  def test_get_filter_match(self):
    # Can contain either Apple or Display or both, case sensitive
    query = ['Apple', '#ipad']
    tf = ContainsTextFilter(query)
    self.ts.add_filter(tf)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      orcondition = False
      expected = dict.fromkeys(query, 0)
      for q in query:
        if q in tweet['text']:
          expected[q] = 1
      filter_match = tf.get_filter_match(tweet)
      for ek in query:
        assert ek in filter_match
      for k in filter_match:
        assert expected[k] == filter_match[k]
        del expected[k]
      assert len(expected) == 0
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")

class RegexTextFilterTestCase(FilterTestCase):
  
  def test_one_regex_start(self):
    query = '^RT' # starts with RT
    tf = RegexTextFilter(query)
    self.ts.add_filter(tf)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      assert tweet['text'].startswith('RT')
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
    
  # TODO(madmath): Add more tests here.
    
class DateFilterTestCase(FilterTestCase):
  
  def test_date_range_with_stop(self):
    start = get_date_from_timestr("Wed Feb 15 05:20:11 +0000 2012")
    stop = get_date_from_timestr("Wed Feb 15 05:30:11 +0000 2012")
    
    df = DateFilter(start, stop=stop)
    self.ts.add_filter(df)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      assert re.search('^Wed Feb 15 05:(2[0-9]|30)', tweet['created_at']) is not None
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")

  def test_date_range_no_stop(self):
    start = get_date_from_timestr("Wed Feb 15 05:20:00 +0000 2012")

    df = DateFilter(start)
    self.ts.add_filter(df)

    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      assert re.search('^Wed Feb 15 05:(2[0-9]|[3-5][0-9])', tweet['created_at']) is not None
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
  
  def test_get_filter_match(self):
    start = get_date_from_timestr("Wed Feb 15 05:20:11 +0000 2012")
    stop = get_date_from_timestr("Wed Feb 15 05:30:11 +0000 2012")
    expected_keys = ['before_start', 'in_range', 'after_stop']
    # We know that stop > start here
    df = DateFilter(start, stop=stop)
    self.ts.add_filter(df)
    
    i = 0
    for tweet in self.ts.iter_tweets():
      i += 1
      date = get_date_from_timestr(tweet['created_at'])
      expected = dict.fromkeys(expected_keys, 0)
      if date < start:
        expected['before_start'] = 1
      elif date > stop:
        expected['after_stop'] = 1
      else:
        expected['in_range'] = 1
      # Assert that filter_match and expected are the same
      filter_match = df.get_filter_match(tweet)
      for ek in expected_keys:
        assert ek in filter_match
      for k in filter_match:
        assert expected[k] == filter_match[k]
        del expected[k]
      assert len(expected) == 0
    self.assertNotEqual(i, 0, "Iterated through no elements (Invalid test)")
  
  