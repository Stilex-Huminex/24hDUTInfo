

with GameInteraction("localhost", 2121) as runner:
    while True:
        print(runner('ENDTURN'))
