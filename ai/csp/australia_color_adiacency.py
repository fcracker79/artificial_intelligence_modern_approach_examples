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
    if not assignment:
        return AustraliaColorAdiacencyVariableType.SA
    min_choices_variable = domain_size = None
    for cur_variable, cur_domain in csp.domain.items():
        if cur_variable in assignment:
            continue
        if min_choices_variable is None or domain_size > len(cur_domain):
            min_choices_variable, domain_size = cur_variable, len(cur_domain)
    return min_choices_variable


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
