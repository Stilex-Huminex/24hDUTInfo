from interactions.game_interaction import GameInteraction
from random import *

with GameInteraction("localhost", 2121) as runner:
    while True:
        
        d = 8
        while d != 0 :
            n = randint(1,4)
            if n == 1 :
                if print(runner('MOVE|0|R'))[0] == 'OK' :
                    d -= 1
        print(runner('ENDTURN'))
