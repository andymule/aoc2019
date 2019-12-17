import math
import sys
import pprint
from sortedcontainers import SortedDict
from collections import defaultdict

filepath = "day17.txt"

RAM = SortedDict()
relptr = 0
ptr = 0
_input = 1
image = defaultdict(lambda: defaultdict(lambda: '.'))
commands = "A,A,A,A,A,A,A,A,A\n1,1,1,1\nR,8\nL,1\ny\n"
commandptr = 0
realcommands = []
realcommands.append("L,10,R,8,R,6,R,10")
realcommands.append("L,12,R,8,L,12,L,10")
realcommands.append("R,8,R,6,R,10,L,12")
realcommands.append("R,8,L,12,L,10,R,8")
realcommands.append("R,8,L,10,R,8,R,8")
realcommands.append("L,12,R,8,L,12,L,10")
realcommands.append("R,8,R,6,R,10,L,10")
realcommands.append("R,8,R,8,L,10,R,8")
realcommands.append("R,6,R,10")

realcommandcounter = 0


def INJECT():
    global realcommandcounter, realcommands, RAM
    r = realcommands[realcommandcounter]
    realcommandcounter += 1
    index = 0
    startdex = 1193
    nums = r.split(",")
    s = ""
    RAM[startdex+index] = len(nums)
    for n in nums:
        index += 1
        if n.isdigit():
            RAM[startdex+index] = int(n)
        else:
            if n == 'R':
                RAM[startdex + index] = -4
            elif n == 'L':
                RAM[startdex + index] = -5
            else:
                jk=69


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
    if relptr + get == 1182 or get == 1182:
        jk = 69
    elif relptr + get == 1193 or get == 1193:
        jk = 69
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


def runDay17():
    global RAM
    global relptr
    global ptr, commands, commandptr
    xcount = 0
    ycount = 0
    imageline = ""
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            RAM[n] = wordsraw[n]
        RAM[0] = 2
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
                if p1 == 1182:
                    jk = 69
                assign(m3, at, newval)
            if op == 3:  # assign
                print("input:")
                read = ord(commands[commandptr])
                commandptr += 1
                assign(m1, next(ptr), read)
                # assign(m1, next(ptr), _input)
            if op == 4:  # output
                p1 = RefOrVal(m1, next(ptr))
                imageline += chr(p1)
                if chr(p1) == '\n':
                    if len(imageline) == 1:
                        jk = 69  # computer newline
                        # INJECT()
                    print(imageline[:-1])
                    imageline = ""
                # image[ycount][xcount] = chr(p1)
                # if chr(p1) == '\n':
                #     ycount += 1
                #     xcount = 0
                # else:
                #     xcount += 1
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
                # sys.exit(0)
                return


runDay17()
# h = len(image.keys())
# w = len(image[0].keys())
# intersects = set()
# for y in range(0, h):
#     s = ""
#     for x in range(0, w):
#         c = image[y][x]
#         if c == '#':
#             if image[y+1][x] == '#' and  image[y-1][x] == '#' and image[y][x+1] == '#' and image[y][x-1] == '#':
#                 intersects.add((y,x))
#         s += c
#     print(s[:-1])
#     # a.append(s[:-1])
#
# total = 0
# for i in intersects:
#     total += i[0]*i[1]
# print(total)
