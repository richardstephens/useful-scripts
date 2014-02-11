#!/usr/bin/python -u
import datetime, sys

while True:
  line = sys.stdin.readline()
  if not line: break
  now = datetime.datetime.now()
  st = now.strftime('%H:%m:%S.%f')[:-3]
  print st, " ", line.rstrip('\n')

