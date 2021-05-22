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

    @staticmethod
    def array_min(array):
        mini = array[0]
        for route in array:
            if route is not None:
                if len(route) < len(mini):
                    mini = route
        return mini

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
        if plateau[rx - 1][ry] == 'R':
            self.resto_loc.append((rx - 1, ry))
        if plateau[rx + 1][ry] == 'R':
            self.resto_loc.append((rx + 1, ry))
        if plateau[rx][ry - 1] == 'R':
            self.resto_loc.append((rx, ry - 1))
        if plateau[rx][ry + 1] == 'R':
            self.resto_loc.append((rx, ry + 1))
        self.resto_loc = self.array_min(array_resto)

        array_maison = []
        if plateau[mx - 1][my] == 'R':
            self.maison_loc.append((mx - 1, my))
        if plateau[mx + 1][my] == 'R':
            self.maison_loc.append((mx + 1, my))
        if plateau[mx][my - 1] == 'R':
            self.maison_loc.append((mx, my - 1))
        if plateau[mx][my + 1] == 'R':
            self.maison_loc.append((mx, my + 1))
        self.maison_loc = self.array_min(array_maison)

    def __lt__(self, other):
        map_man = MapManager(self.runner.map)
        self_path = map_man.astar_search(self.biker.get_pos(0), self.resto_loc)
        other_path = map_man.astar_search(self.biker.get_pos(0), other.resto_loc)
        return len(self_path) < len(other_path)
