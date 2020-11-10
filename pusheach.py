#!/usr/bin/env python3

# Push each commit from a given hash up to the head of this branch
# one by one, force-pushing the first one.
#
# Useful if you have a CI system that runs builds on the HEAD,
# and you want to build each commit one by one
import sys
import subprocess
import os
import time

p = subprocess.run(["git", "branch", "--show-current"], capture_output=True)
current_branch = p.stdout.decode("utf-8").strip()
print('current: "' + current_branch+"'")
p = subprocess.run(["git", "log", sys.argv[1] + ".." +current_branch, '--pretty=format:%h'], capture_output=True)

hashes = p.stdout.decode("utf-8").split('\n')
hashes.reverse()

cmd = ["git", "push", "-f", "origin", sys.argv[1] + ":" + current_branch]
subprocess.run(cmd)

for h in hashes:
    print("H:'" +h+"'")
    cmd = ["git", "push", "origin", h + ":" + current_branch]
    subprocess.run(cmd)
    time.sleep(10)

    
