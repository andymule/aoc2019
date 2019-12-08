import math
import sys
import pprint
from collections import defaultdict
import numpy

def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")
# 0 is black, 1 is white, and 2 is transparent.
filepath = "day8.txt"
words = []
layers = []
# image = defaultdict(lambda: defaultdict(lambda: None))
# image=[] # 25 x 6
image = numpy.ones((6,25))
image *= 2
with open(filepath) as file:
	alldata = file.read().replace("\n", "")
	# words = [int(n) for n in alldata]
	
	layersize = 6 * 25
	least0layer = 0
	least0layercount = 100000
	alldatasize = len(alldata)
	for n in range(0,alldatasize-layersize+1, layersize):
		layers.append(alldata[n:n+layersize])
	# layernum = 0
	for n in range(0,len(layers)):
		layer0s = 0 
		for c in layers[n]:
			if c == '0':
				layer0s += 1
		if layer0s < least0layercount:
			least0layercount = layer0s
			least0layer = n
	count1 = 0
	count2 = 0
	for c in layers[least0layer]:
		if c == '1':
			count1 += 1
		if c == '2':
			count2 += 1
	print(str(count1 * count2))

	width=25
	height=6
	for l in layers:
		for y in range(0,height):
			for x in range(0,width):
				newc = l[y*width+x]
				if image[y][x] == 2:
					if newc != 2:
						image[y][x] = newc

matprint(image)
