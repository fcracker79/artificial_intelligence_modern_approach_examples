import itertools
import random
import typing
import uuid
from functools import reduce


ParentVariables = typing.NewType('ParentVariables', typing.Sequence['BayesianVariable'])
ParentVariableStates = typing.NewType('ParentVariableStates', typing.Sequence[bool])
ConditionalProbabilityTable = typing.NewType(
    'ConditionalProbabilityTable',
    typing.Callable[[ParentVariables, ParentVariableStates], float]
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

    def __str__(self):
        return '{}({})'.format(self.data, self.id)

    def __repr__(self):
        return str(self)


SamplingFunction = typing.NewType(
    'SamplingFunction', typing.Callable[[BayesianVariable], bool])

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


def single_variable_probability(
        hidden_variables: typing.Sequence[BayesianVariable],
        *variable: BayesianVariable
) -> float:
    return multivariable_with_hidden_probability(hidden_variables, {v: True for v in variable})


def single_variable_negative_probability(
        hidden_variables: typing.Sequence[BayesianVariable],
        *variable: BayesianVariable
) -> float:
    return multivariable_with_hidden_probability(hidden_variables, {v: False for v in variable})


def multivariable_with_hidden_probability(
        hidden_variables: typing.Sequence[BayesianVariable],
        known_variables: typing.Dict[BayesianVariable, bool]
) -> float:
    def _f(i: int):
        all_statuses = {v: bool(i & (1 << k)) for k, v in enumerate(hidden_variables)}
        for v, b in known_variables.items():
            all_statuses[v] = b
        return probability(all_statuses)

    return sum(map(_f, range(2 ** len(hidden_variables))))


def get_markov_blanket(variable: BayesianVariable) -> typing.Iterator[BayesianVariable]:
    return itertools.chain(
        variable.children, variable.parents,
        set(
            filter(
                lambda d: d != variable,
                itertools.chain(*map(lambda d: d.parents, variable.children))
            )
        )
    )


def _simple_sampling_function(
        v: BayesianVariable,
        parent_variable_states: ParentVariableStates) -> bool:
    return random.uniform(0, 1) <= v.conditional_probability_table(v.parents, parent_variable_states)


_DEFAULT_SAMPLE = 10000


def _generate_sample(
        *variables: BayesianVariable,
        evidence: typing.Optional[typing.Dict[BayesianVariable, bool]]=None,
        sampling_function: SamplingFunction=_simple_sampling_function,
        result: typing.Optional[typing.Dict[BayesianVariable, bool]]=None
) -> typing.Dict[BayesianVariable, bool]:
    if evidence is None:
        evidence = {}
    if result is None:
        result = {**evidence}
    for variable in variables:
        if variable in result:
            continue
        for v in variable.parents:
            if v not in result:
                _generate_sample(v, evidence=evidence, sampling_function=sampling_function, result=result)
        result[variable] = sampling_function(variable, [result[p] for p in variable.parents])
        _generate_sample(*variable.children, evidence=evidence, sampling_function=sampling_function, result=result)
    return result


def rejection_sampling(
        variable: BayesianVariable, preconditions: typing.Dict[BayesianVariable, bool],
        network: BayesianNetwork,
        sampling_function: SamplingFunction=_simple_sampling_function,
        samples: int=_DEFAULT_SAMPLE
):
    valid_samples = 0
    for sample in (_generate_sample(*network, sampling_function=sampling_function) for _ in range(samples)):
        # Here we skip all the samples that are not compliant with evidence
        if not sample[variable] or not all(preconditions[v] == sample[v] for v in preconditions):
            continue
        valid_samples += 1
    return valid_samples / samples


def _weighted_sample(
        network: BayesianNetwork, evidence: typing.Dict[BayesianVariable, bool],
        sampling_function: SamplingFunction=_simple_sampling_function):
    def _prob(variable: BayesianVariable, all_variables: typing.Dict[BayesianVariable, bool]):
        w = variable.conditional_probability_table(
            variable.parents, [all_variables[p] for p in variable.parents]
        )
        if not all_variables[variable]:
            w = 1 - w
        return w

    sample = _generate_sample(
        *network, evidence=evidence, sampling_function=sampling_function
    )
    w = reduce(
        lambda a, b: a * b,
        (_prob(e, sample) for e in evidence)
    )
    return sample, w


def likelihood_weighting(
        variable: BayesianVariable, preconditions: typing.Dict[BayesianVariable, bool],
        network: BayesianNetwork,
        sampling_function: SamplingFunction=_simple_sampling_function,
        samples: int=_DEFAULT_SAMPLE
):
    true_samples = false_samples = 0
    for sample, w in (
            _weighted_sample(network, preconditions, sampling_function=sampling_function)
            for _ in range(samples)):
        true_samples += sample[variable] * w
        false_samples += (not sample[variable]) * w
    return true_samples / (true_samples + false_samples)
