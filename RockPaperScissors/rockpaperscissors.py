from enum import Enum
import os
import random

class RockPaperScissors(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSOR = "scissors"

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))

    @classmethod
    def get(cls, name):
        if name not in cls.list():
            raise ValueError
        return cls(name)

class GameRelationship:

    class State(Enum):
        WIN = 100
        LOSE = 0
        DRAW = 50

    def __init__(self, options: list = ("rock", "paper","scissors",) ):
        if len(options) % 2 == 0:
            raise ValueError("The number of option must be an odd number.")
        self.relation = tuple(rel for rel in options)
        self.size = len(options)
        self.__edge = (self.size - 1)//2

    def __getitem__(self, item: str):
        return self.relation.index(item)

    def get_winner(self, option: str) -> list[str]:
        """
            Get which option the given options win over, it is the next half option
        :rtype: list[str]
        """
        if option not in self.relation:
            raise ValueError("The given option does not exist.")
        winner_index = [ (self[option] - i) % self.size for i in range(1,self.__edge+1)]
        return list(map(lambda ind: self.relation[ind], winner_index))

    def resolve(self, play_player: str, play_bot: str):
        if play_player not in self.relation:
            raise ValueError("Wrong play from player")
        if play_bot not in self.relation:
            raise ValueError("Wrong play from bot")

        win_case = self.get_winner(play_player)
        if play_player == play_bot:
            return GameRelationship.State.DRAW
        elif play_bot in win_case:
            return GameRelationship.State.WIN
        else:
            return GameRelationship.State.LOSE

    def bot_play(self):
        return random.choice(self.relation)


class Record:

    __FILENAME = "rating.txt"

    def __init__(self, player):
        self.record = {}
        self.__from_files()
        self.current_player = ""
        self.current_score = 0
        self.__init(player)

    def __init(self, player):
        if player in self.record.keys():
            self.current_player = player
            self.current_score = self.record[player]
        else:
            self.record[player] = 0

    def __from_files(self):
        if os.path.isfile(self.__FILENAME):
            with open(self.__FILENAME, "r") as file:
                for line in file:
                    name, score = line.split()
                    self.record[name] = int(score)

    def to_file(self):
        self.record[self.current_player] = self.current_score
        with open(self.__FILENAME, "w") as file:
            self.record = dict(sorted(self.record.items(), key= lambda d: d[0]))
            for key, value in self.record.items():
                file.write(f"{key} {value}\n")

    def add_score(self, value):
        self.current_score += value

COMMAND = {"!exit": lambda _ : print("Bye!"),
           "!rating": lambda rd: print(f"Your ratings: {rd.current_score}") }

if __name__ == '__main__':

    player_name = input("Enter your name: ")
    record = Record(player_name)
    print(f"Hello, {player_name}")

    list_option = input()
    if list_option:
        game = GameRelationship(list_option.split(","))
    else:
        game = GameRelationship()
    print("Okay, let's start")

    command = ""
    while command != "!exit":
        good_input = False
        while not good_input:
            command = input()
            if command in COMMAND.keys():
                good_input = True
            elif command not in game.relation:
                print("Invalid input")
            else:
                good_input = True

        if command in COMMAND.keys():
            COMMAND[command](record)
        else:
            bot_play = game.bot_play()
            state = game.resolve(command, bot_play)
            record.add_score(state.value)
            match state:
                case GameRelationship.State.WIN:
                    print(f"Well done. The computer chose {bot_play} and failed")
                case GameRelationship.State.LOSE:
                    print(f"Sorry, but the computer chose {bot_play}")
                case GameRelationship.State.DRAW:
                    print(f"There is a draw {bot_play}")

    record.to_file()
