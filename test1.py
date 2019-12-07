# something about rearranging strings 
# PROMPT: Make output say It's True that 5 people have 10 hands and 10 fingers.

w1 = " people"
w2 = "Modify "
w3 = " me!"
w8 = True
w9 = False
w10 = 5
w11 = 1.5
w12 = "It's "
w13 = " that "
w14 = " have "
w15 = " hands"
w16 = " fingers."
w17 = " and "
w18 = " head!"

people_count = 5
hands_count = 2
fingers_count = 10

# Using only the variables above and modifying just the single print statement below print this sentence:
# It's True that 5 people have 10 hands and 100 fingers.
# You may only use string concatenation, string casting, and multiplication.
print(w2 + w3)

# BONUS
# Using ONLY type casting and the variables aboce (no math, no declaration, etc), print another line that says:
# "and 1 head!"

print (w12 + str(w8) + w13 + str(people_count) + w1 + w14 + str(people_count*hands_count) + w15 + w17 + str(people_count*hands_count*fingers_count) + w16 )
print (w17 + str(int(w11)) + w18)