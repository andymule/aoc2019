import math
import sys
import pprint

filepath = "day5.txt"

words = []
_input = 5
# def assign(a,b):
#     global words
#     words[b] = a

# def output(a):
#     global words
#     print(words[a])
#     # return words[a]

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    # 3: lambda a, b: assign(a,b),
    # 4: lambda a, b=0: output(a),
    99: lambda a=0, b=0, c=0: End(),
}


def End():
    global words
    if x == 12 and y == 2:
        print("{0}".format(words[0]))
    if words[0] == 19690720:
        print("{0} {1}".format(x, y))
    # sys.exit(0)


def run(op, a, b):
    return codes[op](a, b)

# 99999 biggest
def runDay5():
    global words
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        words = [int(n) for n in alldata.split(",")] #ints
        # words = alldata.split(",") #strings
        it = iter(words)
        # int(str(number)[:2])
        while True:
            # 0 == position, 1==immediate
            # Parameters that an instruction writes to will never be in immediate mode.
            try:
                instruct = str(next(it)) #string
                op = int(instruct[-2:])
                m1=0
                m2=0
                m3=0
                if len(instruct) > 2:
                    m1 = int(instruct[-3:-2])
                if len(instruct) > 3:
                    m2 = int(instruct[-4:-3])
                if len(instruct) > 4:
                    m3 =int(instruct[-5:-4])
                if op==1 or op==2:
                    if m1==0:
                        p1 = int(words[next(it)])
                    else:
                        p1 = int(next(it))
                    if m2==0:
                        p2 = int(words[next(it)])
                    else:
                        p2 = int(next(it))
                    # if m3==0:
                    # at = int(words[next(it)])
                    # else:
                    at = int(next(it))
                    words[at] = run(op, p1, p2)
                if op==3: #assign
                    # if m1==0:
                        # at = int(words[next(it)])
                    # else:
                    at = int(next(it))
                    words[at]= _input
                if op==4:
                    # if m1==0:
                        # at = int(words[next(it)])
                    # else:
                    at = int(next(it))
                    print(words[at]) # = run(op, p1, 0)
                if op==5:
                    if m1==0:
                        p1 = int(words[next(it)])
                    else:
                        p1 = int(next(it))
                    if m2==0:
                        p2 = int(words[next(it)])
                    else:
                        p2 = int(next(it))
                    if p1 != 0:
                        it = iter(words[p2:])
                if op==6:
                    if m1==0:
                        p1 = int(words[next(it)])
                    else:
                        p1 = int(next(it))
                    if m2==0:
                        p2 = int(words[next(it)])
                    else:
                        p2 = int(next(it))
                    if p1 == 0:
                        it = iter(words[p2:])
                if op==7:
                    if m1==0:
                        p1 = int(words[next(it)])
                    else:
                        p1 = int(next(it))
                    if m2==0:
                        p2 = int(words[next(it)])
                    else:
                        p2 = int(next(it))
                    at = int(next(it))
                    if p1 < p2:
                        words[at]=1
                    else:
                        words[at]=0
                if op==8:
                    if m1==0:
                        p1 = int(words[next(it)])
                    else:
                        p1 = int(next(it))
                    if m2==0:
                        p2 = int(words[next(it)])
                    else:
                        p2 = int(next(it))
                    at = int(next(it))
                    if p1 == p2:
                        words[at]=1
                    else:
                        words[at]=0

                if op==99:
                    sys.exit(0)
            except Exception as ex:
                return

runDay5()