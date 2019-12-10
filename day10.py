import math
import sys
import pprint
from collections import defaultdict
import numpy as np
from sortedcontainers import SortedList
import copy

filepath = "day10.txt"
stars = []
realstars = []

class Star:
    def __init__(self, _y, _x):
        self.y = _y
        self.x = _x
        self.distanceToSees = {} # hash of distace to stars can be seen
        self.canSeeAtAngle = {}
        self.tempdistance = 0 # temp variable used for storing while iterating, not always meaningful

    def vec(self):
        return [self.x, self.y]

    def addstar(self, s, ang, dist):
        self.canSeeAtAngle[ang] = s
        self.distanceToSees[s] = dist

def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# [17, 23]
alldata = open(filepath).read()
lines = alldata.split()
width = len(lines[0])
height = len(lines)

for y in range(0, height):
    stars.append([])
    for x in range(0, width):
        c = lines[y][x]
        if c == ".":
            stars[y].append(None)
        if c == "#":
            stars[y].append(Star(y, x))
            realstars.append(stars[y][x])

angles = defaultdict(lambda: SortedList(key=lambda x: x.tempdistance))
for star in realstars:
    print(star.vec())
    for other in realstars:
        if other.vec() == star.vec():  # skip self
            continue
        a = star.vec()
        b = other.vec()
        ab = np.subtract(b, a)
        angle = ab/np.linalg.norm(ab)
        angle = np.around(angle, decimals=5)
        other.tempdistance = np.linalg.norm(ab)
        angles[tuple(angle)].add(other)
    for angle in angles.keys():
        newstar = angles[angle][0]
        star.addstar(newstar, angle, newstar.tempdistance)
    angles.clear()

maxcount = 0
maxpos = [0, 0]
for star in realstars:
    if len(star.canSeeAtAngle) > maxcount:
        maxcount = len(star.canSeeAtAngle)
        maxpos = star.vec()
print(maxcount)
print(maxpos)
