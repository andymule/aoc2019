import math
import sys
import pprint
from sortedcontainers import SortedDict
from collections import defaultdict

# filepath = "/mnt/d/Webs/aoc2019/day11.txt"
filepath = "day11.txt"

words = SortedDict()
relptr = 0
ptr = 0
_input = 1
paint=defaultdict(lambda: defaultdict(lambda: 0))
didpaint=set() #defaultdict(lambda: defaultdict(lambda: False))
posx=0
posy=0
facing=0 # up
# After the robot turns, it should always move forward exactly one panel.

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
}

flipflop = True
def paintit(p):
    global flipflop, paint, didpaint, posx, posy, facing
    if flipflop:
        didpaint.add((posy,posx))
        paint[posy][posx] = p
        flipflop = False
    else:
        # 0 up, 1 right, 2 down, 3 left, 4%4 = 0
        if p == 0:
            facing -= 1
        if p==1:
            facing += 1
        facing = facing % 4
        if facing==0:
            posy+=1
        if facing==1:
            posx+=1
        if facing==2:
            posy-=1
        if facing==3:
            posx-=1
        flipflop = True
# not 249
# not 102
# not 103
#is ZRZPKEZR
def End():
    for y in range(0,-6, -1):
        s = ""
        for x in range(0,42):
            val = paint[y][x]
            c = '.'
            if val == 1:
                c = '#'
            s += c
        print(s)


    import matplotlib 
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt

    colors = {}
    for y in paint.keys():
        for x in paint[y]:
            colors[(x,y)] = paint[y][x]
    white = [k for k,v in colors.items() if v == 1]
    x,y=zip(*white)
    plt.figure(figsize=(4,.5))
    plt.plot(x,y, 'ko')

    plt.savefig('output.png')
    
    print(len(didpaint))
    sys.exit(0)

def run(op, a, b):
    return codes[op](a, b)


def assign(mode, at, val):
    global words
    global relptr
    global ptr
    if mode == 0:
        words[at] = val
    elif mode == 2:
        words[relptr + at] = val
    else:
        print("ERROR ASSIGNING!")
        sys.exit(1)



def RefOrVal(mode, get):
    global words
    global relptr
    global ptr
    if mode == 0:
        try:
            return int(words[get])
        except:
            words[get] = 0
            return int(words[get])
    elif mode == 1:
        return int(get)
    elif mode == 2:
        try:
            return int(words[relptr + get])
        except:
            words[relptr + get] = 0
            return int(words[relptr + get])
    else:
        print("ERROR ACCESSING MEMORY")
        sys.exit(1)


def next(p):
    global words
    global ptr
    ptr += 1
    try:
        return int(words[ptr - 1])
    except:
        words[ptr - 1] = 0
        return int(words[ptr - 1])

#part 2
paint[0][0] = 1
def runDay11():
    global words
    global relptr
    global ptr, flipflop, _input
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            words[n] = wordsraw[n]
        while True:
            if flipflop == True:
                if _input != paint[posy][posx]:
                    jk=69
                _input = paint[posy][posx]
                
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
                assign(m1, next(ptr), _input)
            if op == 4:  # output
                p1 = RefOrVal(m1, next(ptr))
                # print(p1)
                paintit(p1)
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
                End()

runDay11()

