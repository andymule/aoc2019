import sys
import os

ins = []
CARDS = [x for x in range(10007)]

f = open("day22.txt").readlines()

def dealnew(deck):
	deck.reverse()
	return deck
	
def cut(deck, n):
	if n < 0:
		n = len(deck) + n
	topcut = deck[0:n]
	bottom = deck[n:]
	return bottom + topcut
	
def dealinc(deck, n):
	newdeck = [None for x in range(len(deck))]
	index = 0
	#d=[]
	#d.pop
	while len(deck) > 0:
		while newdeck[index] != None:
			index += 1
			index %= len(newdeck)
		newdeck[index] = deck[0]
		deck = deck[1:]
		index += n
		index %= len(newdeck)
	return newdeck
	
ii = len(f)
stack=0
for l in f:
	ii-=1
	print(ii)
	if "new stack" in l:
		CARDS = dealnew(CARDS)
	if "increment" in l:
		ll = l.split()
		ll = ll[-1:][0]
		ll = int(ll)
		CARDS = dealinc(CARDS,ll)
	if "cut" in l:
		n = int(l.split()[1])
		CARDS = cut(CARDS,n)


#print(f)
#CARDS = dealnew(CARDS)
#CARDS = cut(CARDS, -4)

#CARDS = dealinc(CARDS, 7)
#CARDS = dealinc(CARDS, 9)
#CARDS = cut(CARDS, -2)
#CARDS = dealnew(CARDS)
#CARDS = dealnew(CARDS)
#print(CARDS)

print(CARDS.index(2019))