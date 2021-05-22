from interactions.game_interaction import GameInteraction
from interactions.astar_algorithm import MapManager

with GameInteraction("localhost", 2121) as runner:
    runner("GETMAP")
    mapMan = MapManager(runner.map)
    result = mapMan.astar_search((0,0), (30,30))
    print(result)