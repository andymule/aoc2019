import math
import sys
import pprint
from collections import defaultdict
import numpy as np
from sortedcontainers import SortedList
from sortedcontainers import SortedDict
import copy

filepath = "day10.txt"
stars = []
realstars = []


class Star:
    def __init__(self, _y, _x):
        self.y = _y
        self.x = _x
        self.distanceToSees = {}  # hash of distace to stars can be seen
        self.canSeeAtAngle = {}
        self.tempdistance = (
            0  # temp variable used for storing while iterating, not always meaningful
        )

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

def signed_angle(vector1, vector2):
    """ Returns the angle in radians between given vectors"""
    v1_u = unit_vector(vector1)
    v2_u = unit_vector(vector2)
    minor = np.linalg.det(
        np.stack((v1_u[-2:], v2_u[-2:]))
    )
    if minor == 0:
        if np.sign(vector1)[1] == np.sign(vector2)[1]:
            return 0 #haha workaround
        else:
            return 3.14159
        raise NotImplementedError('Too odd vectors =(')
    return np.sign(minor) * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


# [17, 23]
alldata = open(filepath).read()
lines = alldata.split()
width = len(lines[0])
height = len(lines)

l = lines[23]
l = l[:17] + "0" + l[18:]
lines[23] = l

for y in range(0, height):
    stars.append([])
    for x in range(0, width):
        c = lines[y][x]
        if c == ".":
            stars[y].append(None)
        if c == "#" or c == "0":
            stars[y].append(Star(y, x))
            realstars.append(stars[y][x])

for row in lines:
    print(*row)
print()
# matprint(lines)

starsrekt = 0
while True:
    angles = defaultdict(lambda: SortedList(key=lambda x: x.tempdistance))
    for star in realstars:
        # print(star.vec())
        if star.vec() != [17, 23]:  # part 2 ONLY DO SELF
            continue
        for other in realstars:
            if other.vec() == star.vec():  # skip self
                continue
            a = star.vec()
            b = other.vec()
            ab = np.subtract(b, a)
            angle = ab / np.linalg.norm(ab)
            angle = np.around(angle, decimals=5)
            other.tempdistance = np.linalg.norm(ab)
            angles[tuple(angle)].add(other)
        for angle in angles.keys():
            newstar = angles[angle][0]
            star.addstar(newstar, angle, newstar.tempdistance)
        angles.clear()

    for star in realstars:
        # print(star.vec())
        if star.vec() != [17, 23]:  # part 2 ONLY DO SELF
            continue
        sd = SortedDict()
        for angle in star.canSeeAtAngle.keys():
            angleFromUp = np.around(signed_angle(angle, [0, -1]), decimals=8)
            if angleFromUp < 0:
                angleFromUp =  np.around(angleFromUp + (3.14159*2), decimals=8)
            angleFromUp = np.around((3.14159*2) - angleFromUp, decimals=4)
            sd[angleFromUp] = star.canSeeAtAngle[angle]
            # od
        sd[0] = sd.pop(6.2832)
        try:
            while True:
                nextstar = sd.popitem(0)[1]
                starsrekt += 1
                if starsrekt == 200:
                    for row in lines:
                        print(*row)
                    print()
                    jk = 69
                v = nextstar.vec()
                # print(v)
                l = lines[v[1]]
                l = l[: v[0]] + "X" + l[v[0] + 1 :]
                lines[v[1]] = l
                # for row in lines:
                #     print(*row)
                # print()
                if starsrekt == 200:
                    sys.exit(0)
        except:
            sys.exit(0)
            pass
        #224 too high ?

    for row in lines:
        print(*row)
        print()

    # rebuild
    realstars = []
    stars = []
    for y in range(0, height):
        stars.append([])
        for x in range(0, width):
            c = lines[y][x]
            if c == ".":
                stars[y].append(None)
            if c == "#" or c == "0":
                stars[y].append(Star(y, x))
                realstars.append(stars[y][x])

maxcount = 0
maxpos = [0, 0]
for star in realstars:
    if len(star.canSeeAtAngle) > maxcount:
        maxcount = len(star.canSeeAtAngle)
        maxpos = star.vec()
print(maxcount)
print(maxpos)
