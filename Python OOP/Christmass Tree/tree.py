
DEFAULT_CASE = " "
STAR = "X"
SUMMIT = "^"
LEFT_BORDER = "/"
RIGHT_BORDER = "\\"
PINE = "*"
DECORATION = "O"
POT = "|"

def tree(height: int, space: int):

    middle = height
    width = 2 * height - 1
    tree_tab = [list(DEFAULT_CASE * width) for _ in range(height + 2)]  # we add the star and the trunc
    decoration = 0
    # we put the star in the middle and complete with space
    tree_tab[0] = list(DEFAULT_CASE * (middle - 1) + STAR + DEFAULT_CASE * (middle - 1))
    # first height with the pic in the middle
    tree_tab[1] = list(DEFAULT_CASE * (middle - 1) + SUMMIT + DEFAULT_CASE * (middle - 1))
    for i in range(2, height + 1):
        cpt = 0
        # we begin with i=2 so we substract 1 to get the current height
        # middle is the value, we substract 1 to get the index
        frontier_left = (middle - 1) - (i - 1)
        frontier_right = (middle - 1) + (i - 1)
        for j in range(width):
            if j < frontier_left or j > frontier_right:
                tree_tab[i][j] = DEFAULT_CASE
            elif j == frontier_left:
                tree_tab[i][j] = LEFT_BORDER
            elif j == frontier_right:
                tree_tab[i][j] = RIGHT_BORDER
            else:
                if cpt % 2 == 0:
                    tree_tab[i][j] = PINE
                else:
                    if decoration % space == 0:
                        tree_tab[i][j] = DECORATION
                    else:
                        tree_tab[i][j] = PINE
                    decoration += 1
                cpt += 1
    tree_tab[-1] = list(DEFAULT_CASE * (middle - 2) + POT + DEFAULT_CASE + POT + DEFAULT_CASE * (middle - 2))
    return tree_tab


class Postcard:

    def __init__(self, height: int = 30, width: int = 50):
        self.height = height
        self.width = width
        self.postcard = []
        self._init()

    def _init(self):
        for i in range(self.height):
            if i == 0 or i == self.height - 1:
                self.postcard.append(["-" for _ in range(self.width)])
            else:
                self.postcard.append(
                    ["|" if j == 0 or j == self.width - 1 else DEFAULT_CASE for j in range(self.width)])

    def place(self, line: int, column: int, molecule: list):
        height_molecule = len(molecule)
        width_molecule = len(molecule[0])
        offset_line = line
        offset_column = column - (width_molecule // 2 if width_molecule % 2 == 0 else (width_molecule - 1) // 2)
        for i in range(offset_line, offset_line + height_molecule):
            for j in range(offset_column, offset_column + width_molecule):
                if molecule[i - offset_line][j - offset_column] != DEFAULT_CASE:
                    self.postcard[i][j] = molecule[i - offset_line][j - offset_column]

    def __str__(self):
        message = ""
        for index in range(len(self.postcard)):
            line = self.postcard[index]
            if index != self.height - 1:
                message += "".join(line) + "\n"
            else:
                message += "".join(line)
        return message


if __name__ == "__main__":
    card = Postcard()
    args = input().split()
    if len(args) == 2:
        mol = tree(int(args[0]), int(args[1]))
        for line in mol:
            print("".join(line))
    elif len(args) % 4 == 0:
        for i in range(0, len(args), 4):
            height = int(args[i])
            interval = int(args[i + 1])
            line = int(args[i + 2])
            column = int(args[i + 3])
            molecule = tree(height, interval)
            card.place(line, column, molecule)
        molecule = ["Merry Xmas"]
        card.place(27, card.width // 2, molecule)
        print(card)
    else:
        print("bad input")
