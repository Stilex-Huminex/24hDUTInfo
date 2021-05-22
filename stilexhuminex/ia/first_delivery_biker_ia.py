from stilexhuminex.utils.game_interaction import GameInteraction
from stilexhuminex.utils.astar_algorithm import MapManager
from stilexhuminex.utils.biker_interaction import BikerInteraction, BikerStatus


class FirstDeliveryAI:

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

    def move(self, runner, biker):
        runner(f'MOVE|{biker}|' + self.move_from_pos_diff(self.bikerManager.get_pos(0), self.next_move))
        self.bikerManager.move_biker(biker, self.next_move)

    def gen_new_path(self, runner, biker: int, new_status: BikerStatus):
        index = 'client' if new_status == BikerStatus.GOING_TO_CLIENT else 'restaurant'

        (bx, by) = self.bikerManager.get_pos(biker)
        delivery = self.bikerManager.get_deliveries(biker)[0]

        if index == 'client':
            i = (delivery.split(';')[2], delivery.split(';')[3])
        else:
            i = (delivery.split(';')[4], delivery.split(';')[5])

        array = []
        if runner.get_map_pos(i, shift_x=1) == 'R':
            array.append(self.mapManager.astar_search((bx, by), (i[0] + 1, i[1])))
        if runner.get_map_pos(i, shift_x=-1) == 'R':
            array.append(self.mapManager.astar_search((bx, by), (i[0] - 1, i[1])))
        if runner.get_map_pos(i, shift_y=1) == 'R':
            array.append(self.mapManager.astar_search((bx, by), (i[0], i[1] + 1)))
        if runner.get_map_pos(i, shift_y=-1) == 'R':
            array.append(self.mapManager.astar_search((bx, by), (i[0], i[1] - 1)))

        self.bikerManager.set_path(biker, self.array_min(array))
        self.bikerManager.set_status(biker, new_status)

    def run(self):
        with GameInteraction("localhost", 2121) as runner:
            turn = runner.turn
            runner("GETMAP")
            self.mapManager = MapManager(runner.map)
            self.bikerManager = BikerInteraction()

            # Get bikers
            retour = runner("GETBIKERS|" + runner.team_id)
            self.bikerManager.parse_bikers_pos(retour[1])

            commande = runner("GETDELIVERIES")

            while runner.can_play:
                print(self.bikerManager.get_status(0))

                if runner.turn > turn:
                    turn = runner.turn
                    commande = runner("GETDELIVERIES")

                first = commande[1][0]

                if self.bikerManager.get_status(0) == BikerStatus.IDLE:
                    self.bikerManager.take_delivery(0, first)

                # Get the prepared next move
                self.next_move = self.bikerManager.get_next_move(0)
                if self.next_move is None:
                    # If there is none, calculate it
                    self.gen_new_path(runner, 0, BikerStatus.GOING_TO_CLIENT if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT else BikerStatus.GOING_TO_RESTAURANT)
                    self.next_move = self.bikerManager.get_next_move(0)

                # Act on it
                if self.bikerManager.is_arrived(0):
                    d = self.bikerManager.get_deliveries(0)[0]
                    if self.bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT:
                        ret = runner('DELIVER|0|' + d['code'])
                        if ret[0] == "OK":
                            self.bikerManager.set_status(0, BikerStatus.IDLE)
                            self.bikerManager.deliver(0, d)
                    elif self.bikerManager.get_status(0) == BikerStatus.GOING_TO_RESTAURANT:
                        ret = runner('TAKE|0|' + d['code'])
                        if ret[0] == "OK":
                            self.bikerManager.set_status(0, BikerStatus.GOING_TO_CLIENT)
                else:
                    self.move(runner, 0)

    def __call__(self):
        self.run()
