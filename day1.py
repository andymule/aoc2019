import math
filepath = 'day1.txt'
counter = 0
with open(filepath) as fp:
 for cnt, line in enumerate(fp):
  start = math.floor(int(line)/3)-2
  counter += start
  while (start > 0):
   start = math.floor(int(start)/3)-2
   if (start > 0):
    counter += start
print(counter)