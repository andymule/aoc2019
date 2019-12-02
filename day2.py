import math
import sys
import pprint

filepath = "day2.txt"

x = 0
y = 0
words = []

codes = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: lambda a, b: a - b,
    4: lambda a, b: a / b,
    99: lambda a=0, b=0: End(),
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


def runDay2():
    global words
    with open(filepath) as file:
        alldata = file.read().replace("\n", "")
        words = [int(n) for n in alldata.split(",")]
        words[1] = x
        words[2] = y
        it = iter(words)
        while True:
            try:
                op = next(it)
                p1 = words[next(it)]
                p2 = words[next(it)]
                at = next(it)
                words[at] = run(op, p1, p2)
            except Exception as ex:
                return


for x in range(0, 100):
    for y in range(0, 100):
        runDay2()
