import math
import sys
import pprint
import collections

filepath = "day6.txt"
words = []

with open(filepath) as file:
    alldata = file.read().replace("\n", "")
    words = [int(n) for n in alldata.split(",")]
