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
        arguments = args.split(';')
        self.order_id = arguments[0]
        self.valeur = float(arguments[1])
        self.runner = runner
        self.biker = biker
        plateau = runner.map

        rx = int(arguments[2])
        ry = int(arguments[3])
        mx = int(arguments[4])
        my = int(arguments[5])

        array_resto = []
        if plateau[rx - 1][ry] == 'R':
            array_resto.append((rx - 1, ry))
        if plateau[rx + 1][ry] == 'R':
            array_resto.append((rx + 1, ry))
        if plateau[rx][ry - 1] == 'R':
            array_resto.append((rx, ry - 1))
        if plateau[rx][ry + 1] == 'R':
            array_resto.append((rx, ry + 1))
        self.resto_loc = self.array_min(array_resto)

        array_maison = []
        if plateau[mx - 1][my] == 'R':
            array_maison.append((mx - 1, my))
        if plateau[mx + 1][my] == 'R':
            array_maison.append((mx + 1, my))
        if plateau[mx][my - 1] == 'R':
            array_maison.append((mx, my - 1))
        if plateau[mx][my + 1] == 'R':
            array_maison.append((mx, my + 1))
        self.maison_loc = self.array_min(array_maison)

    def __lt__(self, other):
        map_man = MapManager(self.runner.map)
        self_path = map_man.astar_search(self.biker.get_pos(0), self.resto_loc)
        other_path = map_man.astar_search(self.biker.get_pos(0), other.resto_loc)
        return len(self_path) < len(other_path)
