import sys
import time, os
from collections import defaultdict
import json
import keyboard
import networkx as nx
from sortedcontainers import SortedDict
import curses

# from pynput import keyboard

manualStepper = 0
yPos = 0
xPos = 0
blankChar = " "
MAP = defaultdict(lambda: defaultdict(lambda: blankChar))
MAP[yPos][xPos] = '@'
goalX = -69
goalY = -69
startX = 0
startY = 0

words = SortedDict()
relptr = 0
ptr = 0
filepath = "day15.txt"

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


def nextPtr(p):
    global words, ptr
    ptr += 1
    try:
        return int(words[ptr - 1])
    except:
        words[ptr - 1] = 0
        return int(words[ptr - 1])


def DrawMap():
    global MAP, goalX, goalY, manualStepper, startX, startY, blankChar, xPos, yPos
    os.system('cls' if os.name == 'nt' else 'clear')  # clears screen
    # print('\n')  # * 10)  # prints 80 line breaks
    yStart = sorted(MAP.keys())[0]
    ySpan = len(MAP.keys())
    minX = 0
    maxX = 0
    if goalX != -69 and goalY != -69:
        MAP[goalY][goalX] = '$'
    MAP[startY][startX] = 'X'
    for y in range(yStart, yStart + ySpan):
        for x in MAP[y].keys():
            if MAP[y][x] != blankChar and x < minX:
                minX = x
            if MAP[y][x] != blankChar and x > maxX:
                maxX = x
    for y in range(yStart, yStart + ySpan):
        s = ""
        for x in range(minX, maxX + 1):
            # if x == startX and y == startY: # and xPos != startX and yPos != startY:
            # s += 'X'
            if x == xPos and y == yPos:
                s += '@'
            # elif x == goalX and y == yPos and (goalX != -69 and goalX != goalX):
            # s += '$'
            else:
                s += MAP[y][x]
        print(s)
    print()
    print(manualStepper)


def runDay15():
    global words, relptr, ptr, xPos, yPos, goalX, goalY, MAP, manualStepper
    with open(filepath) as file:
        alldata: str = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            words[n] = wordsraw[n]
        move = 1
        lastSignal = 0
        realMove = False
        # takeinputnow = False
        takeinputcount = 0
        while True:
            instruct = str(nextPtr(ptr))  # string
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
                p1 = RefOrVal(m1, nextPtr(ptr))
                p2 = RefOrVal(m2, nextPtr(ptr))
                at = int(nextPtr(ptr))
                newval = run(op, p1, p2)
                assign(m3, at, newval)
            if op == 3:  # assign
                if takeinputcount % 9 == 0:
                    takeinputcount = 1
                    DrawMap()
                    key = keyboard.read_key(True)
                    realMove = True
                    while not (key == 'a' or key == 'w' or key == 's' or key == 'd'):
                        if key == 'q':
                            manualStepper = 0
                            DrawMap()
                        if key == 'o':
                            with open("map.json", 'w') as outfile:
                                json.dump(MAP, outfile)
                        if key == 'l':
                            with open("map.json") as infile:
                                NEWMAP = json.load(infile)
                                NEWMAP = {int(k): v for k, v in NEWMAP.items()}
                                for k in NEWMAP.keys():
                                    NEWMAP[k] = {int(k): v for k, v in NEWMAP[k].items()}
                                MAP = defaultdict(lambda: defaultdict(lambda: blankChar))
                                for y, d in NEWMAP.items():
                                    for x, v in NEWMAP[y].items():
                                        MAP[y][x] = NEWMAP[y][x]
                                DrawMap()
                        key = keyboard.read_key(True)
                    time.sleep(.01)
                else:
                    takeinputcount += 1
                    if takeinputcount == 2:
                        key = 'a'
                    if takeinputcount == 3:
                        if lastSignal != 0:
                            key = 'd'
                    if takeinputcount == 4:
                        key = 'd'
                    if takeinputcount == 5:
                        if lastSignal != 0:
                            key = 'a'
                    if takeinputcount == 6:
                        key = 'w'
                    if takeinputcount == 7:
                        if lastSignal != 0:
                            key = 's'
                    if takeinputcount == 8:
                        key = 's'
                    if takeinputcount == 9:
                        if lastSignal != 0:
                            key = 'w'
                if key == 'a':
                    move = 3
                if key == 'w':
                    move = 1
                if key == 's':
                    move = 2
                if key == 'd':
                    move = 4
                assign(m1, nextPtr(ptr), move)
                # assign(m1, next(ptr), _input)
            if op == 4:  # output
                p1 = RefOrVal(m1, nextPtr(ptr))
                lastSignal = p1
                tempX = xPos
                tempY = yPos
                if move == 3:
                    tempX -= 1
                if move == 1:
                    tempY -= 1
                if move == 2:
                    tempY += 1
                if move == 4:
                    tempX += 1
                if p1 == 0:
                    MAP[tempY][tempX] = "#"
                    if realMove:
                        realMove = False
                if p1 == 1:  # moved in direction
                    # MAP[tempY][tempX] = "@"
                    MAP[yPos][xPos] = "."
                    xPos = tempX
                    yPos = tempY
                    if realMove:
                        manualStepper += 1
                        realMove = False
                if p1 == 2:
                    MAP[tempY][tempX] = "$"
                    MAP[yPos][xPos] = "."
                    xPos = tempX
                    yPos = tempY
                    goalX = xPos
                    goalY = yPos
                    if realMove:
                        manualStepper += 1
                        realMove = False

            # print(p1)
            if op == 5:  # branch not zero
                p1 = RefOrVal(m1, nextPtr(ptr))
                p2 = RefOrVal(m2, nextPtr(ptr))
                if p1 != 0:
                    ptr = p2
            if op == 6:  # branch zero
                p1 = RefOrVal(m1, nextPtr(ptr))
                p2 = RefOrVal(m2, nextPtr(ptr))
                if p1 == 0:
                    ptr = p2
            if op == 7:  # less than
                p1 = RefOrVal(m1, nextPtr(ptr))
                p2 = RefOrVal(m2, nextPtr(ptr))
                at = int(nextPtr(ptr))
                if p1 < p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 8:  # equal to
                p1 = RefOrVal(m1, nextPtr(ptr))
                p2 = RefOrVal(m2, nextPtr(ptr))
                at = int(nextPtr(ptr))
                if p1 == p2:
                    assign(m3, at, 1)
                else:
                    assign(m3, at, 0)
            if op == 9:  # move ref
                p1 = RefOrVal(m1, nextPtr(ptr))
                relptr += p1
            if op == 99:  # exit
                print("EXITING")
                sys.exit(0)


# runDay15()

wholemap = (
" ### ### ############# # ########### ### \n"
"#...#...#.............#.#...........#...#\n"
"#.#.#.#.###.#########.#.#.###.#####.###.#\n"
"#.#...#...#...#.....#.#.#.#...#.........#\n"
"#.#######.###.#.#####.#.#.#.###########.#\n"
"#.#...........#.......#.#.#.......#...#.#\n"
"#.###.#########.#######.#.#######.#.#.#.#\n"
"#...#.#.......#.#...............#.#.#...#\n"
" ##.###.#####.#.#.###########.###.#.#### \n"
"#...#...#...#.#.#...#...#.....#...#.#...#\n"
"#.###.###.#.#.#.#####.#.#.#####.###.###.#\n"
"#...#...#.#.#.#...#...#.#...#...#.......#\n"
"#.#.###.###.#.###.#.###.#####.########## \n"
"#.#...#.#...#.#...#.#.#.......#...#.....#\n"
" ####.#.#.###.#.###.#.###.#####.#.#.###.#\n"
"#.....#.#...#.#.....#...#.#...#.#.....#.#\n"
"#.#####.#.#.#.#######.#.#.#.#.#.#######.#\n"
"#.#.....#.#.#...#.....#...#.#...#.......#\n"
"#.#...........#.......#.#.#.......#...#.#\n"
"#.###.#########.#######.#.#######.#.#.#.#\n"
"#...#.#.......#.#...............#.#.#...#\n"
" ##.###.#####.#.#.###########.###.#.#### \n"
"#...#...#...#.#.#...#...#.....#...#.#...#\n"
"#.###.###.#.#.#.#####.#.#.#####.###.###.#\n"
"#...#...#.#.#.#...#...#.#...#...#.......#\n"
"#.#.###.###.#.###.#.###.#####.########## \n"
"#.#...#.#...#.#...#.#.#.......#...#.....#\n"
" ####.#.#.###.#.###.#.###.#####.#.#.###.#\n"
"#.....#.#...#.#.....#...#.#...#.#.....#.#\n"
"#.#####.#.#.#.#######.#.#.#.#.#.#######.#\n"
"#.#.....#.#.#...#.....#...#.#...#.......#\n"
"#.#.#######.###.###########.#####.###### \n"
"#.#.#.....#...#.#...........#...#.#.....#\n"
"#.#.#.#.#.#.#.#.#.#####.#####.###.#.###.#\n"
"#.#.#.#.#...#.#.#.#...#...#.....#.#.#...#\n"
"#.#.###.#####.#.#.#.#####.#####.#.#.#.## \n"
"#.#...#.....#.#...#.#...#.#.....#.#.#...#\n"
"#.###.#.###.#####.#.#.###.#.#.###.#####.#\n"
"#.....#.#...#...#.#.#.......#.#...#.....#\n"
"#.#####.#.###.#.###.###########.###.#### \n"
"#...#...#...#.#.....#...........#.......#\n"
" ##.###.###.#.#######.###########.#####.#\n"
"#.#...#.#...#.........#...#.....#.#.....#\n"
"#.###.###.#.###########.###.#.###.#.###.#\n"
"#.#...#...#.#...#.....#.#...#.....#.#...#\n"
"#.#.###.###.#.#.#.###.#.#.#########.#.## \n"
"#...#...#.#...#.#.#...#.#.#......$#.#...#\n"
"#.###.###.#####.#.#.###.#.###.#.###.###.#\n"
"#.#...#.......#...#.#.........#.#...#.#.#\n"
"#.###.#.###.#######.#########.###.###.#.#\n"
"#.#...#.#.#.......#...#.....#.#...#.....#\n"
"#.#.###.#.#######.###.#.###.###.###.#### \n"
"#...#...........#.......#.......#.......#\n"
" ### ########### ####### ####### ####### \n")


# print(wholemap)
# 41 wide, 54 tall

def at(y, x):
    global wholemaplist
    pos = 42 * y + x
    return wholemaplist[pos]


def make(y, x, b):
    global wholemaplist
    pos = 42 * y + x
    wholemaplist[pos] = b
    jk = 69

minutesPassed = 0
wholemaplist = list(wholemap)
mymiddleX = 21
mymiddleY = 34
ox = 12 + mymiddleX
oy = 12 + mymiddleY
oxy = set()
oxy.add((oy, ox))

make(oy,ox, '☺')

def expand():
    global oxy, wholemaplist, minutesPassed
    newoxy = set()
    changed = False
    for o in oxy:
        if o[0] < 54 and at(o[0] + 1, o[1]) == '.':  # lower
            newoxy.add((o[0] + 1, o[1]))
        if o[0] > 1 and at(o[0] - 1, o[1]) == '.':  # upper
            newoxy.add((o[0] - 1, o[1]))
        if o[1] > 1 and at(o[0], o[1] - 1) == '.':  # left
            newoxy.add((o[0], o[1] - 1))
        if o[1] < 41 and at(o[0], o[1] + 1) == '.':  # right
            newoxy.add((o[0], o[1] + 1))
    for o in newoxy:
        changed = True
        make(o[0], o[1], '♥')
    if not changed:
        print(minutesPassed)
        sys.exit(0)
    else:
        changed = False
        minutesPassed += 1
    oxy.update(newoxy)
    
#376 too high, so is 374
    # print("".join(wholemaplist))
    jk = 69

while True:
    expand()
# make(o[0] + 1, o[1], newmap, '$')
