import random
import typing

from ai.search_tree.common_types import GenericGraph


_PUZZLE_SIZE = 3
_PUZZLE_TILES_COUNT = _PUZZLE_SIZE ** 2

_MOVEMENTS = {
    2: (
        (1, 2),
        (0, 3),
        (0, 3),
        (1, 2)
    ),
    3: (
        (1, 3),
        (0, 2, 4),
        (1, 5),
        (0, 4, 6),
        (1, 3, 5, 7),
        (2, 4, 8),
        (3, 7),
        (4, 6, 8),
        (5, 7)
    ),
    4: (
        (1, 4),
        (0, 2, 5),
        (1, 6, 3),
        (2, 7),
        (0, 5, 8),
        (1, 4, 6, 9),
        (2, 5, 7, 10),
        (3, 6, 11),
        (4, 9, 12),
        (5, 8, 10, 13),
        (6, 9, 11, 14),
        (7, 10, 15),
        (8, 13),
        (12, 9, 14),
        (10, 13, 15),
        (11, 14)
    )
}


_MOVEMENTS = _MOVEMENTS[_PUZZLE_SIZE]


class Puzzle:
    def __init__(self):
        self.positions = list(range(_PUZZLE_TILES_COUNT))
        random.shuffle(self.positions)
        self.empty_slot = self.positions.index(0)

    def _new_puzzle(self, position_to_move: int) -> 'Puzzle':
        p = Puzzle()
        p.positions = list(self.positions)
        p.empty_slot = self.empty_slot
        p.positions[p.empty_slot], p.positions[position_to_move] = \
            p.positions[position_to_move], p.positions[p.empty_slot]
        p.empty_slot = position_to_move
        return p

    def get_children(self) -> typing.Sequence['Puzzle']:
        return list(map(self._new_puzzle, _MOVEMENTS[self.empty_slot]))

    def __str__(self) -> str:
        corner_size = (_PUZZLE_SIZE + 2) * 2 + _PUZZLE_SIZE - 1
        result = 'Cost: {}\n'.format(self.cost)
        result += '_' * corner_size + '\n'
        for i in range(_PUZZLE_SIZE):
            result += '| ' + ' '.join(
                map(lambda d: '{:02}'.format(d) if d > 0 else ' X', self.positions[i * _PUZZLE_SIZE: (i + 1) * _PUZZLE_SIZE])) + ' |\n'
        result += '-' * corner_size + '\n'
        return result

    @property
    def correct(self) -> bool:
        return all((i == d - 1 or d == 0 for i, d in enumerate(self.positions)))

    def __eq__(self, other):
        return self.positions == other.positions

    def __hash__(self):
        return self.empty_slot

    @property
    def cost(self):
        return sum(
            map(
                lambda d: (
                                  abs(d[0] % _PUZZLE_SIZE - (d[1] - 1) % _PUZZLE_SIZE) +
                                  abs(d[0] // _PUZZLE_SIZE - (d[1] - 1) // _PUZZLE_SIZE)
                          )#  * (_PUZZLE_TILES_COUNT - d[1] + 1)
                ,
                filter(
                    lambda x: x[1] > 0,
                    enumerate(self.positions)
                )
            )
        )


class PuzzleGraph(GenericGraph[Puzzle]):
    def __init__(self, root: Puzzle=None):
        self.root = root or Puzzle()

    def get_children(self, node: Puzzle) -> typing.Sequence[Puzzle]:
        base_heuristic_value = node.cost
        return sorted(node.get_children(), key=lambda d: d.cost - base_heuristic_value)

    def get_cost(self, node1: Puzzle, node2: Puzzle) -> int:
        return 1
