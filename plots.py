import numpy as np
import matplotlib.pyplot as plt

from utils import get_timestamp, get_date

class TweetPlot(object):
  
  def __init__(self, source):
    self.source = source
    self.width = 0.5
  
  def set_width(self, width):
    self.width = float(width)
  
  def show_plot(self):
    plt.show()

  def save_plot(self, filename):
    plt.savefig(filename)
  
  
class TimelineTweetPlot(TweetPlot):
  
  def __init__(self, tweet_source, steps=20):
    super(TimelineTweetPlot, self).__init__(tweet_source)
    self.steps = steps
  
  def get_time_bins(self, timestamps):
    starttime = None
    stoptime = None
    min_ts = min(timestamps)
    max_ts = max(timestamps)
    step = (max_ts-min_ts)/self.steps
    bins = [step*(i+1)+min_ts for i in range(self.steps)]
    return bins
    
  def get_bin(self, ts, bins):
    for i,b in enumerate(bins):
      if ts <= b:
        return i
  
  def generate_plot(self):
    timestamps = [get_timestamp(t['created_at']) for t in self.source.iter_tweets()]
    bins = self.get_time_bins(timestamps)
    tally = [0] * self.steps
    for tstamp in timestamps:
      j = self.get_bin(tstamp, bins)
      tally[j] = tally[j] + 1

    plt.plot(bins, tally)
    dates = ["%s:%s" %(get_date(a).hour, get_date(a).minute) for i,a in enumerate(bins) if i%3 == 0]
    plt.xticks([b for i, b in enumerate(bins) if i%3 ==0], dates, rotation=0)

class FilteredTimelineTweetPlot(TimelineTweetPlot):

  def __init__(self, tweet_source, steps=20, colors=['#cc3366', '#b5cc94', '#996699', '#ffcc33', '#7bcbbe']):
    super(FilteredTimelineTweetPlot, self).__init__(tweet_source)
    self.steps = steps
    self.colors = colors

  def generate_plot(self, filter_label):
    timestamps = [get_timestamp(t['created_at']) for t in self.source.iter_tweets()]
    bins = self.get_time_bins(timestamps)
    feature = self.source.get_stats(include_tweets=True)
    filter_stats = feature.get(filter_label, None)
    if not filter_stats:
      raise Exception("Could not get statistics for filter %s. Wrong filter label?" % filter_label)

    for k, feat in enumerate(filter_stats):    
      # Gather the different timestamps
      ttweets = filter_stats[feat]
      tally = [0] * self.steps

      timestamps = [float(get_timestamp(t['created_at'])) for t in ttweets]
      # Do some sort of histograms with it
      for ts in timestamps:
        j = self.get_bin(ts, bins)#index = int(ts/step)
        tally[j] = tally[j] + 1
      #tally, bins = np.histogram(timestamps, bins=steps)

      #bins = .5*(bins[1:]+bins[:-1])+starttime
      plt.plot(bins, tally, color=self.colors[k])
      dates = ["%s:%s" %(get_date(a).hour, get_date(a).minute) for j,a in enumerate(bins) if j%(self.steps/20) == 0]
      for i, date in enumerate(dates):
        split = date.split(':')
        if len(split[1]) == 1:
          dates[i] = split[0] + ':0' + split[1]
      plt.ylabel('Number of Tweets')
      plt.xticks([b for j,b in enumerate(bins) if j%(self.steps/20)==0], dates, rotation=90)

    plt.legend(filter_stats.keys(),loc=1)
    
class BarChartTweetPlot(TweetPlot):
  
  def __init__(self, tweet_source, percent=False):
    super(BarChartTweetPlot, self).__init__(tweet_source)
    self.percent = percent
  
  def generate_plot(self, filter_label):
    stats = self.source.get_stats()
    filter_stats = stats.get(filter_label, None)
    if not filter_stats:
      raise Exception("Cannot get statistics for specified filter")
    tally = dict([(k,v) for k,v in filter_stats.items()])
    total = sum(tally.values())
    if self.percent:
      plt.ylabel('Percentage')
      for f in tally:
        tally[f] = tally[f]/float(total)*100.
    else:
      plt.ylabel("Number of occurrences")
    svalues = sorted(tally.items(), key= lambda x: x[1], reverse=True)
    bar_locations = [x*self.width for x in range(len(tally))]
    ticks_locations = [x+self.width/2. for x in bar_locations]
    plt.bar(bar_locations, [s[1] for s in svalues], width=self.width)
    plt.xticks(ticks_locations, [s[0] for s in svalues])


  