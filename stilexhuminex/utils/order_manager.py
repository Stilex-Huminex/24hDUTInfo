from stilexhuminex.utils.game_interaction import GameInteraction
from stilexhuminex.utils.astar_algorithm import MapManager
from stilexhuminex.utils.biker_interaction import BikerInteraction


class Order:

    order_id = None
    valeur = None
    resto_loc = None
    maison_loc = None
    validite = None
    runner = None

    def __init__(self, args, runner: GameInteraction, biker: BikerInteraction):
        self.order_id = args[0]
        self.valeur = args[1]
        self.runner = runner
        self.biker = biker
        plateau = runner.map

        rx = args[2]
        ry = args[3]
        mx = args[4]
        my = args[5]
    

        array_resto = []
        if (plateau[rx-1][ry] == 'R'):
            self.resto_loc.append((rx-1, ry))
        if (plateau[rx+1][ry] == 'R'):
            self.resto_loc.append((rx+1, ry))
        if (plateau[rx][ry-1] == 'R'):
            self.resto_loc.append((rx, ry-1))
        if (plateau[rx][ry+1] == 'R'):
            self.resto_loc.append((rx, ry+1))

        array_resto = []
        if (plateau[mx-1][my] == 'R'):
            self.maison_loc.append((mx-1, my))
        if (plateau[mx+1][my] == 'R'):
            self.maison_loc.append((mx+1, my))
        if (plateau[mx][my-1] == 'R'):
            self.maison_loc.append((mx, my-1))
        if (plateau[mx][my+1] == 'R'):
            self.maison_loc.append((mx, my+1))


    def __lt__(self, other):
        mapMan = MapManager(self.runner.map)
        selfPath = mapMan.astar_search(self.biker.get_pos(0) , self.resto_loc)
