#!/usr/bin/python -u
# script to take input from stdin and print a timestamp next to it
# prints time of entry, time since start, time since last entry

import datetime, sys

starttime = datetime.datetime.now()
lasttime = datetime.datetime.now()
while True:
  line = sys.stdin.readline()
  if not line: break
  now = datetime.datetime.now()
  st = now.strftime('%H:%M:%S.%f')[:-3]
  diff = now - lasttime
  diffstart = now - starttime
  print st, " ", str(diffstart)[:-3], " ", str(diff)[:-3], " ", line.rstrip('\n')
  lasttime = now

