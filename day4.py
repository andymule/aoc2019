import math
import sys
import pprint

start=372304
end=847060
yes = []

for i in range(372304, 847060+1):
# for i in range(111122, 111122+1):
    l = list(str(i))
    a = int(l[0]) <= int(l[1]) <=int(l[2]) <=int(l[3]) <=int(l[4])<=int(l[5])
    streak_count = []
    counter = 0
    n = int(l[0])
    c = True
    for m in [int(x) for x in str(i)][1:] :
        if n == m:
            counter += 1
        else:
            streak_count.append(counter+1)
            counter = 0
        n = m
    if n == m:
        streak_count.append(counter+1)
    else:
        streak_count.append(counter)
    if 2 in streak_count:
        c = True
    else:
        c = False

    b = (l[0]==l[1] or l[1]==l[2] or l[2]==l[3] or l[3]==l[4]or l[4]==l[5]) and c
    if a and b:
        yes.append(i)

print(len(yes))

    