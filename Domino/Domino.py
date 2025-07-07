# region STEP 1

import random

stock_piece = []
computer_piece = []
player_piece = []
domino_snake = []


def initialize():
    """
        Resplenish stock_piece with every domino
    """
    global stock_piece
    for i in range(7):
        for j in range(i, 7):
            if [i, j] not in stock_piece:
                stock_piece.append([i, j])
    random.shuffle(stock_piece)


def distribute():
    """
        Distribute seven dominoes to player and computer
    """
    global stock_piece, computer_piece, player_piece

    for i in range(14):
        if i % 2 == 0:
            player_piece.append(stock_piece.pop())
        else:
            computer_piece.append(stock_piece.pop())


def first_player():
    """
        Decide which is the first player or None
    :return: computer or player or None
    """
    global computer_piece, player_piece
    for i in range(6, 0, -1):
        if [i, i] in computer_piece:
            return "computer", [i,i]
        elif [i, i] in player_piece:
            return "player", [i,i]
    return None


def start_game():
    """
        install everything to begin the game
    """
    global stock_piece, computer_piece, player_piece, domino_snake
    initialize()
    distribute()
    player, domino = first_player()
    next_player = None
    while player is None:
        initialize()
        distribute()
        player, domino = first_player()

    if player == "computer":
        domino_snake.append(domino)
        computer_piece.remove(domino)
        next_player = "player"
    elif player == "player":
        domino_snake.append(domino)
        player_piece.remove(domino)
        next_player = "computer"

    print("Stock pieces:", stock_piece)
    print("Computer pieces:", computer_piece)
    print("Player pieces:", player_piece)
    print("Domino snake:",domino_snake)
    print("Status:", next_player)


if __name__ == "__main__":
    start_game()

# endregion