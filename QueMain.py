from interactions.game_interaction import GameInteraction
from interactions.astar_algorithm import MapManager


def min(array):
    mini = array[0]
    for route in array:
        if route != None:
            if len(route) < len(mini):
                mini = route
    return mini

with GameInteraction("localhost", 2121) as runner:
    runner("GETMAP")
    mapMan = MapManager(runner.map)

    biker = runner("GETBIKERS|0")
    bx = int(biker[1][0][2])
    by = int(biker[1][0][4])
    cx = int(biker[1][1][2])
    cy = int(biker[1][1][4])

    commande = runner("GETDELIVERIES")
    tab = commande[1][0].split(';')
    tabA = tab
    
    codeA = tab[0]

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
    

    old = (bx, by)
    where = (0, 0)
    while len(route) != 0:
        where = route.pop(0)
        if (where[0] - old[0] == -1):
            runner('MOVE|0|T')
        if (where[0] - old[0] == 1):
            runner('MOVE|0|B')
        if (where[1] - old[1] == -1):
            runner('MOVE|0|L')
        if (where[1] - old[1] == 1):
            runner('MOVE|0|R')
        old = where
        
    
    retour = "yes"
    while retour != "NOK":
        state = runner("TAKE|0|" + codeA)
        retour = state[0]

    whereA = where




    mapMan = MapManager(runner.map)

    commande = runner("GETDELIVERIES")
    print("yo")
    print(commande)
    tab = commande[1][1].split(';')
    tabB = tab
    
    codeB = tab[0]

    array = []
    if (runner.map[int(tab[2])-1][int(tab[3])] == 'R'):
        array.append(mapMan.astar_search((cx,cy), (int(tab[2])-1, int(tab[3]))))
    if (runner.map[int(tab[2])+1][int(tab[3])] == 'R'):
        array.append(mapMan.astar_search((cx,cy), (int(tab[2])+1, int(tab[3]))))
    if (runner.map[int(tab[2])][int(tab[3])-1] == 'R'):
        array.append(mapMan.astar_search((cx,cy), (int(tab[2]), int(tab[3])-1)))
    if (runner.map[int(tab[2])][int(tab[3])+1] == 'R'):
        array.append(mapMan.astar_search((cx,cy), (int(tab[2]), int(tab[3])+1)))

    route = min(array)
    print(route)

    old = (cx, cy)
    where = (0, 0)
    while len(route) != 0:
        where = route.pop(0)
        if (where[0] - old[0] == -1):
            runner('MOVE|1|T')
        if (where[0] - old[0] == 1):
            runner('MOVE|1|B')
        if (where[1] - old[1] == -1):
            runner('MOVE|1|L')
        if (where[1] - old[1] == 1):
            runner('MOVE|1|R')
        old = where
        print(where)

    whereB = where
    
    retour = "yes"
    while retour != "NOK":
        state = runner("TAKE|1|" + codeB)
        print(state)
        print(tabB)
        retour = state[0]




    tab = tabA
    mapMan = MapManager(runner.map)

    array = []
    if (runner.map[int(tab[4])-1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(whereA, (int(tab[4])-1, int(tab[5]))))
    if (runner.map[int(tab[4])+1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(whereA, (int(tab[4])+1, int(tab[5]))))
    if (runner.map[int(tab[4])][int(tab[5])-1] == 'R'):
        array.append(mapMan.astar_search(whereA, (int(tab[4]), int(tab[5])-1)))
    if (runner.map[int(tab[4])][int(tab[5])+1] == 'R'):
        array.append(mapMan.astar_search(whereA, (int(tab[4]), int(tab[5])+1)))

    route = min(array)
    

    old = whereA
    where = (0, 0)
    while len(route) != 0:
        where = route.pop(0)
        if (where[0] - old[0] == -1):
            runner('MOVE|0|T')
        if (where[0] - old[0] == 1):
            runner('MOVE|0|B')
        if (where[1] - old[1] == -1):
            runner('MOVE|0|L')
        if (where[1] - old[1] == 1):
            runner('MOVE|0|R')
        old = where


    

    mapMan = MapManager(runner.map)
    tab = tabB

    array = []
    if (runner.map[int(tab[4])-1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(whereB, (int(tab[4])-1, int(tab[5]))))
    if (runner.map[int(tab[4])+1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(whereB, (int(tab[4])+1, int(tab[5]))))
    if (runner.map[int(tab[4])][int(tab[5])-1] == 'R'):
        array.append(mapMan.astar_search(whereB, (int(tab[4]), int(tab[5])-1)))
    if (runner.map[int(tab[4])][int(tab[5])+1] == 'R'):
        array.append(mapMan.astar_search(whereB, (int(tab[4]), int(tab[5])+1)))

    print(array)
    route = min(array)
    print(route)

    old = whereB
    where = (0, 0)
    while len(route) != 0:
        where = route.pop(0)
        if (where[0] - old[0] == -1):
            runner('MOVE|1|T')
        if (where[0] - old[0] == 1):
            runner('MOVE|1|B')
        if (where[1] - old[1] == -1):
            runner('MOVE|1|L')
        if (where[1] - old[1] == 1):
            runner('MOVE|1|R')
        old = where
        print(where)





    print(codeA)
    print(codeB)





    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')
    runner('ENDTURN')

    retour = "yes"
    while retour != "NOK":
        state = runner("DELIVER|0|" + codeA)
        print(state)
        retour = state[0]
        
    retour = "yes"
    while retour != "NOK":
        state = runner("DELIVER|1|" + codeB)
        print(state)
        retour = state[0]

    while True:
        runner('ENDTURN')
