#!/usr/bin/python

import subprocess

lines = subprocess.check_output(["kubectl", "get", "pods", "--all-namespaces"]).split("\n")

l = 0
for line in lines:
    print(str(l) + ": " + line)
    l = l + 1

ln = int(raw_input("Select pod: "))

pod = list(filter(lambda x: x != '', lines[ln].split(" ")))

while True:
    c = raw_input("Enter command: ")
    if c == "logs":
        subprocess.call(["kubectl", "logs", pod[1], "-n", pod[0]])
    if c == "shell":
        subprocess.call(["kubectl", "exec", "-it", pod[1], "-n", pod[0], "--", "/bin/bash"])
