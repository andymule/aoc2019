import math
import sys
import pprint
import collections

filepath = "day12.txt"
pos = []
vel = []

alldata = open(filepath).read()
alldata = alldata.split("\n")
planetcount = 0 #len(alldata)
for a in alldata:
    lilwords = a.split(",")
    x = int(lilwords[0][3:])
    y = int(lilwords[1][3:])
    z = int(lilwords[2][3:-1])
    pos.append([x,y,z])
    vel.append([0,0,0])
    planetcount += 1
# print(pos)
# print(vel)

set

steps = 0
while steps < 1000:
    for a in range(0,len(vel)): #vel
        for b in range(0,len(vel)):
            if a == b:
                continue
            for n in range(0,len(pos[a])):
                if pos[a][n] < pos[b][n]:
                    vel[a][n] += 1
                if pos[a][n] > pos[b][n]:
                    vel[a][n] -= 1
    for a in range(0,len(vel)): #new pos
        pos[a] = list(map(lambda x,y: x+y, pos[a],vel[a]))
    steps += 1
    
print(pos)
print(vel)

def abssum(a):
    run = 0
    for b in a:
        run += abs(b)
    return run

totalenergy = 0
for a,b in zip(pos,vel):
    totalenergy += abssum(a) * abssum(b)
print(totalenergy)

