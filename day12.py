import math
import sys
import pprint
import collections
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

filepath = "day12.txt"
pos = []
vel = []

def abssum(a):
    run = 0
    for b in a:
        run += abs(b)
    return run

def statetostring():
    global pos, vel
    s = ""
    for i in range(0,len(pos)):
        s2 = "".join([str(e) for e in pos[i]])
        s3 = "".join([str(e) for e in vel[i]])
        s = s + s2 + s3
    return s

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

history = set()
startstate = statetostring()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
movement = [[],[],[],[]]
steps = 0
while False: #part 1
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
        movement[a].append(pos[a])
    steps += 1
    newstate = statetostring()
    if newstate == startstate:
        print(steps)
        # sys.exit(0)
        # break
        jk = 69

    # newstate = statetostring()
    # if newstate in history:
        # jk = 69
    
print(pos)
print(vel)



totalenergy = 0
for a,b in zip(pos,vel):
    totalenergy += abssum(a) * abssum(b)
print(totalenergy)



def axisstate(index): #only 0-2 are valid
    global pos, vel
    s = ""
    for i in range(0,len(pos)):
        s2 = str(pos[i][index])
        s3 = str(vel[i][index])
        s = s + s2 + s3
    return s

startaxisstates = [0,0,0] #independent axes states
axis = 0
axissteps = [0,0,0]
history.add(statetostring())

startaxisstates[0] = axisstate(0)
startaxisstates[1] = axisstate(1)
startaxisstates[2] = axisstate(2)

while True: #part 2
    for a in range(0,len(vel)): #vel
        for b in range(0,len(vel)):
            if a == b:
                continue
            if pos[a][axis] < pos[b][axis]:
                vel[a][axis] += 1
            if pos[a][axis] > pos[b][axis]:
                vel[a][axis] -= 1
    for a in range(0,len(vel)): #new pos
        pos[a][axis] += vel[a][axis]
    axissteps[axis] += 1
    newstate = axisstate(axis)
    if newstate == startaxisstates[axis]:
        if axissteps[0] == axissteps[1] == axissteps[2]: #WOW ALL AT SAME SPOT
            newtotalstate = statetostring()
            if newtotalstate in history:
                jk = 69
            else:
                history.add(newtotalstate)
        if axissteps[2] == 0:
            axis = 2
        elif axissteps[1] == 0:
            axis = 1
        else:
            print()
            print(axissteps)
            sys.exit(0)

# do least common multiple on step per axis to get reset state