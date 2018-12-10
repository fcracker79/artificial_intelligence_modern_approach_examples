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


_EXPECTED_POSITIONS = {
    2:  [3, 1, 2, 0],
    3: [4, 0, 1, 2, 5, 8, 7, 6, 3],  # From the book, a bit different
}


def _get_position(i: int) -> typing.Tuple[int, int]:
    return i // _PUZZLE_SIZE, i % _PUZZLE_SIZE


_MOVEMENTS = _MOVEMENTS[_PUZZLE_SIZE]
_EXPECTED_POSITIONS = _EXPECTED_POSITIONS[_PUZZLE_SIZE]


class Puzzle:
    def __init__(self, positions: typing.Sequence[int]=None):
        if positions is None:
            self.positions = list(range(_PUZZLE_TILES_COUNT))
            random.shuffle(self.positions)
        else:
            self.positions = positions
        self.empty_slot = self.positions.index(0)
        self._cost = None
        self._correct = None
        self._str = None
        self._hash = hash(str(self))

    def _new_puzzle(self, position_to_move: int) -> 'Puzzle':
        new_puzzle = Puzzle(positions=list(self.positions))
        new_puzzle.positions[new_puzzle.empty_slot], new_puzzle.positions[position_to_move] = \
            new_puzzle.positions[position_to_move], new_puzzle.positions[new_puzzle.empty_slot]
        new_puzzle.empty_slot = position_to_move
        return new_puzzle

    def get_children(self) -> typing.Sequence['Puzzle']:
        return list(map(self._new_puzzle, _MOVEMENTS[self.empty_slot]))

    def __str__(self) -> str:
        if self._str is None:
            corner_size = (_PUZZLE_SIZE + 2) * 2 + _PUZZLE_SIZE - 1
            self._str = 'Cost: {}\n'.format(self.cost)
            self._str += '_' * corner_size + '\n'
            for i in range(_PUZZLE_SIZE):
                self._str += '| ' + ' '.join(
                    map(lambda d: '{:02}'.format(d) if d > 0 else ' X', self.positions[i * _PUZZLE_SIZE: (i + 1) * _PUZZLE_SIZE])) + ' |\n'
            self._str += '-' * corner_size + '\n'
        return self._str

    @property
    def correct(self) -> bool:
        if self._correct is None:
            self._correct = all((i == d - 1 or d == 0 for i, d in enumerate(self.positions)))
        return self._correct

    def __eq__(self, other):
        return self._hash == other._hash and self.positions == other.positions

    def __hash__(self):
        return self._hash

    @property
    def cost(self):
        if self._cost is not None:
            return self._cost
        self._cost = self.cost_by_distance
        return self._cost

    @property
    def cost_by_distance(self):
        self._cost = 0
        for i, e in enumerate(self.positions):
            if not e:
                continue
            cur_position = _get_position(i)
            expected_position = _get_position(_EXPECTED_POSITIONS[e])
            self._cost += sum(map(lambda d: abs(d[1] - d[0]), zip(cur_position, expected_position)))
        return self._cost

    @property
    def cost_by_nearby_wrong_elements(self):
        cost = 0
        pos = _get_position(self.empty_slot)
        for i in (pos[0], pos[0] - 1, pos[0] + 1):
            if i < 0 or i >= _PUZZLE_SIZE:
                continue
            for j in (pos[1], pos[1] - 1, pos[1] + 1):
                if j < 0 or j >= _PUZZLE_SIZE:
                    continue
                if i == pos[0] and j == pos[1]:
                    continue
                if (i, j) != _get_position(_EXPECTED_POSITIONS[self.positions[i * _PUZZLE_SIZE + j]]):
                    cost += 1
        return cost


class PuzzleGraph(GenericGraph[Puzzle]):
    def __init__(self, root: Puzzle=None):
        self.root = root or Puzzle()

    def get_children(self, node: Puzzle) -> typing.Sequence[Puzzle]:
        return sorted(node.get_children(), key=lambda d: d.cost)

    def get_cost(self, node1: Puzzle, node2: Puzzle) -> int:
        node1_cost = node1.cost
        cost = node2.cost - node1_cost
        return cost > 0 and cost or node1_cost


p = Puzzle()
p.positions = [1, 2, 3, 8, 0, 4, 7, 6, 5]
p.empty_slot = 4
print(p.cost_by_distance)
print(p.cost_by_nearby_wrong_elements)
