import collections, sys, os, math

basepattern = [0, 1, 0, -1]
input ="59727310424796235189476878806940387435291429226818921130171187957262146115559932358924341808253400617220924411865224341744614706346865536561788244183609411225788501102400269978290670307147139438239865673058478091682748114942700860895620690690625512670966265975462089087644554004423208369517716075591723905075838513598360188150158989179151879406086757964381549720210763972463291801513250953430219653258827586382953297392567981587028568433943223260723561880121205475323894070000380258122357270847092900809245133752093782889315244091880516672127950518799757198383131025701009960944008679555864631340867924665650332161673274408001712152664733237178121872"

def makepattern(startpattern, shift, limit):
    newpattern = []
    countdown = shift
    while countdown > 0:
        countdown -= 1
        newpattern.append(0)
    index = 1
    while True:
        repeatcount = shift + 1
        while repeatcount > 0:
            repeatcount -= 1
            newpattern.append(startpattern[index])
            if len(newpattern) == limit:
                return newpattern
        repeatcount = shift + 1
        index = (index + 1) % len(startpattern)


def fft(plist, num):
    # pstr = str(pat)
    nstr = str(num)
    total = 0
    for p,n in zip(plist, nstr):
        total += int(p)*int(n)
    return str(total)[-1:]


runtimes = 100
signal = input
while runtimes > 0:
    runtimes -= 1
    numberbuilder = ""
    limit = len(signal)
    for i in range(0, limit):
        plist = makepattern(basepattern, i, limit)
        numberbuilder += fft(plist, signal)
    signal = str(numberbuilder)
    jk = 69
print(signal)