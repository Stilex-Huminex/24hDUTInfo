from interactions.game_interaction import GameInteraction
from interactions.astar_algorithm import MapManager
from interactions.biker_interaction import BikerInteraction, BikerStatus


def array_min(array):
    mini = array[0]
    for route in array:
        if route is not None:
            if len(route) < len(mini):
                mini = route
    return mini


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


def move(biker):
    runner(f'MOVE|{biker}|' + move_from_pos_diff(bikerManager.get_pos(0), next_move))
    bikerManager.move_biker(biker, next_move)


def gen_new_path(biker: int, new_status: BikerStatus):
    index = 'client' if new_status == BikerStatus.GOING_TO_CLIENT else 'restaurant'

    (bx, by) = bikerManager.get_pos(biker)
    delivery = bikerManager.get_deliveries(biker)[0]

    array = []
    if runner.get_map_pos(delivery[index], shift_x=1) == 'R':
        array.append(mapMan.astar_search((bx, by), (delivery[index][0] + 1, delivery[index][1])))
    if runner.get_map_pos(delivery[index], shift_x=-1) == 'R':
        array.append(mapMan.astar_search((bx, by), (delivery[index][0] - 1, delivery[index][1])))
    if runner.get_map_pos(delivery[index], shift_y=1) == 'R':
        array.append(mapMan.astar_search((bx, by), (delivery[index][0], delivery[index][1] + 1)))
    if runner.get_map_pos(delivery[index], shift_y=-1) == 'R':
        array.append(mapMan.astar_search((bx, by), (delivery[index][0], delivery[index][1] - 1)))

    bikerManager.set_path(biker, array_min(array))
    bikerManager.set_status(biker, new_status)


with GameInteraction("localhost", 2121) as runner:
    turn = runner.turn
    runner("GETMAP")
    mapMan = MapManager(runner.map)
    bikerManager = BikerInteraction()

    # Get bikers
    retour = runner("GETBIKERS|" + runner.team_id)
    bikerManager.parse_bikers_pos(retour[1])

    commande = runner("GETDELIVERIES")

    while runner.can_play:
        # print(bikerManager.get_status(0))

        if runner.turn > turn:
            turn = runner.turn
            commande = runner("GETDELIVERIES")

        first = commande[1][0]

        if bikerManager.get_status(0) == BikerStatus.IDLE:
            bikerManager.take_delivery(0, first)

        # Get the prepared next move
        next_move = bikerManager.get_next_move(0)
        if next_move is None:
            # If there is none, calculate it
            gen_new_path(0, BikerStatus.GOING_TO_CLIENT if bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT else BikerStatus.GOING_TO_RESTAURANT)
            next_move = bikerManager.get_next_move(0)

        # Act on it
        if bikerManager.is_arrived(0):
            d = bikerManager.get_deliveries(0)[0]
            if bikerManager.get_status(0) == BikerStatus.GOING_TO_CLIENT:
                ret = runner('DELIVER|0|' + d['code'])
                if ret[0] == "OK":
                    bikerManager.set_status(0, BikerStatus.IDLE)
                    bikerManager.deliver(0, d)
            elif bikerManager.get_status(0) == BikerStatus.GOING_TO_RESTAURANT:
                ret = runner('TAKE|0|' + d['code'])
                if ret[0] == "OK":
                    bikerManager.set_status(0, BikerStatus.GOING_TO_CLIENT)
        else:
            move(0)
