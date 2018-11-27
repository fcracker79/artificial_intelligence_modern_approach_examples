import typing

from ai.search_tree.eight_queens.chessboard import CHESSBOARD_SIZE, Chessboard
from ai.search_tree.print_tools import print_queens_positions


class _NoSuchSolutionException(Exception):
    pass


def _incr_queens(q: typing.List[int]):
    for i in range(len(q)):
        if q[i] < len(q) - 1:
            q[i] += 1
            break
        elif i < len(q) - 1:
            q[i] = 0
        else:
            raise _NoSuchSolutionException


def brute_force():
    solutions = set()
    queens = [0 for _ in range(CHESSBOARD_SIZE)]
    chessboard = Chessboard()
    try:
        while True:
            if not chessboard.any_queen_eat(queens):
                s = str(queens)
                if s not in solutions:
                    solutions.add(s)
                    print_queens_positions(queens)
            _incr_queens(queens)
    except _NoSuchSolutionException:
        return solutions
