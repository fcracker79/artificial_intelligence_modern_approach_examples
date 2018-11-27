import abc
import typing


ElementType = typing.TypeVar('ElementType')


class GenericGraph(typing.Generic[ElementType], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_children(self, node: ElementType) -> typing.Sequence[ElementType]:
        pass

    @abc.abstractmethod
    def get_cost(self, node1: ElementType, node2: ElementType) -> int:
        pass


class Graph(GenericGraph):

    def __init__(self):
        self.arch_count = 0
        self.nodes = set()
        self.archs = dict()  # type: typing.Dict[ElementType, typing.Set[ElementType]]
        self.costs = dict()  # type: typing.Dict[ElementType, int]

    def add_arch(self, node1: ElementType, node2: ElementType, cost: int=1):
        self.arch_count += 1
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.archs.setdefault(node1, set()).add(node2)
        self.archs.setdefault(node2, set()).add(node1)
        self.costs[','.join(sorted((node1, node2)))] = cost

    def get_cost(self, node1: ElementType, node2: ElementType) -> int:
        return self.costs[','.join(map(str, sorted((node1, node2))))]

    def get_children(self, node: ElementType) -> typing.Sequence[ElementType]:
        return self.archs.get(node, [])


Node = typing.NamedTuple(
        'Node',
        (
            ('state', typing.Any),
            ('parent', typing.Optional['Node']),
            # ('operator', 'Boh'),
            ('depth', int),
            ('cost', int),
        )
    )


Solution = typing.NamedTuple(
    'Solution',
    (
        ('nodes', typing.List[Node]),
        ('score', int),
        ('iterations', int)
    )
)

QueuingFunction = typing.NewType(
    'QueuingFunction',
    typing.Callable[[typing.Deque[Node], typing.Sequence[Node]], typing.Deque[Node]]
)
