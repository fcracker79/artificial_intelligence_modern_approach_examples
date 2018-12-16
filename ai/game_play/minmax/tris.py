import typing

from ai.search_tree.common_types import GenericGraph, ElementType, Node

_WIN_SCORE = 9


class TrisState:
    def __init__(self, statuses=None, another_tris_state: 'TrisState'=None):
        if statuses:
            self.statuses = list(statuses)
        elif another_tris_state:
            self.statuses = list(another_tris_state.statuses)
        else:
            self.statuses = [''] * 9
        self._value = self._other_value = None

    def set(self, i: int, j: int, value: str):
        if self.get(i, j):
            raise ValueError
        self.statuses[i * 3 + j] = value

    def get(self, i: int, j: int) -> str:
        return self.statuses[i * 3 + j]

    def i_win(self) -> bool:
        return self.get_value() == _WIN_SCORE

    def you_win(self) -> bool:
        return self.get_other_value() == _WIN_SCORE

    def get_value(self):
        if self._value is None:
            if self.get_other_value() == _WIN_SCORE:
                self._value = 0
            else:
                self._value = self._get_value()
        return self._value

    def get_other_value(self):
        if self._other_value is None:
            self._other_value = self._get_value('x')
        return self._other_value

    def _get_value(self, v: str='o'):
        value = 0
        for i in range(3):
            found_horizontal = found_vertical = 0
            for j in range(3):
                if self.get(i, j) == v:
                    if found_horizontal:
                        value += 1
                    found_horizontal += 1
                elif self.get(i, j):
                    found_horizontal = 0
                    break
            for j in range(3):
                if self.get(j, i) == v:
                    if found_vertical:
                        value += 1
                    found_vertical += 1
                elif self.get(i, j):
                    found_vertical = 0
                    break
            if found_horizontal == 3 or found_vertical == 3:
                return _WIN_SCORE

        found_diag1 = found_diag2 = 0
        for i in range(3):
            if self.get(i, i) == v:
                if found_diag1:
                    value += 1
                found_diag1 += 1
            elif self.get(i, i):
                found_diag1 = 0
                break
        for i in range(3):
            if self.get(i, 2 - i) == v:
                if found_diag2:
                    value += 1
                found_diag2 += 1
            elif self.get(i, 2 - i):
                found_diag2 = 0
                break
        if found_diag1 == 3 or found_diag2 == 3:
            return _WIN_SCORE

        return value

    def __str__(self):
        result = '________\n'
        for i, v in enumerate(self.statuses):
            if i % 3 == 0:
                result += '|'
            result += ' '
            result += self.statuses[i] or ' '
            if (i + 1) % 3 == 0:
                result += '|\n'
        result += '--------\n'
        return result


class TrisGraph(GenericGraph):
    def get_children(self, node: Node) -> typing.Sequence[Node]:
        # we win
        if node.state.get_value() == _WIN_SCORE:
            return []

        if node.depth % 2 == 0:
            value = 'o'
        else:
            value = 'x'
        children = [
            Node(TrisState(another_tris_state=node.state), parent=node, depth=node.depth + 1, cost=node.cost + 1)
            for _ in filter(lambda d: not bool(d), node.state.statuses)
        ]

        children_idx = 0
        for i, v in enumerate(node.state.statuses):
            if not v:
                children[children_idx].state.statuses[i] = value
                children_idx += 1
        return children

    def get_cost(self, node1: ElementType, node2: ElementType) -> int:
        return 1
