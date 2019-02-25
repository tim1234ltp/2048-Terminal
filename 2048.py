import random
import os
import abc
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
        def resolve_row(row: List)->List:
            j = 0
            merged = False
            for i in range(len(row)):
                if row[i] != 0:
                    row[j] = row[i]
                    if i != j:
                        row[i] = 0
                    if not merged and j > 0 and row[j] == row[j - 1]:
                        changed = 1;
                        row[j - 1] *= 2;
                        row[j] = 0;
                        merged = True;
                    else:
                        merged = False;
                        j += 1
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

class AbstractOSFactory(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def create_command(self):
    pass
class ConcreteFactoryWin(AbstractOSFactory):
  def create_command(self):
      return ConcreteCommandWin()
class ConcreteFactoryPosix(AbstractOSFactory):
  def create_command(self):
      return ConcreteCommandPosix()

class AbstractCommand(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def interface_clear_command(self):
      pass
class ConcreteCommandWin(AbstractCommand):
  def interface_clear_command(self):
      os.system("cls")
class ConcreteCommandPosix(AbstractCommand):
  def interface_clear_command(self):
      os.system("clear")

def init_game():
  game = Grid()
  if os.name == "posix":
    return game, ConcreteFactoryPosix().create_command()
  else:
    return game, ConcreteFactoryWin().create_command()

if __name__ == "__main__":
    game, commander = init_game()
    while True:
        if not game.check_finished():
            game.generate_elem()
            print(game)
            game.move()
            commander.interface_clear_command()
            print(game)
            commander.interface_clear_command()
        else:
            print("Game Over")
            exit(0)
