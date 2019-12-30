import sys
from sortedcontainers import SortedDict
from collections import defaultdict
from itertools import combinations


def sub_lists(my_list):
    subs = []
    for i in range(0, len(my_list) + 1):
        temp = [list(x) for x in combinations(my_list, i)]
        if len(temp) > 0:
            subs.extend(temp)
    return subs

filepath = "day25.txt"

RAM = SortedDict()
relptr = 0
ptr = 0
_input = 0
image = defaultdict(lambda: defaultdict(lambda: '.'))

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


def getnext():
    global RAM
    global ptr
    ptr += 1
    try:
        return int(RAM[ptr - 1])
    except:
        RAM[ptr - 1] = 0
        return int(RAM[ptr - 1])


GET_SEMI = """west
take semiconductor
east
"""
GET_PLANET = """west
west
take planetoid
east
east
"""
GET_FOOD = """west
west
west
take food ration
east
east
east
"""
GET_FIXED = """west
west
west
west
take fixed point
east
east
east
east
"""
GET_KLEIN = """west
west
west
west
west
take klein bottle
east
east
east
east
east
"""
GET_WEATHER = """west
west
west
west
south
west
take weather machine
east
north
east
east
east
east
"""
GET_PLANET = """west
west
take planetoid
east
east
"""
GET_POINTER = """west
west
south
south
south
take pointer
north
north
north
east
east
"""
GET_COIN = """west
west
south
east
take coin
west
north
east
east
"""

GET_CP = """west
west
south
east
east
north
east
east
"""

things = [
    "food ration",
    "fixed point",
    "weather machine",
    "semiconductor",
    "planetoid",
    "klein bottle",
    "coin",
    "pointer"
]

all = sub_lists(things)
allcounter = 0

dropall = """drop food ration
drop fixed point
drop weather machine
drop semiconductor
drop planetoid
drop klein bottle
drop coin
drop pointer
"""


def newpicks(newtry):
    mytry = ""
    for t in newtry:
        mytry += "take " + t + '\n'
    return mytry


def makeins():
    global dropall, all, allcounter
    newtry = all[allcounter]
    allcounter += 1
    thisone = dropall + newpicks(newtry) + "north\n"
    return list(thisone)


def runDay25():
    global RAM
    global relptr
    global ptr
    imageline = ""
    buf = ""
    instruction_list = GET_COIN + GET_FIXED + GET_FOOD + GET_KLEIN + GET_PLANET + GET_POINTER + GET_SEMI + GET_WEATHER + GET_CP
    instructions = [instruction + '\n' for instruction in instruction_list.split('\n')]
    tooheavy = True
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            RAM[n] = wordsraw[n]
        while True:
            instruct = str(getnext())  # string
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
                p1 = RefOrVal(m1, getnext())
                p2 = RefOrVal(m2, getnext())
                at = int(getnext())
                newval = run(op, p1, p2)
                if p1 == 1182:
                    jk = 69
                assign(m3, at, newval)
            if op == 3:  # assign
                if buf == "":
                    if not instructions:
                        instructions = makeins()

                    buf = instructions.pop(0)
                    jk = 69
                    # buf = input(":") + '\n'
                    # GET_COIN + GET_FIXED + GET_FOOD + GET_KLEIN + GET_PLANET + GET_POINTER + GET_SEMI + GET_WEATHER + GET_CP
                c = buf[0]
                buf = buf[1:]
                read = ord(c)
                assign(m1, getnext(), read)
            if op == 4:  # output
                p1 = RefOrVal(m1, getnext())
                imageline += chr(p1)
                if chr(p1) == '\n':
                    print(imageline[:-1])
                    imageline = ""
            if op == 5:  # branch not zero
                p1 = RefOrVal(m1, getnext())
                p2 = RefOrVal(m2, getnext())
                if p1 != 0:
                    ptr = p2
            if op == 6:  # branch zero
                p1 = RefOrVal(m1, getnext())
                p2 = RefOrVal(m2, getnext())
                if p1 == 0:
                    ptr = p2
            if op == 7:  # less than
                p1 = RefOrVal(m1, getnext())
                p2 = RefOrVal(m2, getnext())
                at = int(getnext())
                if p1 < p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 8:  # equal to
                p1 = RefOrVal(m1, getnext())
                p2 = RefOrVal(m2, getnext())
                at = int(getnext())
                if p1 == p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 9:  # move ref
                p1 = RefOrVal(m1, getnext())
                relptr += p1
            if op == 99:  # exit
                print("EXITING")
                return


runDay25()
