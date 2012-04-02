import json
from filters import *
"""
Base class for the TweetSource that should be subclassed
"""
class TweetSource(object):
  def __init__(self):
    self.filters = None

  def get_tweets(self):
    pass
    
  # TODO(madmath): Should the argument be a list?
  def add_filters(self, *filters):
    if not self.filters:
      self.filters = []
    for fil in filters:
      self.add_filter(fil)

  def add_filter(self, fil):
    if not self.filters:
      self.filters = []
    self.filters.append(fil)
  
  def get_stats(self, include_tweets=False):
    stats = {}
    for tweet in self.get_tweets():
      ANDcondition = True
      if self.filters:
        for fil in self.filters:
          ANDcondition &= fil.is_valid(tweet)
      # ANDcondition controls if this tweet is valid.
      if not ANDcondition:
        continue
      # Once we know the tweet is valid, do the statistics part
      elif self.filters:
        for fil in self.filters:
          if fil.is_valid(tweet):
            label = fil.get_label()
            breakdown = fil.get_filter_match(tweet)
            filter_stats = stats.get(label, {})
            for k, v in breakdown.items():
              if include_tweets:
                if v > 0:
                  rlist = filter_stats.get(k, [])
                  rlist.append(tweet)
                  filter_stats[k] = rlist
              else:
                filter_stats[k] = filter_stats.get(k, 0) + v
            stats[label] = filter_stats
      if include_tweets:
        rlist = stats.get('all', [])
        rlist.append(tweet)
        stats['all'] = rlist
      else:
        stats['all'] = stats.get('all', 0) + 1
    return stats
  
  def iter_tweets(self):
    for tweet in self.get_tweets():
      ANDcondition = True
      if self.filters:
        for fil in self.filters:
          ANDcondition &= fil.is_valid(tweet)
      if ANDcondition:
        yield tweet

"""
  JSON tweet source.
"""
class JSONTweetSource(TweetSource):
  def __init__(self, filename):
    super(JSONTweetSource, self).__init__()
    self.source = filename
  
  def get_tweets(self):
    for line in open(self.source):
      try:
        tweet = json.loads(line)
        yield tweet
      except ValueError:
        print "Could not load tweet"
