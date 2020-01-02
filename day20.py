import networkx as nx
import os, sys, collections
import matplotlib.pyplot as plt

filepath = "day20.txt"
MAP = []
alldata = open(filepath).readlines()
for line in alldata:
    MAP.append(line[:-1])
H = len(MAP)
W = len(MAP[0])

graph = nx.MultiGraph()
# start = (2, 9)
# end = (16, 13)
portals = {}


# for y in range(H):
#     s = ""
#     for x in range(W):
#         if (y, x) == start:
#             s += '☻'
#         elif (y, x) == end:
#             s += '♥'
#         else:
#             s += MAP[y][x]
#     print(s)


def tupletomap(t):
    return MAP[t[0]][t[1]]


def buildgraph():
    for y in range(H):
        for x in range(W):
            if MAP[y][x] == '.':
                up = (y - 1, x)
                down = (y + 1, x)
                left = (y, x - 1)
                right = (y, x + 1)
                if tupletomap(up) == '.':
                    graph.add_edge((y, x), up)
                if tupletomap(down) == '.':
                    graph.add_edge((y, x), down)
                if tupletomap(left) == '.':
                    graph.add_edge((y, x), left)
                if tupletomap(right) == '.':
                    graph.add_edge((y, x), right)


def findportals():
    didvisit = set()
    needtovisit = set()
    for y in range(H):
        for x in range(W):
            if MAP[y][x] == '.':
                needtovisit.add((y, x))
    for visitme in needtovisit:
        yy = int(visitme[0])
        xx = int(visitme[1])
        up = (yy - 1, xx)
        down = (yy + 1, xx)
        left = (yy, xx - 1)
        right = (yy, xx + 1)
        n = ""
        if tupletomap(up).isalpha():
            up2 = (yy - 2, xx)
            n = "" + tupletomap(up2) + tupletomap(up)
        elif tupletomap(down).isalpha():
            down2 = (yy + 2, xx)
            n = "" + tupletomap(down) + tupletomap(down2)
        elif tupletomap(left).isalpha():
            left2 = (yy, xx - 2)
            n = "" + tupletomap(left2) + tupletomap(left)
        elif tupletomap(right).isalpha():
            right2 = (yy, xx + 2)
            n = "" + tupletomap(right) + tupletomap(right2)
        if n != "":
            if n in portals.keys():
                graph.add_edge(portals[n], visitme)
                didvisit.add(visitme)
                didvisit.add(portals[n])
                del portals[n]
            else:
                portals[n] = visitme
    for d in didvisit:
        needtovisit.remove(d)


findportals()  # also connects
start = portals["AA"]
end = portals["ZZ"]
buildgraph()
print("finding shortest:")
# nx.draw(graph)
# plt.show()
print(nx.shortest_path_length(graph, start, end))
