from interactions.game_interaction import GameInteraction
from random import *

with GameInteraction("localhost", 2121) as runner:
    while True:
        
       
        runner("GETMAP")
        runner.map[2][4]

        biker = (runner("GETBIKERS|0"))
        biker[1][0]
        bx = int(biker[1][0][2])
        by = int(biker[1][0][4])

        runner.map[bx][by]
        if bx != 30 :
            if runner.map[bx+1][by] == "R" :
                print(runner("MOVE|0|R"))
        if bx != 0 :
            if runner.map[bx-1][by] == "R" :
                print(runner("MOVE|0|L"))
        
        print(runner("ENDTURN"))
        
       
