# Orthello - DYOA at TU Graz WS 2019
# Name:       Fabian Roßmann
# Student ID: 11914778

# STATIC STRINGS - DO NOT CHANGE
import random
import sys

TERMINAL_COLOR_NC = '\033[0m'
TERMINAL_COLOR_1 = '\033[94m'
TERMINAL_COLOR_2 = '\033[92m'
TERMINAL_COLOR_EMPTY = '\033[93m'
TERMINAL_COLOR_ERROR = '\033[91m'

ERROR_INVALID_INPUT = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Invalid Input"
ERROR_NOT_ALLOWED = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Stone is not allowed to be placed here"
ERROR_OCCUPIED = TERMINAL_COLOR_ERROR + "[ERROR]" + TERMINAL_COLOR_NC + " Field already occupied"

PROMPT_HUMAN_AI = "Play against a [human] or an [ai]? "

PROMPT_PLAYER_1 = TERMINAL_COLOR_1 + "player1>" + TERMINAL_COLOR_NC + " "
PROMPT_PLAYER_2 = TERMINAL_COLOR_2 + "player2>" + TERMINAL_COLOR_NC + " "
PROMPT_AI = TERMINAL_COLOR_2 + "ai plays>" + TERMINAL_COLOR_NC + " "

WON_PLAYER_1 = TERMINAL_COLOR_1 + "[player1]" + TERMINAL_COLOR_NC + " has won!"
WON_PLAYER_2 = TERMINAL_COLOR_2 + "[player2]" + TERMINAL_COLOR_NC + " has won!"
WON_DRAW = "It's a " + TERMINAL_COLOR_EMPTY + "[DRAW]" + TERMINAL_COLOR_NC

STATISTICS_1 = "[STATS]" + TERMINAL_COLOR_1 + "[player1]=" + TERMINAL_COLOR_NC
STATISTICS_2 = "[STATS]" + TERMINAL_COLOR_2 + "[player2]=" + TERMINAL_COLOR_NC

INPUT_HUMAN = "human"
INPUT_COMPUTER = "ai"
INPUT_SKIP = "skip"
INPUT_QUIT = "quit"

# END OF STATIC STRINGS

game_field = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


# A function to print boardData provided.
def printBoard(boardData):
    print("\n   ┌───┬───┬───┬───┬───┬───┬───┬───┐")

    row_keys = ["A", "B", "C", "D", "E", "F", "G", "H"]

    row_count = 0

    for row in boardData:
        column_string = " " + row_keys[row_count] + " │";
        for column in row:
            if column == 1:
                column_text = TERMINAL_COLOR_1 + "1" + TERMINAL_COLOR_NC
            elif column == 2:
                column_text = TERMINAL_COLOR_2 + "2" + TERMINAL_COLOR_NC
            else:
                column_text = TERMINAL_COLOR_EMPTY + "0" + TERMINAL_COLOR_NC

            column_string += " " + column_text + " │"
        print(column_string)

        row_count = row_count + 1
        if (row_count < len(boardData)):
            print("   ├───┼───┼───┼───┼───┼───┼───┼───┤")

    print("   └───┴───┴───┴───┴───┴───┴───┴───┘")
    print("     0   1   2   3   4   5   6   7  ")


def getPlayerInput(player):
    if player == 1:
        return input(PROMPT_PLAYER_1)
    elif player == 2:
        return input(PROMPT_PLAYER_2)


def getEnemy(player):
    if player == 1:
        return 2
    return 1


def isCorner(row, col):
    if (row == 0 and col == 0) or (row == 7 and col == 7) or (row == 7 and col == 0) or (row == 0 and col == 7):
        return True
    return False


def isOutOfRange(row, col):
    if row > 7 or row < 0 or col > 7 or col < 0:
        return True
    return False


def isTurnableInDirection(row, col, rStep, wStep, player):
    x = row + rStep
    y = col + wStep
    if rStep == -1:
        rborder = -1
    else:
        rborder = 8

    if wStep == -1:
        wborder = -1
    else:
        wborder = 8

    if wStep == 0:
        for x in range(x, rborder, rStep):
            if game_field[x][y] == 0:
                return False
            if game_field[x][y] == player:
                return True
    elif rStep == 0:
        for y in range(y, wborder, wStep):
            if game_field[x][y] == 0:
                return False
            if game_field[x][y] == player:
                return True
    else:
        for x, y in zip(range(x, rborder, rStep), range(y, wborder, wStep)):
            if game_field[x][y] == 0:
                return False
            if game_field[x][y] == player:
                return True


# TODO: make it more efficent
def isValidMove(row, col, player):
    enemy = getEnemy(player)
    isValidVar = False
    if  game_field[row][col] == 0:
        if not isOutOfRange(row + 1, col + 1) and game_field[row + 1][col + 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, 1, 1, player)

        if not isOutOfRange(row + 1, col - 1) and game_field[row + 1][col - 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, 1, -1, player)

        if not isOutOfRange(row - 1, col + 1) and game_field[row - 1][col + 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, -1, 1, player)

        if not isOutOfRange(row - 1, col - 1) and game_field[row - 1][col - 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, -1, -1, player)

        if not isOutOfRange(row, col + 1) and game_field[row][col + 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, 0, 1, player)

        if not isOutOfRange(row, col - 1) and game_field[row][col - 1] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, 0, -1, player)

        if not isOutOfRange(row + 1, col) and game_field[row + 1][col] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, 1, 0, player)

        if not isOutOfRange(row - 1, col) and game_field[row - 1][col] == enemy:
            isValidVar = isValidVar or isTurnableInDirection(row, col, -1, 0, player)

    return isValidVar


# TODO: make it KISS
def turnStones(row, col, player):
    # N
    x = row - 1
    while True:
        if x < 0:
            break
        if game_field[x][col] == 0:
            break
        if game_field[x][col] == player:
            for x in range(x, row, 1):
                game_field[x][col] = player
            break
        x = x - 1
    # NE
    x = row - 1
    y = col + 1
    while True:
        if x < 0 or y > 7:
            break
        if game_field[x][y] == 0:
            break
        if game_field[x][y] == player:
            for x, y in zip(range(x, row, 1), range(y, col, -1)):
                game_field[x][y] = player
            break
        x = x - 1
        y = y + 1
    # E
    y = col + 1

    while True:
        if y > 7:
            break
        if game_field[row][y] == 0:
            break
        if game_field[row][y] == player:
            for y in range(y, col, -1):
                game_field[row][y] = player
            break
        y = y + 1

    # SE
    x = row + 1
    y = col + 1
    while True:
        if x > 7 or y > 7:
            break
        if game_field[x][y] == 0:
            break
        if game_field[x][y] == player:
            for x, y in zip(range(x, row, -1), range(y, col, -1)):
                game_field[x][y] = player
            break
        x = x + 1
        y = y + 1

    # S
    x = row + 1
    while True:
        if x > 7:
            break
        if game_field[x][col] == 0:
            break
        if game_field[x][col] == player:
            for x in range(x, row, -1):
                game_field[x][col] = player
            break
        x = x + 1
    # SW
    x = row + 1
    y = col - 1
    while True:
        if y < 0 or x > 7:
            break
        if game_field[x][y] == 0:
            break
        if game_field[x][y] == player:
            for x, y in zip(range(x, row, -1), range(y, col, 1)):
                game_field[x][y] = player
            break
        x = x + 1
        y = y - 1
    # W
    y = col - 1
    while True:
        if y < 0:
            break
        if game_field[row][y] == 0:
            break
        if game_field[row][y] == player:
            for y in range(y, col, 1):
                game_field[row][y] = player
            break
        y = y - 1
    # NW
    x = row - 1
    y = col - 1
    while True:
        if x < 0 or y < 0:
            break
        if game_field[x][y] == 0:
            break
        if game_field[x][y] == player:
            for x, y in zip(range(x, row, 1), range(y, col, 1)):
                game_field[x][y] = player
            break
        x = x - 1
        y = y - 1


def setStone(row, col, player):
    if game_field[row][col] == 0:
        if isValidMove(row, col, player):
            game_field[row][col] = player
            turnStones(row, col, player)
            return True
        else:
            print(ERROR_NOT_ALLOWED)
    else:
        print(ERROR_OCCUPIED)
    return False


def isSkippable(player):
    x = 0
    y = 0
    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if isValidMove(x, y, player):
                return False
    return True


def interpretInput(ch, player):
    if len(ch) == 2:
        inputList = list(ch)
        inputList[1] = int(ord(inputList[1]) - 48)
        if isinstance(inputList[0], str) and isinstance(inputList[1], int):
            inputList[0] = ord(inputList[0]) - 65
            inputList = list(map(int, inputList))
            if inputList[0] <= 7 and inputList[1] <= 7:
                return inputList
    if ch == INPUT_QUIT:
        sys.exit(0)
    if ch == INPUT_SKIP:
        if isSkippable(player):
            return -2
    print(ERROR_INVALID_INPUT)
    return -1


def countPlayer(player):
    count = 0
    x = 0
    for x in range(x, 8, 1):
        y = 0
        for y in range(y, 8, 1):
            if game_field[x][y] == player:
                count += 1
    return count


def setAi():
    uInput = ""
    while not (uInput == INPUT_COMPUTER or uInput == INPUT_HUMAN):
        uInput = input(PROMPT_HUMAN_AI)
    if uInput == INPUT_COMPUTER:
        return True
    return False


def getAiInput():
    if isSkippable(2):
        return -2
    row = -1
    col = -1
    while not isValidMove(row, col, 2):
        row = random.randrange(0, 7)
        col = random.randrange(0, 7)

    inputList = [row, col]
    print(PROMPT_AI + chr(65 + row) + str(col))
    return inputList


def main():
    availableFields = 4
    player = 1
    lastInput = 0
    stonePlaced = False
    ai = setAi()
    printBoard(game_field)
    while True:
        if availableFields == 64:
            break
        if player != 2 or not ai:
            inputStr = getPlayerInput(player)
            inputList = interpretInput(inputStr, player)
            if inputList != -1 and inputList != -2:
                stonePlaced = setStone(inputList[0], inputList[1], player)

            while (inputList == -1 or not stonePlaced) and inputList != -2:
                inputStr = getPlayerInput(player)
                inputList = interpretInput(inputStr, player)
                if inputList != -1 and inputList != -2:
                    stonePlaced = setStone(inputList[0], inputList[1], player)
        else:
            inputList = getAiInput()
            if inputList != -2:
                stonePlaced = setStone(inputList[0], inputList[1], 2)

        if stonePlaced:
            availableFields += 1

        stonePlaced = False
        printBoard(game_field)
        if player == 1:
            player += 1
        else:
            player -= 1

        if lastInput == -2 and inputList == -2:
            break
        lastInput = inputList

    player1Points = countPlayer(1)
    player2Points = countPlayer(2)
    print(STATISTICS_1 + str(player1Points))
    print(STATISTICS_2 + str(player2Points))
    if player1Points > player2Points:
        print(WON_PLAYER_1)
        sys.exit(1)
    elif player1Points < player2Points:
        print(WON_PLAYER_2)
        sys.exit(2)
    else:
        print(WON_DRAW)
        sys.exit(3)


if __name__ == "__main__":
    main()
