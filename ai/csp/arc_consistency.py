import itertools
import typing

from ai.csp.csp_types import ConstraintSatisfactionProblem, VariableType, VariableAssignment, VariableValue


def _revise(csp: ConstraintSatisfactionProblem, variables: typing.Sequence[VariableType]) -> bool:
    def _assignment(*variable_values: VariableValue) -> VariableAssignment:
        return VariableAssignment({e[0]: e[1] for e in zip(csp.variables, variable_values)})
    values_to_remove = []
    variable_to_refine = variables[0]
    for x in csp.domain[variable_to_refine]:
        if not any(
                c(_assignment(x, *values))
                for values in itertools.product(*(csp.domain[v] for v in variables[1:]))
                for c in csp.constraints):
            values_to_remove.append(x)
    for v in values_to_remove:
        csp.domain[variable_to_refine].remove(v)
    return bool(values_to_remove)


def ac3(csp: ConstraintSatisfactionProblem, queue: typing.List[typing.Sequence[VariableType]]) -> bool:
    while queue:
        cur_variables, queue = queue[0], queue[1:]
        if _revise(csp, cur_variables):
            if not csp.domain[cur_variables[0]]:
                return False
            new_variables_to_recheck = list(filter(lambda d: d != cur_variables, queue))
            queue.extend(new_variables_to_recheck)
    return True
