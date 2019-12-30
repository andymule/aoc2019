import sys
import os
import copy

init = """..###
##...
#...#
#.#.#
.#.#."""

# init = """....#
# #..#.
# #.?##
# ..#..
# #...."""

def returngrid(): 
	global init



grid = []
saw = set()
i = 0
for l in init.splitlines():
    grid.append([])
    for c in l:
        grid[i].append(c)
    i += 1


def go():
    global grid
    newgrid = copy.deepcopy(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            count = 0
            if y+1 < 5:
                if grid[y+1][x] == '#':
                    count += 1
            if y-1 >= 0:
                if grid[y-1][x] == '#':
                    count += 1
            if x+1 < 5:
                if grid[y][x+1] == '#':
                    count += 1
            if x-1 >= 0:
                if grid[y][x-1] == '#':
                    count += 1
            if grid[y][x] == '#':
                if count != 1:
                    newgrid[y][x] = '.'
            if grid[y][x] == '.':
                if count == 1 or count == 2:
                    newgrid[y][x] = '#'
    grid = copy.deepcopy(newgrid)


def ppp():
    global grid
    score = 0
    for y in range(len(grid)):
        s = ""
        for x in range(len(grid[y])):
            s += grid[y][x]
            if grid[y][x] == "#":
                score += 2**(y*5+x)
        print(s)
    print(score)
    print()


def store():
    global grid
    s = ""
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            s += grid[y][x]
    if s in saw:
        sys.exit(0)
    else:
        saw.add(s)


for r in range(999999):
    ppp()
    store()
    go()
