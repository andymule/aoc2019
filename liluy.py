realcommands = []
realcommands.append("L,10,R,8,R,6,R,10")
realcommands.append("L,12,R,8,L,12,L,10")
realcommands.append("R,8,R,6,R,10,L,12")
realcommands.append("R,8,L,12,L,10,R,8")
realcommands.append("R,8,L,10,R,8,R,8")
realcommands.append("L,12,R,8,L,12,L,10")
realcommands.append("R,8,R,6,R,10,L,10")
realcommands.append("R,8,R,8,L,10,R,8")
realcommands.append("R,6,R,10")

for r in realcommands:
    nums = r.split(",")
    s = ""
    s += str(len(nums))
    for n in nums:
        if n.isdigit():
            s+= " "+n
        else:
            s+= " "+str(ord(n))
    print(s)