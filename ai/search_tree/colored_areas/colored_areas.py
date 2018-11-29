import itertools
import typing

from ai.search_tree.common_types import GenericGraph, ElementType

ColoredArea = typing.NamedTuple(
    'ColoredArea',
    (
        ('area', str),
        ('color', str)
    )
)


class ColoredAreas(GenericGraph[ColoredArea]):
    def __init__(
            self, areas: typing.Sequence[str], colors: typing.Sequence[str]):
        self._areas = areas
        self.colors = colors
        self.adiacencies = {}

    def add_adiacency(self, area1: str, area2: str):
        self.adiacencies.setdefault(area1, set()).add(area2)
        self.adiacencies.setdefault(area2, set()).add(area1)

    def get_children(self, node: ColoredArea) -> typing.Sequence[ColoredArea]:
        return list(
            map(
                lambda d: ColoredArea(d[1], d[0]),
                itertools.product(self.colors, self.adiacencies.get(node.area, set()))
            )
        )

    def get_cost(self, node1: ColoredArea, node2: ColoredArea) -> int:
        return 1

    @property
    def areas_count(self) -> int:
        return len(self._areas)
