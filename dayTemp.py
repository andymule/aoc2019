import math
import sys
import pprint
from collections import defaultdict

filepath = "day14.txt"
words = []
reacts = defaultdict(lambda: {})
# startingore = 30
with open(filepath) as file:
    alldata = file.read().split()
    for l in alldata:
        print(l.split(" => "))



