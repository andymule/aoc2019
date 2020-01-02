import math
import sys
import pprint
from collections import defaultdict
from typing import Dict

import networkx as nx
from networkx import Graph


def buildgraph(symbol, check, parent, needtovisit):
    y = check[0]
    x = check[1]
    c = MAP[y][x]
    graphs[symbol].add_node(check)
    if parent:
        graphs[symbol].add_edge(parent, check)
    if c.isalpha():
        if c.islower():
            keys[c] = (y, x)
        else:
            doors[c] = (y, x)
    up = (y - 1, x)
    if up in needtovisit:
        needtovisit.remove(up)
        buildgraph(up, check)
    down = (y + 1, x)
    if down in needtovisit:
        needtovisit.remove(down)
        buildgraph(down, check)
    left = (y, x - 1)
    if left in needtovisit:
        needtovisit.remove(left)
        buildgraph(left, check)
    right = (y, x + 1)
    if right in needtovisit:
        needtovisit.remove(right)
        buildgraph(right, check)


# TODO make paths to doors include picking up keys... make paths to doors include all prereqs then just find paths dummy
def findnextmove():
    global totalsteps, POS
    nextmove = (-69, -69)
    for key in keys.values():
        shortest = nx.shortest_path(G, key, POS)
        for door in doors.values():
            if door in shortest:
                continue  # door in way
        if len(shortest) < minpath:
            minpath = len(shortest)
            nextmove = key
    totalsteps += minpath
    POS = nextmove


filepath = "day18.txt"
MAP = []
alldata = open(filepath).readlines()
for l in alldata:
    MAP.append(l.strip())
H = len(MAP)
W = len(MAP[0])

keys = {}  # defaultdict(lambda: None)
doors = {}  # defaultdict(lambda: None)
graphs: Dict[str, Graph] = {}
graphs["@"] = nx.Graph()

akeys = set()
adoors = set()
for y in range(H):
    for x in range(W):
        c = MAP[y][x]
        if c != '#' and c != '@':
            if c.islower():
                akeys.add(c)
            else:
                adoors.add(c)


def findpathsfor(symbol):
    needtovisit = set()
    start = (0, 0)
    for y in range(H):
        for x in range(W):
            if MAP[y][x] == symbol:
                start = (y, x)
            elif MAP[y][x] != '#':
                needtovisit.add((y, x,))
    buildgraph("@", tuple(start), None)
    return needtovisit, start



# POS = start

minpath = 99999999
# nextmove = start
totalsteps = 0
