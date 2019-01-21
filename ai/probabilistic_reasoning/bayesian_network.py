import typing
import uuid
from functools import reduce

ConditionalProbabilityTable = typing.NewType(
    'ConditionalProbabilityTable',
    typing.Callable[[typing.Sequence['BayesianVariable'], typing.Sequence[bool]], float]
)


BayesianVariableID = typing.NewType('BayesianVariableID', uuid.UUID)


class BayesianVariable:
    def __init__(
            self,
            id:  BayesianVariableID,
            data:  typing.Any,
            parents:  typing.List['BayesianVariable'],
            children:  typing.List['BayesianVariable'],
            conditional_probability_table:  ConditionalProbabilityTable
    ):
        self.id = id
        self.data = data
        self.parents = parents
        self.children = children
        self.conditional_probability_table = conditional_probability_table

    def __eq__(self, other):
        return isinstance(other, BayesianVariable) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


BayesianNetwork = typing.NewType('BayesianNetwork', typing.Sequence[BayesianVariable])


class BayesianNetworkBuilder:
    def __init__(self):
        self._variables = dict()  # type: typing.Dict[uuid.UUID, BayesianVariable]
        self._roots = set()

    def get_variable_by_id(self, variable_id: BayesianVariableID) -> typing.Optional[BayesianVariable]:
        return self._variables.get(variable_id)

    def create_variable(
            self, data: typing.Any,
            conditional_probability_table: ConditionalProbabilityTable) \
            -> BayesianVariableID:
        v = BayesianVariable(
            BayesianVariableID(uuid.uuid4()),
            data,
            [],
            [],
            conditional_probability_table
        )
        self._variables[v.id] = v
        self._roots.add(v.id)
        return v.id

    def add_arrow(self, parent_id: BayesianVariableID, child_id: BayesianVariableID):
        self._variables[parent_id].children.append(self._variables[child_id])
        self._variables[child_id].parents.append(self._variables[parent_id])
        self._roots.discard(child_id)

    def build(self) -> BayesianNetwork:
        return BayesianNetwork([self._variables[i] for i in self._roots])


def probability(states: typing.Dict[BayesianVariable, bool]) -> float:
    terminal_nodes = filter(lambda d: not d.children, states)
    already_include_variables = set()
    return reduce(
        lambda x, y: x * y, map(lambda tn: _probability_node(states, tn, already_include_variables), terminal_nodes)
    )


def _probability_node(
        states: typing.Dict[BayesianVariable, bool], node: BayesianVariable,
        already_included_variables: typing.Set[BayesianVariable]) -> float:
    already_included_variables.add(node)
    p = node.conditional_probability_table(
        node.parents, [states[i] for i in node.parents]
    )
    if not states[node]:
        p = 1 - p
    filtered_parents = tuple(filter(lambda parent: parent not in already_included_variables, node.parents))
    if not filtered_parents:
        return p
    return p * reduce(
        lambda x, y: x * y,
        map(
            lambda parent: _probability_node(states, parent, already_included_variables),
            filtered_parents
        )
    )
