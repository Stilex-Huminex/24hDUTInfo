from interactions.game_interaction import GameInteraction
from interactions.astar_algorithm import MapManager
from random import *

with GameInteraction("localhost", 2121) as runner:
    runner("GETMAP")
    while True:
        

        biker = (runner("GETBIKERS|0"))
        bx = int(biker[1][0][2])
        by = int(biker[1][0][4])

        
        mapMan = MapManager(runner.map)
        result = mapMan.astar_search((bx,by), (30,30))
        
        
       
        i = 0
        while i != len(result) :
            if result[i][1] == (by-1) :
                print(runner("MOVE|0|B"))
            if result[i][0] == (bx+1) : 
                print(runner("MOVE|0|R"))
            if result[i][0] == (bx-1) :
                print(runner("MOVE|0|L"))
            i = i +1 
            
            
        
       
