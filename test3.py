from random import randint
import keyboard, sys, os, time

######### global variables we'll be using all over the places #######
me = '☻'
posX = randint(1,11)
posY = randint(1,5)
elusive_love = '♥'
lovePosX = randint(1,11)
lovePosY = randint(1,5)
money = '$'
moneyPosX = randint(1,11)
moneyPosY = randint(1,5)
total_gold = 0
trap = 'P'
trapPosX = randint(1,11)
trapPosY = randint(1,5)
lives = 3
step_count = 0
mapwidth = 14
MAP = """ ----------- 
|           |
|           |
|           |
|           |
|           |
 -----------
"""


######### we define some functions to call later here #######
def drawThingAt(drawme,y,x,currentmap): #draws whatever you pass it into the preset map
	mypos = mapwidth*y + x	#convert y and x into a single counter from beginning of string
	newmap = list(currentmap) #string can't be altered, so we convert our string to a list
	newmap[mypos] = drawme	# and then we insert our thing into that list
	return "".join(newmap) # force cast the list back into a string and return it to be altered later

def delay_print(s):
    for c in s: # go through all of the characters in the string
        sys.stdout.write(c) #write single char, it normally wouldn't print until newline
        sys.stdout.flush() #forces single char to screen, doesn't wait for newline
        time.sleep(0.15) #artisic pause


# !!! all of your modifications will be below this line ###
# X1) make your character walk around the screen #COMPLETE
# X2) make your character unable to travel thru walls #COMPLETE
# X3) draw the elusive love to the screen #INCOMPLETE i could not figure this out i tried many many things
# X4) when your character enters the same square as elusive_love, you have won the game #COMPLETE
# X5) do something fun to indicate that you have fun the game! #COMPLETE

######### start our program here #######
os.system('cls' if os.name=='nt' else 'clear') #clears screen
delay_print("DUKE GAMES PRESENTS:             ")
delay_print("DUKE IN THE DARK: 2019           ")
while True: #is this just a way to loop endlesslessly thru all this until the sys.exit?
    os.system('cls' if os.name=='nt' else 'clear') #clears screen
    currentmap = drawThingAt(me, posY, posX, MAP)
    moneymap = drawThingAt(money, moneyPosY, moneyPosX, MAP)
    trapmap = drawThingAt(trap, trapPosY, trapPosX, MAP)
    # Lovecurrentmap = drawThingAt(elusive_love, lovePosY, lovePosX, MAP)
    # print elusive love to the screen
    # Lovecurrentmap = drawThingAt(elusive_love,lovePosY,lovePosX,MAP)
    # print(str('%s + %s')) % (moneyPosX,moneyPosY)
    print(currentmap)
    print("Press F1 for help")
    # print(moneymap)
    # print(trapmap) #for debugging
    time.sleep(0.1)
    key = keyboard.read_key()
    if key == 'w' and posY != 1:
        step_count += 1
        posY = posY - 1
        currentmap = drawThingAt(me, posY, posX, MAP)
        print(currentmap)
    if key == 'a' and posX != 1:
        step_count += 1
        posX = posX - 1
        currentmap = drawThingAt(me, posY, posX, MAP)
        print(currentmap)
    if key == 's' and posY != 5:
        step_count += 1
        posY = posY + 1
        currentmap = drawThingAt(me, posY, posX, MAP)
        print(currentmap)
    if key == 'd' and posX != 11:
        step_count += 1
        posX = posX + 1
        currentmap = drawThingAt(me, posY, posX, MAP)
        print(currentmap)
    if key == '0':
        delay_print("bye bye!")
        sys.exit(0)
    if posX == lovePosX and posY == lovePosY:
        lovePosX = randint(1,11)
        lovePosY = randint(1,5)
        lives = lives + 1
        delay_print("you have found elusive love! ")
        if lives == 6:
            delay_print("you win! you found love and money. wow. %s of it AND it only took you %s steps.. " % (total_gold, step_count))
            time.sleep(.7)
            sys.exit(0)
    if posX == moneyPosX and posY == moneyPosY:
        moneyPosX = randint(1,11)
        moneyPosY = randint(1,5)
        moneymap = drawThingAt(money, moneyPosY, moneyPosX, MAP)
        gold = randint(1,200)
        total_gold = gold + total_gold
        delay_print("you have chosen money over love, take %s gold.." % (gold))
    if key == 'i':
        delay_print("you check your purse.. %s gold!" % (total_gold))
        time.sleep(0.3) #EVEN MORE PAUSE
    if posX == trapPosX and posY == trapPosY:
        trapPosX = randint(1,11)
        trapPosY = randint(1,5)        
        lives = lives - 1
        delay_print("you have fallen in a pit! ")
        if lives == 0:
            delay_print("you died in a pit with %s gold after %s steps.." % (total_gold, step_count))
            sys.exit(0)
    if key == 'h':
        if lives >= 3:
            delay_print("you feel great, and you look great too!")
        elif lives == 2:
            delay_print("you have two lives..")
        else: 
            delay_print("you only have one more life..")
    if key == 'f':
        delay_print("you check your fitbit, %s steps.." % (step_count))
    if key == 'f1':
        delay_print("Press I for Inventory \n")
        delay_print("Press H for Health \n")
        delay_print("Press F for Fitbit \n")
        delay_print("Press 0 to Quit")