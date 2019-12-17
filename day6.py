import math
import sys
import pprint
from collections import defaultdict

# A function used by DFS 
def DFSUtil(self, v, visited): 
    # Mark the current node as visited  
    # and print it 
    visited[v] = True
    print(v, end = ' ') 

    # Recur for all the vertices  
    # adjacent to this vertex 
    for i in self.graph[v]: 
        if visited[i] == False: 
            self.DFSUtil(i, visited) 

    # The function to do DFS traversal. It uses 
    # recursive DFSUtil() 
    def DFS(self, v): 
  
        # Mark all the vertices as not visited 
        visited = [False] * (len(self.graph)) 
  
        # Call the recursive helper function  
        # to print DFS traversal 
        self.DFSUtil(v, visited)

filepath = "day6.txt"
RAM = []
relates = defaultdict(lambda:[])
countat = {}
parent = {}
counttotal = -1 #COM doesnt count

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

with open(filepath) as file:
    alldata = file.read() #.replace("\n", "")
    RAM = alldata.split()
    for w in RAM:
        s = w.split(")")
        relates[s[0]].append(s[1])
        parent[s[1]]=s[0]
        counttotal += 1
    queue = relates["COM"].copy()
    level = 1
    while len(queue)>0:
        toqueue = []
        for x in queue:
            countat[x] = level
            toqueue += relates[x]
        queue = toqueue
        level +=1
        counttotal -= 1
    y = parent["YOU"]
    ys = [y]
    yptr = y
    try:
        while yptr:
            ys.append(parent[yptr])
            yptr = parent[yptr]
    except:
        pass
    s = parent["SAN"]
    ss = [s]
    sptr = s
    try:
        while sptr:
            ss.append(parent[sptr])
            sptr = parent[sptr]
    except:
        pass
    print(sum(countat.values()))
    d = list(set(ss).symmetric_difference(set(ys)))
    print(len(d))
        

