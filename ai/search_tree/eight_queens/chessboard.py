import typing

CHESSBOARD_SIZE = 8


class Chessboard:
    def __init__(self):
        self._chessboard = [[set() for _ in range(CHESSBOARD_SIZE)] for _ in range(CHESSBOARD_SIZE)]
        for i in range(CHESSBOARD_SIZE):
            for j in range(CHESSBOARD_SIZE):
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
