from interactions.game_interaction import GameInteraction

with GameInteraction("localhost", 2121) as runner:
    print(runner('GETMAP'))
