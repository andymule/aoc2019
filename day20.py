import networkx as nx
import matplotlib.pyplot as plt

filepath = "day20.txt"
MAP = []
alldata = open(filepath).readlines()
for line in alldata:
    MAP.append(line[:-1])
H = len(MAP)
W = len(MAP[0])


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


def buildgraph2(level):
    for y in range(H):
        for x in range(W):
            if MAP[y][x] == '.':
                up = (y - 1, x)
                down = (y + 1, x)
                left = (y, x - 1)
                right = (y, x + 1)
                if tupletomap(up) == '.':
                    graph.add_edge((level, y, x), (level,) + up)
                if tupletomap(down) == '.':
                    graph.add_edge((level, y, x), (level,) + down)
                if tupletomap(left) == '.':
                    graph.add_edge((level, y, x), (level,) + left)
                if tupletomap(right) == '.':
                    graph.add_edge((level, y, x), (level,) + right)


def findportals():
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
                del portals[n]
            else:
                portals[n] = visitme


def findportals2(level):
    global portals2
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
        inner = False
        if visitme[0] in range(5, H - 5) and visitme[1] in range(5, W - 5):
            inner = True
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
            if n == 'AA' or n == 'ZZ':
                jk = 69
            if not inner and level == 0:
                if n != 'AA' and n != 'ZZ':
                    continue
            if level > 0:
                if n == 'AA' or n == 'ZZ':
                    continue
            if level > 0 and not inner and n in portals2[level - 1].keys():
                graph.add_edge(portals2[level - 1][n], (level,) + visitme)
                del portals2[level - 1][n]
            else:
                try:
                    portals2[level][n] = (level,) + visitme
                except:
                    portals2[level] = {}
                    portals2[level][n] = (level,) + visitme


graph = nx.MultiGraph()
# start = (2, 9)
# end = (16, 13)
portals = {}
findportals()  # also connects
start = portals["AA"]
end = portals["ZZ"]
buildgraph()
print("p1:")
# nx.draw(graph)
# plt.show()
print(nx.shortest_path_length(graph, start, end))

# part 2
portals2 = {}
graph = nx.MultiGraph()
for i in range(26):
    findportals2(i)
    buildgraph2(i)
start2 = portals2[0]["AA"]
end2 = portals2[0]["ZZ"]
print("p2:")
print(nx.shortest_path_length(graph, start2, end2))
