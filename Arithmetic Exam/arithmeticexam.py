import random
from enum import Enum

class Arithmetic:

    __operation = {
        "+": lambda a,b : a+b,
        "-": lambda a,b : a-b,
        "*": lambda a,b : a*b,
        "/": lambda a,b : a/b,
    }

    @classmethod
    def parse(cls, string):
        try:
            a, operand, b = string.split()
            a = int(a)
            b = int(b)
        except ValueError:
            pass
        else:
            return cls.__operation[operand](a, b)

class Quiz:

    class DIFFICULTY(Enum):
        SIMPLE = 1
        SQUARE = 2

    menu_difficulty = {
        "1": "simple operations with numbers 2-9",
        "2": "integral squares 11-29"
    }

    def __init__(self, number = 5):
        self.number = number
        self.difficulty = self.menu()

    def menu(self):
        print("Which level do you want? Enter a number:")
        for key, value in self.menu_difficulty.items():
            print(f"{key} - {value}")
        while (n := input() ) not in self.menu_difficulty.keys():
            print("Incorrect fromat.")
        return Quiz.DIFFICULTY(int(n))


    def __good_format(self, entry: str):
        return entry[1:].isdigit() if entry.startswith("-") else entry.isdigit()

    def create_question(self):
        if self.difficulty is Quiz.DIFFICULTY.SIMPLE:
            return self.__create_operation()
        elif self.difficulty is Quiz.DIFFICULTY.SQUARE:
            return self.__create_quadratic()

    def __create_quadratic(self):
        a = random.randint(11, 29)
        return str(a)

    def __create_operation(self):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        operand = random.choice(["+", "-", "*"])
        return f"{a} {operand} {b}"

    def start(self):
        score = 0
        for _ in range(self.number):
            question = self.create_question()
            print(question)

            good_format = False
            value = ""
            while not good_format:
                try:
                    value = input()
                    if not self.__good_format(value):
                        raise ValueError
                except ValueError:
                    print("Incorrect format.")
                else:
                    good_format = True

            response = Arithmetic.parse(question) if self.difficulty is Quiz.DIFFICULTY.SIMPLE else int(question)**2
            if value == str(response):
                score += 1
                print("Right!")
            else:
                print("Wrong!")
        return score

class Record:

    __FILENAME = "results.txt"

    @classmethod
    def save(cls, score, quiz: Quiz):
        name = input("What is your name? \n")
        level = quiz.difficulty.value
        description = quiz.menu_difficulty[str(level)]
        cls.__to_file(f"{name}: {score}/{quiz.number} in level {level} ({description})")
        print(f"The result are saved in \"{cls.__FILENAME}\"")

    @classmethod
    def __to_file(cls, string):
        with open(cls.__FILENAME, "a") as f:
            f.write(string)


if __name__ == "__main__":
    quiz = Quiz()
    score = quiz.start()
    print(f"Your mark is {score}/{quiz.number}. Would you like to save the result? Enter yes or no.")
    response = input()
    if response in ("yes", "Yes", "YES", "y"):
        Record.save(score, quiz)
