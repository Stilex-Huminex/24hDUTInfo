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
        max_ = array[0]
        for c in array:
            if c.valeur > max_.valeur:
                max_ = c

        return max_

    @staticmethod
    def meilleures_commandes(array):
        retour = []
        for i in range(len(array) - 4):
            max_ = ValueAI.max_val(array)
            retour.append(max_)
            array.remove(max_)
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
            runner.end_turn()

            # Get bikers
            retour = runner("GETBIKERS|" + runner.team_id)
            self.bikerManager.parse_bikers_pos(retour[1])

            commande = runner("GETDELIVERIES")
            array_com = []
            for comm in commande[1]:
                array_com.append(Order(comm, runner, self.bikerManager))

            if runner.nbJoueurs == 1:
                array_com = ValueAI.meilleures_commandes(array_com)
            else:
                array_com.sort()
                if (len(array_com) > 3):
                    array_com = array_com[0:3]
                max_ = ValueAI.max_val(array_com)
                array_com[0] = max_

            while runner.can_play:
                print(runner.turn)
                # print(self.bikerManager.get_status(0))

                if runner.turn > turn:
                    turn = runner.turn
                    commande = runner("GETDELIVERIES")
                    array_com = []
                    for comm in commande[1]:
                        array_com.append(Order(comm, runner, self.bikerManager))

                    if runner.nbJoueurs == 1:
                        array_com = ValueAI.meilleures_commandes(array_com)
                        print("Je suis tout seul")
                    else:
                        array_com.sort()
                        if (len(array_com) > 3):
                            array_com = array_com[0:3]
                        max_ = ValueAI.max_val(array_com)
                        array_com[0] = max_

                    if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_RESTAURANT:
                        self.bikerManager.deliver(0, self.bikerManager.get_deliveries(0)[0])
                        self.bikerManager.take_delivery(0, array_com[0])
                        self.gen_new_path(0, BikerStatus.GOING_TO_RESTAURANT)

                if self.bikerManager.get_status(0) == BikerStatus.IDLE:
                    self.bikerManager.take_delivery(0, array_com[0])

                # Get the prepared next move
                self.next_move = self.bikerManager.get_next_move(0)
                if self.next_move is None:
                    # If there is none, calculate it
                    self.gen_new_path(0, BikerStatus.GOING_TO_CLIENT if self.bikerManager.get_status(
                        0) == BikerStatus.GOING_TO_CLIENT else BikerStatus.GOING_TO_RESTAURANT)
                    self.next_move = self.bikerManager.get_next_move(0)

                # Act on it
                if self.bikerManager.is_arrived(0):
                    d = self.bikerManager.get_deliveries(0)[0]
                    if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT:
                        ret = runner('DELIVER|0|' + d.order_id)
                        if ret[0] == "OK":
                            array_com.sort()
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
