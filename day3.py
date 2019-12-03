import math
import sys
import pprint

filepath = "day3.txt"

wire1 = {}
wire1L = {}
wire2 = {}
wire2L = {}
hits = []
hitsL = {}
p1 = (0,0)
p2 = (0,0)

sign = lambda x: int(math.copysign(1, x))

def add(n1, n2):
    return (n1[0]+n2[0], n1[1]+n2[1])

def sub(n1, n2):
    return (n1[0]-n2[0], n1[1]-n2[1])

def build(wire, p, words, other, L, L2):
    global hits
    minwire = 1000000000000
    dist = 0
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    wire[p] = 'o'
    for w in words:
        wire[p] = '+'
        if other is not None:
            try:
                if p in other:
                    other[p]='X'
                    hits.append(p)
            except: 
                pass
        if w[0] == 'R':
            maxx+=int(w[1:])
            for i in range(int(w[1:])):
                dist+=1
                p = add(p,(1,0))
                wire[p] = '-'
                L[p] = dist
                if other is not None:
                    try:
                        if p in other:
                            other[p]='X'
                            if dist+L2[p] < minwire:
                                minwire = dist+L2[p]
                            hits.append(p)
                    except: 
                        pass
        if w[0] == 'L':
            minx-=int(w[1:])
            for i in range(int(w[1:])):
                dist+=1
                p = sub(p,(1,0))
                wire[p] = '-'
                L[p] = dist
                if other is not None:
                    try:
                        if p in other:
                            other[p]='X'
                            if dist+L2[p] < minwire:
                                minwire = dist+L2[p]
                            hits.append(p)
                    except: 
                        pass
        if w[0] == 'D':
            miny-=int(w[1:])
            for i in range(int(w[1:])):
                dist+=1
                p = sub(p,(0,1))
                wire[p] = '|'
                L[p] = dist
                if other is not None:
                    try:
                        if p in other:
                            other[p]='X'
                            if dist+L2[p] < minwire:
                                minwire = dist+L2[p]
                            hits.append(p)
                    except: 
                        pass
        if w[0] == 'U':
            maxy+=int(w[1:])
            for i in range(int(w[1:])):
                dist+=1
                p = add(p,(0,1))
                wire[p] = '|'
                L[p] = dist
                if other is not None:
                    try:
                        if p in other:
                            other[p]='X'
                            if dist+L2[p] < minwire:
                                minwire = dist+L2[p]
                            hits.append(p)
                    except: 
                        pass
    hits = list(dict.fromkeys(hits))
    print(minwire)
    return (minx,maxx, miny, maxy)

def printwire(wire, r):
    for y in range(r[3]+3, r[2]-1, -1):
        l = ""
        for x in range(r[0]-1, r[1]+3):
            try:
                l += wire[(x,y)]
            except:
                l += '.'
        print(l)

def findClosest():
    global hits
    least = 10000000
    for h in hits:
        n = abs(h[0]) + abs(h[1])
        if n < least:
            least = n
    print(least)
        

with open(filepath) as file:
    # alldata = file.read().replace("\n", "")
    r1 = build(wire1, p1, file.readline().split(','), None, wire1L, None)
    r2 = build(wire2, p2, file.readline().split(','), wire1, wire2L, wire1L)
    hits.remove((0,0))
    findClosest()
    # printwire(wire1, r1)


