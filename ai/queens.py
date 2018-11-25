import typing

_CHESS_SIZE = 8


class Chessboard:
    def __init__(self):
        self._chessboard = [[set() for _ in range(_CHESS_SIZE)] for _ in range(_CHESS_SIZE)]
        for i in range(_CHESS_SIZE):
            for j in range(_CHESS_SIZE):
                self._tag(i, j, 'row{}'.format(i))
                self._tag(i, j, 'col{}'.format(j))
                self._tag(i, j, 'diagX{}'.format(i - j))
                self._tag(i, j, 'diagY{}'.format(j + i))

    def _tag(self, i: int, j: int, tag: str):
        self._chessboard[i][j].add(tag)

    def queens_eat(self, i1: int, j1: int, i2: int, j2: int) -> bool:
        return bool(self._chessboard[i1][j1] & self._chessboard[i2][j2])

    def any_queen_eat(self, queens: typing.List[int]):
        for i1, j1 in enumerate(queens):
            for i2, j2 in enumerate(queens):
                if i1 == i2:
                    continue
                if self.queens_eat(i1, j1, i2, j2):
                    return True
        return False


def _incr_queens(q: typing.List[int]):
    for i in range(len(q)):
        if q[i] < len(q) - 1:
            q[i] += 1
            break
        elif i < len(q) - 1:
            q[i] = 0
        else:
            raise ValueError


def _print_queens(queens: typing.List[int]):
    print(' ', '_' * (_CHESS_SIZE * 2 + 1), sep='')
    for i in range(_CHESS_SIZE):
        print(
            '|',
            ' '.join('Q' if queens[i] == j else '*' for j in range(_CHESS_SIZE)),
            '|')
    print(' ', '-' * (_CHESS_SIZE * 2 + 1), '\n', sep='')


if __name__ == '__main__':
    solutions = set()
    queens = [0 for _ in range(_CHESS_SIZE)]
    chessboard = Chessboard()
    while True:
        if not chessboard.any_queen_eat(queens):
            s = str(queens)
            if s not in solutions:
                solutions.add(s)
                _print_queens(queens)
        _incr_queens(queens)
