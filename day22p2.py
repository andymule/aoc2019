import sys
import os
import math

def dealnew():
    global card, decksize
    card = decksize - card

def cut(n):
    global card, decksize
    card += n
    card %= decksize


def dealinc(n):
    global card, decksize
    if card == 0:
        return
    g = math.floor((card-1)/n)
    g = decksize - g*decksize
    b = card*n-decksize
    c = n*n-decksize
    card = g-(b/c)


ins = []
card = 101741582076661
decksize = 119315717514047

stack = 0
f = open("day22.txt").readlines()
f.reverse()
ii = len(f)

for l in f:
    ii -= 1
    print(ii)
    if "new stack" in l:
        dealnew()
    if "increment" in l:
        ll = l.split()
        ll = ll[-1:][0]
        ll = int(ll)
        dealinc(ll)
    if "cut" in l:
        n = int(l.split()[1])
        cut(n)

# for n in range(decksize):
#     card = n
#     dealinc(3)
#     print("{}:{}",n,card)
print()
print(card)
