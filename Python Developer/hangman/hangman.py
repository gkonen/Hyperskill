import random
from enum import Enum

class GameState(Enum):
    WON = 1
    LOST = 2

class Hangman:

    list_word = ["python", "java", "swift", "javascript"]

    def __init__(self):
        self.secret_word = random.choice(self.list_word)
        self.found_letters = ["-" for _ in self.secret_word]
        self.given_letters = set()
        self.attempts = 8

    def discover_letter(self, letter: str):
        found = False
        for i, word_letter in enumerate(self.secret_word):
            if word_letter == letter:
                self.found_letters[i] = letter
                found = True
        return found

    def play(self):
        while self.attempts > 0 and "-" in self.found_letters:
            print("".join(self.found_letters))
            try:
                guess = input(f"Input a letter: ")
                if len(guess) != 1:
                    raise ValueError
                if not guess.isalpha() or not guess.islower():
                    raise TypeError
                if guess in self.given_letters:
                    raise AttributeError
            except ValueError:
                print("Please, input a single letter.")
                continue
            except TypeError:
                print("Please, enter a lowercase letter from the English alphabet.")
                continue
            except AttributeError:
                print("You've already guessed this letter.")
                continue
            else:
                good_guess = self.discover_letter(guess)
                if not good_guess:
                    print("That letter doesn't appear in the word.")
                    self.attempts -= 1

                self.given_letters.add(guess)
                print()

        if self.attempts == 0:
            print("You lost!")
            return GameState.LOST
        else:
            print(f"You guessed the word {self.secret_word}!")
            print("You survived!")
            return GameState.WON

class Menu:
    def __init__(self):
        self.result = { GameState.WON : 0, GameState.LOST : 0 }

    def show_menu(self):
        print("H A N G M A N")
        while True:
            option = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')
            match option:
                case "play":
                    game = Hangman()
                    game_state = game.play()
                    self.result[game_state] += 1
                case "results":
                    print(f"You won: {self.result[GameState.WON]} times.\nYou lost: {self.result[GameState.LOST]} times")
                case "exit":
                    exit()
                case _:
                    print("Invalid option. Please, try again.")

if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()