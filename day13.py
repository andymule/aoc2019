import math
import sys
import pprint
from sortedcontainers import SortedDict

filepath = "day13.txt"

RAM = SortedDict()
relptr = 0
ptr = 0
_input = 0

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
        words[at] = val
    elif mode == 2:
        words[relptr + at] = val
    else:
        print("ERROR ASSIGNING!")
        sys.exit(1)


def RefOrVal(mode, get):
    global RAM
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
    global RAM
    global ptr
    ptr += 1
    try:
        return int(words[ptr - 1])
    except:
        words[ptr - 1] = 0
        return int(words[ptr - 1])

joystickX = 0
lasttwo = [0,0]
outputcounter = 0
tilecount = 0
lastballX = 0
def runDay9():
    global RAM
    global relptr
    global ptr, tilecount, outputcounter, joystickX, lastballX
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        wordsraw = [int(n) for n in alldata.split(",")]  # ints
        for n in range(0, len(wordsraw)):
            words[n] = wordsraw[n]
        words[0] = 2 #free quarters
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
                assign(m1, next(ptr), _input)
            if op == 4:  # output
                p1 = RefOrVal(m1, next(ptr))
                outputcounter += 1
                outputcounter = outputcounter % 3
                if lasttwo[0]==-1 and lasttwo[1]==0:
                    print(p1) #print score    
                # print(p1)
                if outputcounter == 0 and p1 == 2: #command and block
                    # if lasttwo[0] < joystickX:
                        # pass
                        # _input = 
                    tilecount += 1
                elif outputcounter == 0 and p1 == 4: #command and ball
                    lastballX = lasttwo[0]
                    if joystickX < lastballX:
                        _input = 1
                    elif joystickX > lastballX:
                        _input = -1
                    else:
                        _input = 0
                elif outputcounter == 0 and p1 == 3: #command and paddle
                    joystickX = lasttwo[0]    
                    if joystickX < lastballX:
                        _input = 1
                    elif joystickX > lastballX:
                        _input = -1
                    else:
                        _input = 0
                else:
                    lasttwo.pop(0)
                    lasttwo.append(p1)
                
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
                print(tilecount)
                return
                # sys.exit(0)

runDay9()