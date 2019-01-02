import typing

from ai.csp import arc_consistency
from ai.csp.csp_types import VariableAssignment, ConstraintSatisfactionProblem, VariableType, \
    UnassignedVariableSelectionFunction, OrderDomainValueFunction


def _assign_is_complete(assignment: VariableAssignment, variables: typing.Sequence[VariableType]) -> bool:
    return all(assignment.get(v) for v in variables)


def _inference(
    csp: ConstraintSatisfactionProblem,
    variable: VariableType,
    assignment: VariableAssignment
) -> typing.Optional[VariableAssignment]:
    # I might have to undo what _inference does. So I cannot simply apply 'arc_consistency.ac3'
    # as this would reduce the domain. After undoing, I should restore the domain as well, which
    # could be rather annoying.
    # Since I could not find an explicit reference to this problem, I decided to implement this
    # as a copy of the domain and use cs3 just to discover if, upon assignment, I can INFER
    # other singleton values.
    # On the other hand, though, I cannot benefit from domain reduction.
    csp = ConstraintSatisfactionProblem(
        csp.variables, csp.constrained_variables,
        dict(csp.domain), csp.constraints
    )
    for k, v in assignment.items():
        csp.domain[k] = {v}

    queue = []
    for cur_constrained_variables in filter(lambda d: variable in d, csp.constrained_variables):
        cur_queue_element = [variable]
        if variable in cur_constrained_variables:
            cur_queue_element.extend(filter(lambda d: d != variable, cur_constrained_variables))
        queue.append(cur_queue_element)
    if not arc_consistency.ac3(csp, queue):
        return None

    return VariableAssignment(
        {variable: next(iter(variable_values)) for variable, variable_values in csp.domain.items() if len(variable_values) == 1}
    )


def _update_assignment_with_inferences(assignment: VariableAssignment, inferences: VariableAssignment):
    assignment.update(inferences)


def _remove_inferences_from_assignment(assignment: VariableAssignment, inferences: VariableAssignment):
    for k in inferences:
        if k in assignment:
            del assignment[k]


def _backtrack(
        assignment: VariableAssignment, csp: ConstraintSatisfactionProblem,
        get_unassigned_variable: UnassignedVariableSelectionFunction,
        get_order_domain_values: OrderDomainValueFunction)\
        -> typing.Optional[VariableAssignment]:
    if _assign_is_complete(assignment, csp.variables):
        return assignment
    variable_to_assign = get_unassigned_variable(csp, assignment)
    for cur_value in get_order_domain_values(variable_to_assign, assignment, csp):
        assignment[variable_to_assign] = cur_value
        inferences = _inference(csp, variable_to_assign, assignment)
        if inferences is not None:
            # inferences and print(
            #     'I have found {} new inferences, assignments were {}'.format(
            #         len(inferences), len(assignment)
            #     )
            # )
            _update_assignment_with_inferences(assignment, inferences)
            result = _backtrack(assignment, csp, get_unassigned_variable, get_order_domain_values)
            if result is not None:
                return result
            _remove_inferences_from_assignment(assignment, inferences)
    del assignment[variable_to_assign]
    return None


def backtracking_search(
        csp: ConstraintSatisfactionProblem,
        get_unassigned_variable: UnassignedVariableSelectionFunction,
        get_order_domain_values: OrderDomainValueFunction)\
        -> typing.Optional[VariableAssignment]:
    return _backtrack(VariableAssignment({}), csp, get_unassigned_variable, get_order_domain_values)
