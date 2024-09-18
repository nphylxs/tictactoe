from tabulate import tabulate
import re
import cowsay

class Board:
    filled = []
    ttt = {"a": [" ", " ", " "], "b": [" ", " ", " "], "c": [" ", " ", " "]}

    @classmethod
    def cell(cls, cell):
        if matches := re.search(r"^([a,b,c])([1,2,3])$", cell):
            if cell in cls.filled:
                raise TypeError
            else:
                cls.filled.append(cell)
                return matches.groups()
        else:
            raise ValueError

    @classmethod
    def turn(cls, row, column, i):
        if i % 2 == 0:
            cls.ttt[row][int(column) - 1] = "x"
        else:
            cls.ttt[row][int(column) - 1] = "o"


def main():
    board = Board()
    i = 1
    while True:
        try:
            print(currentboard(board.ttt))
            print(player(i))
            move = input("What is your move? ").strip().lower()
            if move == "exit":
                print("Goodbye!")
                break
            row, column = board.cell(move)
        except ValueError:
            print(f"Invalid input. {move} is not a valid cell.")
        except TypeError:
            print(f"{move} has already been filled")
        else:
            board.turn(row, column, i)
            if victorycheck(board.ttt):
                print(f"{currentboard(board.ttt)}")
                cowsay.cow(f"{player(i)} is the winner!")
                break
            i += 1
        if i > 9:
            print(f"{currentboard(board.ttt)}")
            cowsay.cow("The game ends in a draw")
            break


def listmaker(d):
    final = []
    for i in d.keys():
        temp = [a for a in d[i]]
        temp.insert(0, i)
        final.append(temp)
    return final


def player(i):
    if i % 2 == 0:
        return "Player x"
    return "Player o"


def victorycheck(dict):
    # horizontal
    for key in dict.keys():
        if all(element == "o" for element in dict[key]) or all(
            element == "x" for element in dict[key]
        ):
            return True
    # vertical
    for i in range(3):
        if all(dict[key][i] == "o" for key in dict.keys()) or all(
            dict[key][i] == "x" for key in dict.keys()
        ):
            return True
    # diagonal
    first = [dict["a"][0], dict["b"][1], dict["c"][2]]
    second = [dict["a"][2], dict["b"][1], dict["c"][0]]
    if diagonal(first) or diagonal(second):
        return True


def diagonal(l):
    return any(l.count(i) == 3 for i in ["x", "o"])


def currentboard(dict):
    top = [1, 2, 3]
    return tabulate(listmaker(dict), top, tablefmt="grid")


if __name__ == "__main__":
    main()
