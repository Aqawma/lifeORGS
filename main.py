from parsing.commandParse import parseCommand

while True:
    result = parseCommand(input("Enter command: \n"))
    for res in result:
        print(res)
