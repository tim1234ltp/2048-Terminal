import random
import os
from typing import List

class Grid(object):
    def __init__(self):
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    def check_finished(self):
        for x in self.board:
            for y in x:
                if y == 0:
                    return False
        return True

    def generate_elem(self):
        x, y = random.randrange(4), random.randrange(4)
        while self.board[x][y] != 0:
            x, y = random.randrange(4), random.randrange(4)
        self.board[x][y] = random.randrange(1, 3) * 2

    def move(self):
        def collapse_row(row):
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0

        def shift_elem(row: List):
            j = 0
            for i in range(len(row)):
                if row[i] != 0:

                    row[j] = row[i]
                    if i != j:
                        row[i] = 0
                    j += 1

        def resolve_row(row: List)->List:
            shift_elem(row)
            collapse_row(row)
            shift_elem(row)
            return row

        move = input("> ")
        if move == "a":
            for i in range(4):
                self.board[i] = resolve_row(self.board[i])

        if move == "d":
            for i in range(4):
                self.board[i] = resolve_row(self.board[i][::-1])
                self.board[i] = self.board[i][::-1]

        if move == "w":
            self.board[:] = [list(a) for a in [*zip(*self.board)][::-1]]
            for i in range(4):
                self.board[i] = resolve_row(self.board[i])
            self.board[:] = [list(a) for a in zip(*self.board[::-1])]

        if move == "s":
            self.board[:] = [list(a) for a in zip(*self.board[::-1])]
            for i in range(4):
                self.board[i] = resolve_row(self.board[i])
            self.board[:] = [list(a) for a in [*zip(*self.board)][::-1]]

    def __str__(self):
        result = ""
        for row in self.board:
            result += "+----+----+----+----+\n"
            for col in row:
                result += f"|{col:>4}"
            result += "|\n"
        result += "+----+----+----+----+\n"
        return result


if __name__ == "__main__":
    game = Grid()
    while True:
        if not game.check_finished():
            game.generate_elem()
            print(game)
            game.move()
            os.system('cls')
            print(game)
            os.system("cls")
        else:
            print("Game Over")
            exit(0)
