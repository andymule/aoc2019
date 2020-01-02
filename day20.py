import networkx as nx
import os, sys, collections

filepath = "day20.txt"
MAP = []
alldata = open(filepath).readlines()
for line in alldata:
    MAP.append(line[:-1])
H = len(MAP)
W = len(MAP[0])

graph = nx.Graph()
# .add_edge(parent, check)
# .add_node(check)
start = (2, 9)
end = (16, 13)
portals = {}
for y in range(H):
    s = ""
    for x in range(W):
        if (y, x) == start:
            s += '☻'
        elif (y, x) == end:
            s += '♥'
        else:
            s += MAP[y][x]
    print(s)


def tupletomap(t):
    return MAP[t[0]][t[1]]


def buildgraph(check, parent, needtovisitlocal):
    y = check[0]
    x = check[1]
    if MAP[y][x].isalpha():
        portals.add((y, x))
    graph.add_node(check)
    if parent:
        graph.add_edge(parent, check)
    up = (y - 1, x)
    c = MAP[y - 1][x]
    if up in needtovisitlocal:
        needtovisitlocal.remove(up)
        buildgraph(up, check)
    down = (y + 1, x)
    if down in needtovisitlocal:
        needtovisitlocal.remove(down)
        buildgraph(down, check)
    left = (y, x - 1)
    if left in needtovisitlocal:
        needtovisitlocal.remove(left)
        buildgraph(left, check)
    right = (y, x + 1)
    if right in needtovisitlocal:
        needtovisitlocal.remove(right)
        buildgraph(right, check)


def findportals():
    for n in needtovisit:
        yy = n[0]
        xx = n[1]
        up = (yy - 1, xx)
        down = (yy + 1, xx)
        left = (yy, xx - 1)
        right = (yy, xx + 1)
        n = ""
        p = None
        if tupletomap(up).isalpha():
            up2 = (yy - 2, xx)
            n = "" + tupletomap(up2) + tupletomap(up)
            p = up
        elif tupletomap(down).isalpha():
            down2 = (yy + 2, xx)
            n = "" + tupletomap(down) + tupletomap(down2)
            p = down
        elif tupletomap(left).isalpha():
            left2 = (yy, xx - 2)
            n = "" + tupletomap(left2) + tupletomap(left)
            p = left
        elif tupletomap(right).isalpha():
            right2 = (yy, xx + 2)
            n = "" + tupletomap(right) + tupletomap(right2)
            p = right
        if n != "":
            if n in portals.keys():
                
            portals[n] = p
            graph.add_node(n)


def connectportals():
    for p1 in portals.keys():
        for p2 in portals.keys():
            if p1 is p2:
                continue
            e1 = graph.edges(p1)
            e2 = graph.edges(p2)
            if p1[0] in p2 or p1[1] in p2:
                graph.add_edge(p1, p2)

    # graph = nx.Graph()
    # .add_edge(parent, check)
    # .add_node(check)


needtovisit = set()
for y in range(H):
    for x in range(W):
        if (y, x) != start:
            if MAP[y][x] == '.':
                needtovisit.add((y, x))
findportals()
connectportals()

buildgraph("@", tuple(start), None)
