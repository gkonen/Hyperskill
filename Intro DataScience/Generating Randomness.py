from dataclasses import dataclass
from itertools import product

MIN_CHAR = 100
MIN_CHAR_TEST = 4

def sanitize(user_input):
    return "".join([c for c in user_input if c in {"0", "1"}])

@dataclass
class Predictor:
    def __init__(self, clean_input):
        self.word = clean_input
        self.counter_triad = { key : [0,0] for key in self._create_triad() }
        self._count_triad()

    def _create_triad(self, list_char = ["0", "1"]):
        for triad in product(list_char, repeat=3):
            yield "".join(triad)

    def _count_triad(self):
        for i in range(len(self.word) - 3):
            triad = self.word[i:i+3]
            count = self.word[i+3]
            self.counter_triad[triad][int(count)] += 1

    def _predict(self, triad):
        majority = self.counter_triad[triad][0] > self.counter_triad[triad][1]
        return "0" if majority else "1"

    def predict_input(self, test_input):
        if len(test_input) <= 3:
            return "", 0
        predictions = ""
        score = 0
        for i in range(len(test_input) - 3):
            triad = test_input[i:i+3]
            test = self._predict(triad)
            predictions += test
            if test == test_input[i+3]:
                score += 1

        return predictions, score

    def play(self):
        account = 1000
        entry = ""
        exit_play= False
        print("You have $1000. Every time the system successfully predicts your next press, you lose $1."
              "\nOtherwise, you earn $1. Print \"enough\" to leave the game. Let's go!\n")
        while account > 0 and not exit_play:
            while len(entry) < MIN_CHAR_TEST:
                print("Print a random string containing 0 or 1:\n")
                entry = input()
                if entry == "enough":
                    exit_play = True
            if not exit_play:
                entry = sanitize(entry)
                predictions, score = self.predict_input(entry)
                print(f"Predictions: {predictions} \n\nComputer guessed {score} out of {len(predictions)} symbols right ({round(score / len(predictions) * 100, 2)} %)")
                account += len(predictions) - 2*score
                print(f"Your balance is now ${account}")
                entry = ""
        print("Game Over!")


if __name__ == "__main__":
    data = ''
    print("Please provide AI some data to learn...")
    print(f"The current data length is {len(data)}, {MIN_CHAR - len(data)} symbols left")
    while len(data) < MIN_CHAR:
        print("Print a random string containing 0 or 1: \n")
        user_input = input()
        data += sanitize(user_input)
        print(f"The current data length is {len(data)}, {MIN_CHAR - len(data)} symbols left")

    print(f"Final data string:\n{data}\n")
    predictor = Predictor(data)
    predictor.play()

