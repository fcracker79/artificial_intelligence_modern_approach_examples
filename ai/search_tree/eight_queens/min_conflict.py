import typing

from ai.search_tree.eight_queens.chessboard import Chessboard, CHESSBOARD_SIZE
from ai.search_tree.eight_queens.graph import Queen
from ai.search_tree.print_tools import print_queens


def _get_min_conflicts_pos(i: int, queens: typing.Sequence[Queen], c: Chessboard) -> int:
    conflicts = tuple(
        sum(
            map(
                lambda q: int(c.queens_eat(i, j, q.queen_number, q.position)),
                filter(
                    lambda q: q.queen_number != i,
                    queens
                )
            )
        )
        for j in range(CHESSBOARD_SIZE)
    )

    return min(list(range(len(conflicts))), key=conflicts.__getitem__)


def min_conflict() -> typing.Tuple[typing.Sequence[Queen], int]:
    chessboard = Chessboard()
    queens = [Queen(i, i) for i in range(CHESSBOARD_SIZE)]
    c = 0
    while chessboard.any_queen_eat(list(map(lambda q: q.position, queens))):
        c += 1
        for i in range(len(queens)):
            queens[i] = Queen(
                queens[i].queen_number,
                _get_min_conflicts_pos(i, queens, chessboard))
    return queens, c
