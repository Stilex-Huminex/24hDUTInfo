from interactions.game_interaction import GameInteraction

with GameInteraction("localhost", 2121) as runner:
    command = ""
    while command != "fin":
        command = input(">> ")
        print(runner(command))
