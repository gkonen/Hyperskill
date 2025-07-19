import random
from unittest import case

name_choice = ("John", "Jack")

good_pencils = False
nb_pencils = 0

print("How many pencils would you like to use:")
while not good_pencils:
    try:
        nb_pencils = int(input())
        if nb_pencils == 0:
            print("The number of pencils should be positive")
        elif nb_pencils < 0:
            raise ValueError
        else:
            good_pencils = True
    except ValueError:
        print("The number of pencils should be numeric")

good_name = False
name = ""
print("Who will be the first ({}, {}):".format(*name_choice))
while not good_name:
    name = input()
    if name not in name_choice:
        print("Choose between {} and {}".format(*name_choice))
    else:
        good_name = True

game = "|" * nb_pencils
turn = 0 if name=="John" else 1

while game:
    print(game)
    print(name_choice[turn] + "'s turn")
    pick = 0
    # Player turn
    if name_choice[turn] == "John":
        good_input = False
        while not good_input:
            try:
                pick = int(input())
                if pick > len(game):
                    print("Too many pencils were taken")
                    raise ValueError
                elif pick <= 0 or pick > 3:
                    raise ValueError
                else:
                    good_input = True
            except ValueError:
                print("Possible values: '1', '2' or '3'")
        game = game[pick:]
    # Bot turn
    else:
        match len(game)%4:
            # case 4, 8, 12, 16, ...
            case 0:
                pick = 3
            case 1:
                pick = 1 if len(game) == 1 else random.randint(1,3)
            # case 2, 6, 10, 14, ...
            case 2:
                pick = 1
            # case 3, 7, 11, 15, ...
            case 3:
                pick = 2
        print(pick)
        game = game[pick:]
    turn = (turn + 1) % 2

print(name_choice[turn] + " won!")

