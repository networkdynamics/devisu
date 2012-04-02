import inspect, traceback
import os.path as path

from devisu.sources import JSONTweetSource
from devisu.filters import *
from devisu.plots import *

class Examples(object):
  
  def show_timeline(self):
    ts = JSONTweetSource(path.join(path.dirname(__file__)+"/../tests/",'test_ipad.txt'))
    pl = TimelineTweetPlot(ts)
    pl.generate_plot()
    pl.show_plot()
    
  def show_pie_chart(self):
    pass
    
  def show_bar_chart(self):
    ts = JSONTweetSource(path.join(path.dirname(__file__)+"/../tests/",'test_ipad.txt'))
    tf = ContainsTextFilter(["Apple", "iPad", "3"])
    ts.add_filter(tf)
    pl = BarChartTweetPlot(ts)
    pl.generate_plot(tf.get_label())
    pl.show_plot()
    
  def show_filtered_timeline(self):
    ts = JSONTweetSource(path.join(path.dirname(__file__)+"/../tests/",'test_ipad.txt'))
    tf = ContainsTextFilter(["Apple", "iPad", "3"])
    ts.add_filter(tf)
    pl = FilteredTimelineTweetPlot(ts)
    pl.generate_plot(tf.get_label())
    pl.show_plot()

if __name__ == '__main__':
  ex = Examples()
  members = inspect.getmembers(ex)
  functions = []
  for i, member in enumerate(members):
    if not member[0].startswith('__'):
      functions.append(member)
  
  while True:
    print "\n".join("%d. %s" % (i+1, fn[0]) for i,fn in enumerate(functions))
    choice = raw_input("Choose your example, -1 to quit: ")
    if int(choice) == -1:
      break
    else:
      try:
        fname = functions[int(choice)-1][0]
        print "Executing function:", fname
        functions[int(choice)-1][1]()
      except:
        traceback.print_exc()
        break
