from interactions.game_interaction import GameInteraction
from interactions.astar_algorithm import MapManager


def min(array):
    mini = array[0]
    for route in array:
        if len(route) < len(array):
            mini = route
    return mini

with GameInteraction("localhost", 2121) as runner:
    runner("GETMAP")
    mapMan = MapManager(runner.map)

    biker = runner("GETBIKERS|0")
    bx = int(biker[1][0][2])
    by = int(biker[1][0][4])

    commande = runner("GETDELIVERIES")
    tab = commande[1][0].split(';')
    print(tab)
    code = tab[0]
    print(runner.map[int(tab[2])][int(tab[3])])

    array = []
    if (runner.map[int(tab[2])-1][int(tab[3])] == 'R'):
        array.append(mapMan.astar_search((bx,by), (int(tab[2])-1, int(tab[3]))))
    if (runner.map[int(tab[2])+1][int(tab[3])] == 'R'):
        array.append(mapMan.astar_search((bx,by), (int(tab[2])+1, int(tab[3]))))
    if (runner.map[int(tab[2])][int(tab[3])-1] == 'R'):
        array.append(mapMan.astar_search((bx,by), (int(tab[2]), int(tab[3])-1)))
    if (runner.map[int(tab[2])][int(tab[3])+1] == 'R'):
        array.append(mapMan.astar_search((bx,by), (int(tab[2]), int(tab[3])+1)))

    route = min(array)
    print(route)

    old = (bx, by)
    while len(route) != 0:
        where = route.pop(0)