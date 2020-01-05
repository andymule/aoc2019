import math
import sys
import pprint
from sortedcontainers import SortedDict

filepath = "day19.txt"

RAM = SortedDict()
relptr = 0
ptr = 0
# _input = 1

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
}


def run(op, a, b):
    return codes[op](a, b)


def assign(mode, at, val):
    global RAM
    global relptr
    global ptr
    if mode == 0:
        RAM[at] = val
    elif mode == 2:
        RAM[relptr + at] = val
    else:
        print("ERROR ASSIGNING!")
        sys.exit(1)


def RefOrVal(mode, get):
    global RAM
    global relptr
    global ptr
    if mode == 0:
        try:
            return int(RAM[get])
        except:
            RAM[get] = 0
            return int(RAM[get])
    elif mode == 1:
        return int(get)
    elif mode == 2:
        try:
            return int(RAM[relptr + get])
        except:
            RAM[relptr + get] = 0
            return int(RAM[relptr + get])
    else:
        print("ERROR ACCESSING MEMORY")
        sys.exit(1)


def next(p):
    global RAM
    global ptr
    ptr += 1
    try:
        return int(RAM[ptr - 1])
    except:
        RAM[ptr - 1] = 0
        return int(RAM[ptr - 1])


def runDay9(y1, x1):
    global RAM
    global relptr, inside, outside
    global ptr
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        RAMraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(RAMraw)):
            RAM[n] = RAMraw[n]
        firsttime = True
        while True:
            instruct = str(next(ptr))  # string
            op = int(instruct[-2:])
            m1 = 0
            m2 = 0
            m3 = 0
            if len(instruct) > 2:  # mode 1
                m1 = int(instruct[-3:-2])
            if len(instruct) > 3:  # mode 2
                m2 = int(instruct[-4:-3])
            if len(instruct) > 4:  # mode 3
                m3 = int(instruct[-5:-4])
            if op == 1 or op == 2:  # arithmetic
                p1 = RefOrVal(m1, next(ptr))
                p2 = RefOrVal(m2, next(ptr))
                at = int(next(ptr))
                newval = run(op, p1, p2)
                assign(m3, at, newval)
            if op == 3:  # assign
                if firsttime == True:
                    assign(m1, next(ptr), x1)
                else:
                    assign(m1, next(ptr), y1)
                firsttime = False
            if op == 4:  # output
                p1 = RefOrVal(m1, next(ptr))
                if p1 == 1:
                    inside.add((y1, x1))
                else:
                    outside.add((y1, x1))
            # print(p1)
            if op == 5:  # branch not zero
                p1 = RefOrVal(m1, next(ptr))
                p2 = RefOrVal(m2, next(ptr))
                if p1 != 0:
                    ptr = p2
            if op == 6:  # branch zero
                p1 = RefOrVal(m1, next(ptr))
                p2 = RefOrVal(m2, next(ptr))
                if p1 == 0:
                    ptr = p2
            if op == 7:  # less than
                p1 = RefOrVal(m1, next(ptr))
                p2 = RefOrVal(m2, next(ptr))
                at = int(next(ptr))
                if p1 < p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 8:  # equal to
                p1 = RefOrVal(m1, next(ptr))
                p2 = RefOrVal(m2, next(ptr))
                at = int(next(ptr))
                if p1 == p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 9:  # move ref
                p1 = RefOrVal(m1, next(ptr))
                relptr += p1
            if op == 99:  # exit
                return
                # sys.exit(0)


def printmap(x, y):
    global inside, outside
    for yy in range(y + 1):
        s = ""
        for xx in range(x + 1):
            if (yy, xx) in inside:
                s += '#'
            else:
                s += '.'
        print(s)


def dorun(yyy, xxx):
    global RAM, relptr, ptr, inside, outside
    if (yyy, xxx) in inside or (xxx, yyy) in outside:
        return
    RAM = SortedDict()
    relptr = 0
    ptr = 0
    runDay9(yyy, xxx)


inside = set()
outside = set()
# manually calculated slope of beam from image
slope = .3  # conservative manually found slope 
stop = False
y = 1130  # manual binary search to find
while True:
    for x in range(int(y * slope) - 200, y + 2000, 100):
        if x < 0:
            break
        dorun(y, x)
        if (y, x) in inside:
            thiscount = 0
            minx = x
            maxx = x
            for xx in range(x, x - 101, -1):
                dorun(y, xx)
                if (y, xx) in inside:
                    minx = min(minx, xx)
                    maxx = max(maxx, xx)
                    thiscount += 1
            for xx in range(x + 1, x + 2000, 1):
                dorun(y, xx)
                if (y, xx) in inside:
                    minx = min(minx, xx)
                    maxx = max(maxx, xx)
                    thiscount += 1
                else:
                    break
            if thiscount >= 100:
                # print(y, minx, maxx+1)
                for xxx in range(minx, maxx + 1):
                    ycount = 0
                    for yyy in range(y, y + 100):
                        dorun(yyy, xxx)
                        if (yyy, xxx) in inside:
                            ycount += 1
                        else:
                            break
                        if ycount == 100 and (y, xxx + 99) in inside:
                            print(xxx, y)
                            break
    y += 1

print(x * 10000 + y)
