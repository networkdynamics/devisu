"""
  Filters that can be used with TweetSource.
"""
import re
from utils import get_date_from_timestr, get_date
from datetime import datetime

class Filter(object):
  def is_valid(self, tweet_object):
    pass
  
  def get_label(self):
    return self.label
    
  # Returns a dictionary of the filter's match for one tweet
  def get_filter_match(self, tweet_object):
    pass

class DateFilter(Filter):
  
  # Supports timestamp string (from Twitter) and datetime object
  def __init__(self, start, stop=None, label=None):
    # Set the date range
    self.start = self.ensure_datetime(start)
    self.stop = self.ensure_datetime(stop) if stop is not None else None
    # Set the label
    if label:
      self.label = label
    else:
      self.label = str(self.start) + "-" + str(self.stop)
  
  def is_valid(self, tweet_object):
    return self.get_filter_match(tweet_object)['in_range'] is not 0
      
  def ensure_datetime(self, arg):
    if isinstance(arg, str):
      return get_date(arg)
    elif not isinstance(arg, datetime):
      raise TypeError("Argument to DateFilter should be a timestamp string or a datetime object")  
    return arg
  
  def get_filter_match(self, tweet_object):
    match = {'before_start': 0, 'in_range': 0, 'after_stop': 0}
    tweet_date = get_date_from_timestr(tweet_object['created_at'])
    if self.stop and tweet_date > self.stop:
      match['after_stop'] = 1
    elif tweet_date < self.start:
      match['before_start'] = 1
    else:
      match['in_range'] = 1
    return match
  
class ContainsTextFilter(Filter):
  def __init__(self, text_list, case_sensitive=True, label=None):
    # Set the text list
    if isinstance(text_list, str):
      text_list = [text_list]
    self.contains = text_list
    self.case_sensitive = case_sensitive
    # Set the label
    if label:
      self.label = label
    else:
      # TODO(madmath): Support pattern labels
      self.label = ",".join(self.get_pattern_label(p) for p in text_list)
  
  def get_pattern_label(self, pattern):
    if isinstance(pattern, str):
      return pattern
    else:
      return "-".join(pattern)
    
  def is_valid(self, tweet_object):
    return sum(self.get_filter_match(tweet_object).values()) != 0
  
  def get_filter_match(self, tweet_object):
    match = {}
    for i, pattern in enumerate(self.contains): # Tweet can contain either of the n patterns
      if isinstance(pattern, list):
        pattern_label = self.get_pattern_label(pattern)
        for pat in pattern:
          if self.match(pat, tweet_object['text']):
            match[pattern_label] = 1 # Don't have detailed stats for all pattern
            break
        if pattern_label not in match:
          match[pattern_label] = 0
      else:
        if self.match(pattern, tweet_object['text']):
          match[pattern] = 1
        else:
          match[pattern] = 0
    return match
  
  def match(self, pattern, text):
    pattern = pattern if self.case_sensitive else pattern.lower()
    text = text if self.case_sensitive else text.lower()
    return pattern in text

class RegexTextFilter(ContainsTextFilter):
  def __init__(self, re_list, label=None):
    super(RegexTextFilter, self).__init__(re_list, label=label)
  
  def match(self, regex, text):
    return re.search(regex, text) is not None
