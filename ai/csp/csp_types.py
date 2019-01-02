import typing

VariableType = typing.TypeVar('VariableType')
VariableValue = typing.TypeVar('VariableValue', bound=typing.Hashable)
VariableDomain = typing.NewType('VariableDomain', typing.Set[VariableValue])
Domain = typing.NewType('Domain', typing.Dict[VariableType, VariableDomain])
VariableAssignment = typing.NewType('VariableAssignment', typing.Dict[VariableType, VariableValue])
ConstraintFunction = typing.NewType('ConstraintFunction', typing.Callable[[VariableAssignment], bool])
ConstraintSatisfactionProblem = typing.NamedTuple(
    'ConstraintSatisfactionProblem',
    (
        ('variables', typing.Sequence[VariableType]),
        ('constrained_variables', typing.Sequence[typing.Set[VariableType]]),
        ('domain', Domain),
        ('constraints', typing.Sequence[ConstraintFunction])
    )
)
UnassignedVariableSelectionFunction = typing.Callable[
    [ConstraintSatisfactionProblem, VariableAssignment],
    VariableType
]
OrderDomainValueFunction = typing.Callable[
    [VariableType, VariableAssignment, ConstraintSatisfactionProblem],
    typing.Iterator[VariableValue]
]
