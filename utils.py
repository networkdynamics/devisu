"""
  Utility functions for parsing tweet objects
"""
import time
from datetime import datetime
from dateutil.tz import *

# Helper function to transform the ['created_at'] field in a tweet json object, to a timestamp str.
def get_timestamp(timestr,tz=tzlocal()):
  a = datetime.strptime(timestr,'%a %b %d %H:%M:%S +0000 %Y')
  a = a.replace(tzinfo=tzoffset(None, 0))
  a = a.astimezone(tz=tz)
  return time.mktime(a.timetuple())

def get_date(timestamp,tz=tzlocal()):
  a = datetime.fromtimestamp(float(timestamp), tz=tzoffset(None, 0))
  a = a.astimezone(tz=tz)
  return a

def get_date_from_timestr(timestr, tz=tzlocal()):
  return get_date(get_timestamp(timestr, tz=tz),tz=tz)