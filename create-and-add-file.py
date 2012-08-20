## Symple script for bulk creating and adding files to a git repo
import os

for n in range(5, 20):
  f = open('BLAHfile-' + str(n) + '.txt', 'w')
  f.write('some test file content')
  f.close()
  os.system('git add BLAHfile-' + str(n) + '.txt')
  os.system('git commit -m "BLAH-' + str(n) + ': added test file number '+str(n)+'"')

