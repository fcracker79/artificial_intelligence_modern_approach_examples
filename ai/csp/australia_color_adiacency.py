import enum
import typing

from ai.csp.csp_types import Domain, VariableAssignment, VariableType, ConstraintSatisfactionProblem


@enum.unique
class AustraliaColorAdiacencyVariableType(enum.IntEnum):
    WA = 1
    NT = 2
    Q = 3
    SA = 4
    NSW = 5
    V = 6
    T = 7


@enum.unique
class AustraliaColorVariableValue(enum.IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3


AUSTRALIA_CONSTRAINED_VARIABLES = [
    {AustraliaColorAdiacencyVariableType.WA, AustraliaColorAdiacencyVariableType.NT},
    {AustraliaColorAdiacencyVariableType.WA, AustraliaColorAdiacencyVariableType.SA},
    {AustraliaColorAdiacencyVariableType.NT, AustraliaColorAdiacencyVariableType.SA},
    {AustraliaColorAdiacencyVariableType.NT, AustraliaColorAdiacencyVariableType.Q},
    {AustraliaColorAdiacencyVariableType.SA, AustraliaColorAdiacencyVariableType.Q},
    {AustraliaColorAdiacencyVariableType.Q, AustraliaColorAdiacencyVariableType.NSW},
    {AustraliaColorAdiacencyVariableType.SA, AustraliaColorAdiacencyVariableType.NSW},
    {AustraliaColorAdiacencyVariableType.NSW, AustraliaColorAdiacencyVariableType.V},
    {AustraliaColorAdiacencyVariableType.SA, AustraliaColorAdiacencyVariableType.V}
]

_AUSTRALIA_NUM_CONSTRAINTS = dict()

for s in AUSTRALIA_CONSTRAINED_VARIABLES:
    for v in s:
        _AUSTRALIA_NUM_CONSTRAINTS.setdefault(v, 0)
        _AUSTRALIA_NUM_CONSTRAINTS[v] += len(s) - 1


def create_domain() -> Domain:
    return Domain({v: set(x for x in AustraliaColorVariableValue) for v in AustraliaColorAdiacencyVariableType})


def _constraint_function(assignment: VariableAssignment, constraint: typing.Set[AustraliaColorAdiacencyVariableType]) \
        -> bool:
    colors = set()
    for v in constraint:
        if v in assignment:
            if assignment[v] in colors:
                return False
            colors.add(assignment[v])
    return True


def constraint_function(assignment: VariableAssignment) -> bool:
    return all(_constraint_function(assignment, constraint) for constraint in AUSTRALIA_CONSTRAINED_VARIABLES)


def select_unassigned_variable(csp: ConstraintSatisfactionProblem, assignment: VariableAssignment) -> VariableType:
    unassigned_variables = [v for v in csp.variables if v not in assignment]
    return sorted(unassigned_variables, key=lambda d: _AUSTRALIA_NUM_CONSTRAINTS.get(d, 0), reverse=True)[0]


def get_ordered_values(
        variable_type: AustraliaColorAdiacencyVariableType,
        assignment: VariableAssignment,
        csp: ConstraintSatisfactionProblem) -> typing.Iterable[AustraliaColorAdiacencyVariableType]:

        count_colors = dict()
        for c in assignment.values():
            count_colors.setdefault(c, 0)
            count_colors[c] += 1
        return sorted(AustraliaColorVariableValue, key=lambda d: count_colors.get(d, 0))


def create_csp():
    return ConstraintSatisfactionProblem(
        AustraliaColorAdiacencyVariableType,
        AUSTRALIA_CONSTRAINED_VARIABLES,
        {v: set(AustraliaColorVariableValue) for v in AustraliaColorAdiacencyVariableType},
        [constraint_function]
    )
