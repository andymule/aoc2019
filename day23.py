import math
import sys
import pprint
from sortedcontainers import SortedDict
import logging
import threading
import time

filepath = "day23.txt"
ids = [x for x in range(50)]
idctr = 0

RAM = SortedDict()
RAMS = {}
relptr = 0
relptrs = {}
ptr = 0
ptrs = {}
inputs = {}
queues = {}
sleeping = set()

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
}

def run(code, a, b):
    return codes[code](a, b)


def assign(mode, at, val, uid):
    global RAMS
    global relptrs
    if mode == 0:
        RAMS[uid][at] = val
    elif mode == 2:
        RAMS[uid][relptrs[uid] + at] = val
    else:
        print("ERROR ASSIGNING!", flush=True)
        sys.exit(1)


def RefOrVal(mode, get, uid):
    global RAMS
    global relptrs
    if mode == 0:
        try:
            return int(RAMS[uid][get])
        except:
            RAMS[uid][get] = 0
            return int(RAMS[uid][get])
    elif mode == 1:
        return int(get)
    elif mode == 2:
        try:
            return int(RAMS[uid][relptrs[uid] + get])
        except:
            RAMS[uid][relptrs[uid] + get] = 0
            return int(RAMS[uid][relptrs[uid] + get])
    else:
        print("ERROR ACCESSING MEMORY", flush=True)
        sys.exit(1)


def getnext(uid):
    global RAMS
    global ptrs
    ptrs[uid] += 1
    try:
        return int(RAMS[uid][ptrs[uid] - 1])
    except:
        RAMS[uid][ptrs[uid] - 1] = 0
        return int(RAMS[uid][ptrs[uid] - 1])

sleepEvent = threading.Event()
def main(uid):
    global RAMS, RAM
    global relptrs, relptr
    global ptrs, ptr
    global inputs, queues, sleeping, globalfirst
    alldata = open(filepath).read().replace("\n", "")
    wordsraw = [int(n) for n in alldata.split(",")]  # ints
    for n in range(0, len(wordsraw)):
        RAM[n] = wordsraw[n]
    RAMS[uid] = RAM.copy()
    relptrs[uid] = relptr
    ptrs[uid] = ptr
    queues[uid] = []
    first = True
    midread = None
    newmessage = []
    sleepEvent.wait(20)
    while True:
        instruct = str(getnext(uid))  # string
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
            p1 = RefOrVal(m1, getnext(uid), uid)
            p2 = RefOrVal(m2, getnext(uid), uid)
            at = int(getnext(uid))
            newval = run(op, p1, p2)
            assign(m3, at, newval, uid)
        if op == 3:  # assign
            # assign(m1, getnext(uid), inputs[uid], uid)
            if first:
                assign(m1, getnext(uid), uid, uid)
                first = False
            else:
                if midread is not None:
                    if uid in sleeping:
                        sleeping.remove(uid)
                    assign(m1, getnext(uid), midread, uid)
                    midread = None
                elif len(queues[uid]) > 0:
                    if uid in sleeping:
                        sleeping.remove(uid)
                    newcom = queues[uid].pop(0)
                    assign(m1, getnext(uid), newcom[0], uid)
                    midread = newcom[1]
                else:
                    assign(m1, getnext(uid), -1, uid)
                    time.sleep(1)
                    sleeping.add(uid)
                    if len(sleeping) == 50:
                        totallength = 0
                        for k in queues.keys():
                            if k == 255:
                                continue
                            else:
                                totallength += len(queues[k])
                        if totallength == 0:
                            queues[0].append((queues[255][0], queues[255][1]))
                            print(queues[255], flush=True)

        if op == 4:  # output
            p1 = RefOrVal(m1, getnext(uid), uid)
            newmessage.append(p1)
            if len(newmessage) == 3:
                try:
                    if newmessage[0] == 255:
                        queues[255] = (newmessage[1], newmessage[2])
                    else:
                        queues[newmessage[0]].append((newmessage[1], newmessage[2]))
                except:
                    queues[newmessage[0]] = []
                    queues[newmessage[0]].append((newmessage[1], newmessage[2]))
                # print(newmessage, flush=True)
                newmessage = []
        if op == 5:  # branch not zero
            p1 = RefOrVal(m1, getnext(uid), uid)
            p2 = RefOrVal(m2, getnext(uid), uid)
            if p1 != 0:
                ptrs[uid] = p2
        if op == 6:  # branch zero
            p1 = RefOrVal(m1, getnext(uid), uid)
            p2 = RefOrVal(m2, getnext(uid), uid)
            if p1 == 0:
                ptrs[uid] = p2
        if op == 7:  # less than
            p1 = RefOrVal(m1, getnext(uid), uid)
            p2 = RefOrVal(m2, getnext(uid), uid)
            at = int(getnext(uid))
            if p1 < p2:
                assign(m3, at, 1, uid)
            else:
                assign(m3, at, 0, uid)
        if op == 8:  # equal to
            p1 = RefOrVal(m1, getnext(uid), uid)
            p2 = RefOrVal(m2, getnext(uid), uid)
            at = int(getnext(uid))
            if p1 == p2:
                assign(m3, at, 1, uid)
            else:
                assign(m3, at, 0, uid)
        if op == 9:  # move ref
            p1 = RefOrVal(m1, getnext(uid), uid)
            relptrs[uid] += p1
        if op == 99:  # exit
            print("EXITING", flush=True)
            sys.exit(0)

threads = []
for x in range(50):
    t = threading.Thread(target=main, args=(x,))
    threads.append(t)

for x in range(50):
    threads[x].start()
    print(x)
sleepEvent.set()
#18471 too high!