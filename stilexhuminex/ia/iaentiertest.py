from stilexhuminex.utils.game_interaction import GameInteraction
from stilexhuminex.utils.astar_algorithm import MapManager
from random import *

def min(array):
    mini = array[0]
    for route in array:
        if len(route) < len(mini):
            mini = route
    return mini
def distance(commande,bx,by):
    tab = commande[1][0].split(';')
    dist = []
    dist.append(abs(bx - int(tab[2])) + abs(by - int(tab[3])) + (abs(int(tab[2])) - int(tab[4])) + abs(int(tab[3]) - int(tab[5])))
    dist.append(0)
    print(dist)
    for i in range (1,len(commande)):
        tab = commande[1][i].split(';')
        if abs(bx - int(tab[2])) + abs(by - int(tab[3])) + (abs(int(tab[2])) - int(tab[4])) + abs(int(tab[3]) - int(tab[5])) > dist[1] :
            dist[0] = i
            dist[1] = abs(bx - int(tab[2])) + abs(by - int(tab[3])) + (abs(int(tab[2])) - int(tab[4])) + abs(int(tab[3]) - int(tab[5]))
    return dist[0]




    
with GameInteraction("localhost", 2121) as runner:
    runner("GETMAP")
    mapMan = MapManager(runner.map)

    biker = runner("GETBIKERS|0")
    bx = int(biker[1][0][2])
    by = int(biker[1][0][4])
   

  

    commande = runner("GETDELIVERIES")
    tab = commande[1][distance(commande,bx,by)].split(';')
    code = tab[0]
    
    

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
        print(where)
    
    retour = "yes"
    while retour != "NOK":
        state = runner("TAKE|0|" + code)
        retour = state[0]

    mapMan = MapManager(runner.map)

    array = []
    if (runner.map[int(tab[4])-1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4])-1, int(tab[5]))))
    if (runner.map[int(tab[4])+1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4])+1, int(tab[5]))))
    if (runner.map[int(tab[4])][int(tab[5])-1] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4]), int(tab[5])-1)))
    if (runner.map[int(tab[4])][int(tab[5])+1] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4]), int(tab[5])+1)))

    route = min(array)
    print(route)

    old = where 
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
        print(where)

    retour = "yes"
    while retour != "NOK":
        state = runner("DELIVER|0|" + code)
        retour = state[0]

    runner("GETMAP")
    mapMan = MapManager(runner.map)

    biker = runner("GETBIKERS|0")
    bx = int(biker[1][0][2])
    by = int(biker[1][0][4])
   

  

    commande = runner("GETDELIVERIES")
    tab = commande[1][distance(commande,bx,by)].split(';')
    code = tab[0]
    
    

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
        print(where)
    
    retour = "yes"
    while retour != "NOK":
        state = runner("TAKE|0|" + code)
        retour = state[0]

    mapMan = MapManager(runner.map)

    array = []
    if (runner.map[int(tab[4])-1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4])-1, int(tab[5]))))
    if (runner.map[int(tab[4])+1][int(tab[5])] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4])+1, int(tab[5]))))
    if (runner.map[int(tab[4])][int(tab[5])-1] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4]), int(tab[5])-1)))
    if (runner.map[int(tab[4])][int(tab[5])+1] == 'R'):
        array.append(mapMan.astar_search(where, (int(tab[4]), int(tab[5])+1)))

    route = min(array)
    print(route)

    old = where 
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
        print(where)

    retour = "yes"
    while retour != "NOK":
        state = runner("DELIVER|0|" + code)
        retour = state[0]


    
    
 