#!/usr/bin/python -u
import datetime, sys

lasttime = datetime.datetime.now()
while True:
  line = sys.stdin.readline()
  if not line: break
  now = datetime.datetime.now()
  st = now.strftime('%H:%M:%S.%f')[:-3]
  diff = now - lasttime
  print st, " ", str(diff), " ", line.rstrip('\n')
  lasttime = now

