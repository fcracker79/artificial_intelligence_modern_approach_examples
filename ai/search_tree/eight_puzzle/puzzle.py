import random
import typing

from ai.search_tree.common_types import GenericGraph


class Puzzle:
    _MOVEMENTS = {
        0: (1, 4),
        1: (0, 2, 5),
        2: (1, 6, 3),
        3: (2, 7),
        4: (0, 5, 8),
        5: (1, 4, 6, 9),
        6: (2, 5, 7, 10),
        7: (3, 6, 11),
        8: (4, 9, 12),
        9: (5, 8, 10, 13),
        10: (6, 9, 11, 14),
        11: (7, 10, 15),
        12: (8, 13),
        13: (12, 9, 14),
        14: (10, 13, 15),
        15: (11, 14)
    }

    def __init__(self):
        self.positions = list(range(16))
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
        return list(map(self._new_puzzle, self._MOVEMENTS[self.empty_slot]))

    def __str__(self) -> str:
        result = '_' * 15 + '\n'
        for i in range(4):
            result += '| ' + ' '.join(
                map(lambda d: '{:02}'.format(d) if d > 0 else ' X', self.positions[i * 4: (i + 1) * 4])) + ' |\n'
        result += '-' * 15 + '\n'
        return result

    @property
    def correct(self) -> bool:
        return all((i == d - 1 for i, d in enumerate(self.positions)))

    def __eq__(self, other):
        return self.positions == other.positions

    def __hash__(self):
        return self.empty_slot


class PuzzleGraph(GenericGraph[Puzzle]):
    def __init__(self, root: Puzzle=None):
        self.root = root or Puzzle()

    def get_children(self, node: Puzzle) -> typing.Sequence[Puzzle]:
        def _s(n: Puzzle) -> int:
            return sum(
                map(
                    lambda d: abs(d[0] - d[1] - 1),
                    filter(
                        lambda x: x[1] > 0,
                        enumerate(n.positions)
                    )
                )
            )
        base_heuristic_value = _s(node)
        return sorted(node.get_children(), key=lambda d: _s(d) - base_heuristic_value)

    def get_cost(self, node1: Puzzle, node2: Puzzle) -> int:
        return 1
