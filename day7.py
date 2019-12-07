import math, sys, pprint, itertools, argparse, itertools, threading, time
from collections import defaultdict
import ctypes 
# import stopit

filepath = "day7.txt"


def assign(a, b, words):
    words[b] = a


def output(a, words):
    print(words[a])


codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    # 3: lambda a, b: assign(a,b),
    # 4: lambda a, b=0: output(a),
    # 99: lambda a=0, b=0, c=0: End(),
}


def run(op, a, b):
    return codes[op](a, b)


def RefOrVal(mode, get, words):
    if mode == 0:
        return int(words[get])
    else:
        return int(get)


# 99999 biggest
def runDay5(ins, nodenum, fbphase, words):
    global maxval
    global maxcombo
    global ampval
    global ampstate
    global threads
    global initialvalue
    returnval = 0
    first = True
    it = iter(words)
    while True:
        # 0 == position, 1==immediate
        # Parameters that an instruction writes to will never be in immediate mode.
        try:
            instruct = str(next(it))  # string
            op = int(instruct[-2:])
            m1 = 0
            m2 = 0
            m3 = 0
            if len(instruct) > 2:
                m1 = int(instruct[-3:-2])
            if len(instruct) > 3:
                m2 = int(instruct[-4:-3])
            if len(instruct) > 4:
                m3 = int(instruct[-5:-4])
            if op == 1 or op == 2:
                p1 = RefOrVal(m1, next(it), words)
                p2 = RefOrVal(m2, next(it), words)
                at = int(next(it))
                words[at] = run(op, p1, p2)
            if op == 3:  # assign
                at = int(next(it))
                if nodenum == -1:  #part 1 non feedback
                    words[at] = next(ins)
                else: #feedback mode
                    if first: #set phase first time
                        first = False
                        words[at] = fbphase[nodenum]
                    else:
                        if initialvalue:
                            initialvalue = False
                            words[at] = 0
                        else:
                            lastnode = (5+(nodenum-1))%5
                            if ampval[lastnode] == -1:
                                threading.currentThread().wait()
                            words[at] = ampval[lastnode]
                            ampval[lastnode] = -1
            if op == 4:
                at = int(next(it))
                returnval = int(words[at])
                if nodenum != -1:  # feedback loop mode, part2
                    ampval[nodenum] = returnval
                    nextnode = (nodenum+1)%5
                    if threads[nextnode] == None:
                        threads[nextnode] = threading.Thread(target=runDay5, args=(iter(inputs),nextnode,fbphase,mainwords.copy()))
                        threads[nextnode].start()
                        threading.currentThread().wait()
                    else:
                        threads[nextnode].notify()
                        threading.currentThread().wait()
                else: #part 1
                    print(words[at]) # = run(op, p1, 0)
            if op == 5:
                p1 = RefOrVal(m1, next(it), words)
                p2 = RefOrVal(m2, next(it), words)
                if p1 != 0:
                    it = iter(words[p2:])
            if op == 6:
                p1 = RefOrVal(m1, next(it), words)
                p2 = RefOrVal(m2, next(it), words)
                if p1 == 0:
                    it = iter(words[p2:])
            if op == 7:
                p1 = RefOrVal(m1, next(it), words)
                p2 = RefOrVal(m2, next(it), words)
                at = int(next(it))
                if p1 < p2:
                    words[at] = 1
                else:
                    words[at] = 0
            if op == 8:
                p1 = RefOrVal(m1, next(it), words)
                p2 = RefOrVal(m2, next(it), words)
                at = int(next(it))
                if p1 == p2:
                    words[at] = 1
                else:
                    words[at] = 0
            if op == 99:
                ampstate[nodenum] = 0
                return returnval
                # sys.exit(0)
        except Exception as ex:
            ampstate[nodenum] = 0
            return returnval

mainwords = []
with open(filepath) as file:
    alldata = file.read().replace("\n", "")
    mainwords = [int(n) for n in alldata.split(",")]  # ints

if (False):
    maxval = 0
    maxcombo = ()
    permutes = list(itertools.permutations([0, 1, 2, 3, 4]))
    for setup in permutes:
        currentval = 0
        if setup == (4, 3, 2, 1, 0):
            jk = 69
        for singlesetting in setup:
            inputs = [singlesetting, currentval]
            currentval = runDay5(iter(inputs), -1, mainwords.copy())
        if currentval > maxval:
            maxval = currentval
            maxcombo = setup
    print(maxval)
    print(maxcombo)

maxval = 0
maxcombo = ()
ampval = []
ampstate = []
permutes = list(itertools.permutations([5, 6, 7, 8, 9]))
initialvalue = True #force input ONCE
threads = defaultdict(lambda: None)
for setup in permutes:
    for ampphase in setup:
        ampval = [0, -1,-1,-1,-1]
        ampstate = [1,1,1,1,1]
        if setup == (9, 8, 7, 6, 5):
            jk = 69
        for t in threads.values():
            t.join()
            # for id, thread in threading._active.items(): 
            #     if thread is t: 
            #         thread_id = id
            #         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit)) 
            #         break
        threads.clear()
        inputs = [ampphase, 0]
        threads[0] = threading.Thread(target=runDay5, args=(iter(inputs),0,setup,mainwords.copy()))
        threads[0].start()
        while True:
            if sum(ampstate) == 0:
                break
            time.sleep(.000001)
        if setup == (9, 8, 7, 6, 5):
            jk = 69
        if ampval[4] > maxval:
            maxval = ampval[4]
            maxcombo = setup
print(maxval)
print(maxcombo)
