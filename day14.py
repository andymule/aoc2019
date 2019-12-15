import math, sys, pprint
from collections import defaultdict

reactsDict = defaultdict(lambda: defaultdict(lambda: {}))  # [makes] = {takes: count, takes:count .... }
reactsAmounts = defaultdict(lambda: None)  # {makes: count}
leftovers = defaultdict(lambda: 0)

allData = open("day14.txt").readlines()
for l in allData:
    reacts = l.strip().split(" => ")
    makes = reacts[1].replace(',', '').split()[1]
    makesAmount = int(reacts[1].replace(',', '').split()[0])
    reactsAmounts[makes] = makesAmount
    for r in reacts[0].split(','):  # left
        takes = r.split()[1]
        takesAmount = int(r.split()[0])
        reactsDict[makes][takes] = takesAmount


def findFuel(outputType, outputRequiredAmount):
    global reactsDict, reactsAmounts, globalCounter, leftovers
    while leftovers[outputType] > 0 and outputRequiredAmount > 0:
        outputRequiredAmount -= 1
        leftovers[outputType] -= 1
    outputPerReactionAmount = reactsAmounts[outputType]
    willRunAmount = math.ceil(outputRequiredAmount / outputPerReactionAmount)
    leftovers[outputType] += willRunAmount * outputPerReactionAmount - outputRequiredAmount
    for inputType, inputPerReactionAmount in reactsDict[outputType].items():
        inputAmountWillBeProduced = willRunAmount * inputPerReactionAmount
        if inputType == "ORE":
            globalCounter += inputAmountWillBeProduced
        elif inputAmountWillBeProduced > 0:
            findFuel(inputType, inputAmountWillBeProduced)


globalCounter = 0
findFuel("FUEL", 1)
print(globalCounter)

globalCounter = 0
findFuel("FUEL", 2595245) #did manual binary search haha wow great work USA
print(globalCounter)
