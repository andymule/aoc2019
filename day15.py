import math, sys, pprint, os
from sortedcontainers import SortedDict
from collections import defaultdict
import keyboard

filepath = "day15.txt"

words = SortedDict()
MAP = defaultdict(lambda: defaultdict(lambda: " "))
relptr = 0
ptr = 0
_input = 1
lastcode = 0

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
}


def run(op, a, b):
    return codes[op](a, b)


def assign(mode, at, val):
    global words, relptr, ptr
    if mode == 0:
        words[at] = val
    elif mode == 2:
        words[relptr + at] = val
    else:
        print("ERROR ASSIGNING!")
        sys.exit(1)


def RefOrVal(mode, get):
    global words, relptr, ptr
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
    global words, ptr
    ptr += 1
    try:
        return int(words[ptr - 1])
    except:
        words[ptr - 1] = 0
        return int(words[ptr - 1])


def DrawMap():
    global MAP
    os.system('cls' if os.name == 'nt' else 'clear')  # clears screen
    print('\n'*80) # prints 80 line breaks
    yStart = sorted(MAP.keys())[0]
    ySpan = len(MAP.keys())
    minX = 0
    maxX = 0
    for y in range(yStart, ySpan):
        for x in MAP[y].keys():
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
    for y in range(yStart, ySpan):
        s = ""
        for x in range(minX, maxX+1):
            s += MAP[y][x]
        print(s)

MAP[0][0] = '@'


def runDay15():
    global words, lastcode, relptr, ptr
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            words[n] = wordsraw[n]
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
                move = 1
                DrawMap()
                key = keyboard.read_key()
                if key == 'a':
                    move = 3
                if key == 'w':
                    move = 1
                if key == 's':
                    move = 2
                if key == 'd':
                    move = 4
                assign(m1, next(ptr), move)
                # assign(m1, next(ptr), _input)
            if op == 4:  # output
                p1 = RefOrVal(m1, next(ptr))
                lastcode = p1

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
                print("EXITING")
                sys.exit(0)


runDay15()
