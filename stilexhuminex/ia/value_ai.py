from stilexhuminex.utils.game_interaction import GameInteraction
from stilexhuminex.utils.astar_algorithm import MapManager
from stilexhuminex.utils.biker_interaction import BikerInteraction, BikerStatus
from stilexhuminex.utils.order_manager import Order


class ValueAI:

    mapManager = None
    bikerManager = None
    next_move = None

    @staticmethod
    def array_min(array):
        mini = array[0]
        for route in array:
            if route is not None:
                if len(route) < len(mini):
                    mini = route
        return mini

    @staticmethod
    def move_from_pos_diff(pos, move):
        if move[0] - pos[0] == -1:
            return 'T'
        elif move[0] - pos[0] == 1:
            return 'B'
        elif move[1] - pos[1] == -1:
            return 'L'
        elif move[1] - pos[1] == 1:
            return 'R'
        return "N"

        
    @staticmethod
    def max_val(array):
        max = array[0]
        for c in array:
            if c.valeur > max.valeur:
                max = c

        return max

    @staticmethod
    def meilleures_commandes(array):
        retour = []
        for i in range(len(array)-4):
            max = soloAI.max_val(array)
            retour.append(max)
            array.remove(max)
        retour.sort()
        return retour

    def move(self, runner, biker):
        runner(f'MOVE|{biker}|' + self.move_from_pos_diff(self.bikerManager.get_pos(0), self.next_move))
        self.bikerManager.move_biker(biker, self.next_move)

    def gen_new_path(self, biker: int, new_status: BikerStatus):

        (bx, by) = self.bikerManager.get_pos(biker)
        delivery = self.bikerManager.get_deliveries(biker)[0]

        pos = delivery.maison_loc if new_status == BikerStatus.GOING_TO_CLIENT else delivery.resto_loc

        self.bikerManager.set_path(biker, self.mapManager.astar_search((bx, by), pos))
        self.bikerManager.set_status(biker, new_status)

    def run(self):
        with GameInteraction("localhost", 2121) as runner:
            turn = runner.turn
            runner("GETMAP")
            self.mapManager = MapManager(runner.map)
            self.bikerManager = BikerInteraction()
            runner("TEAMS")
            runner("ENDTURN")

            # Get bikers
            retour = runner("GETBIKERS|" + runner.team_id)
            self.bikerManager.parse_bikers_pos(retour[1])

            commande = runner("GETDELIVERIES")
            arrayCom = []
            for comm in commande[1]:
                arrayCom.append(Order(comm, runner, self.bikerManager))
            
            if (runner.nbJoueurs == 1):
                arrayCom = soloAI.meilleures_commandes(arrayCom)
                print("Je suis tout seul")
            else:
                arrayCom.sort()
                arrayCom = arrayCom[0:3]
                max = soloAI.max_val(arrayCom)
                arrayCom[0] = max
                print("Je ne suis pas tout seul")


            while runner.can_play:
                print(runner.turn)
                # print(self.bikerManager.get_status(0))

                if runner.turn > turn:
                    turn = runner.turn
                    commande = runner("GETDELIVERIES")
                    arrayCom = []
                    for comm in commande[1]:
                        arrayCom.append(Order(comm, runner, self.bikerManager))

                    if (runner.nbJoueurs == 1):
                        arrayCom = soloAI.meilleures_commandes(arrayCom)
                        print("Je suis tout seul")
                    else:
                        arrayCom.sort()
                        arrayCom = arrayCom[0:3]
                        max = soloAI.max_val(arrayCom)
                        arrayCom[0] = max
                        print("Je ne suis pas tout seul")

                    if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_RESTAURANT:
                        self.bikerManager.deliver(0, self.bikerManager.get_deliveries(0)[0])
                        self.bikerManager.take_delivery(0, arrayCom[0])
                        self.gen_new_path(0, BikerStatus.GOING_TO_RESTAURANT)
                

                if self.bikerManager.get_status(0) == BikerStatus.IDLE:
                    self.bikerManager.take_delivery(0, arrayCom[0])

                # Get the prepared next move
                self.next_move = self.bikerManager.get_next_move(0)
                if self.next_move is None:
                    # If there is none, calculate it
                    self.gen_new_path(0, BikerStatus.GOING_TO_CLIENT if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT else BikerStatus.GOING_TO_RESTAURANT)
                    self.next_move = self.bikerManager.get_next_move(0)

                # Act on it
                if self.bikerManager.is_arrived(0):
                    d = self.bikerManager.get_deliveries(0)[0]
                    if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT:
                        ret = runner('DELIVER|0|' + d.order_id)
                        if ret[0] == "OK":
                            arrayCom.sort()
                            self.bikerManager.set_status(0, BikerStatus.IDLE)   
                            self.bikerManager.deliver(0, d)
                    elif self.bikerManager.get_status(0) == BikerStatus.GOING_TO_RESTAURANT:
                        ret = runner('TAKE|0|' + d.order_id)
                        if ret[0] == "OK":
                            self.bikerManager.set_status(0, BikerStatus.GOING_TO_CLIENT)
                else:
                    self.move(runner, 0)

    def __call__(self):
        self.run()