import itertools
import typing

State = typing.TypeVar('State')
Action = typing.TypeVar('Action')

UnconditionalSubplan = typing.NewType('UnconditionalSubplan', typing.Sequence[Action])
ConditionalSubplan = typing.NamedTuple(
    'ConditionalSubplan',
    (
        ('state', State),
        ('subplan', 'Plan')
    )
)

Plan = typing.NewType('Plan', typing.Sequence[typing.Union[UnconditionalSubplan, ConditionalSubplan]])

GoalTestFunction = typing.NewType('GoalTestFunction',  typing.Callable[[State], bool])
ResultsFunction = typing.NewType('StatesFunction', typing.Callable[[State, Action], typing.Sequence[State]])
ActionsFunction = typing.NewType('ActionsFunction', typing.Callable[[State], typing.Sequence[Action]])


_FAILURE = None


def or_search(
        state: State,
        goal_test_function: GoalTestFunction,
        results_function: ResultsFunction,
        actions_function: ActionsFunction,
        path: typing.Sequence[State]=tuple()
) -> typing.Optional[Plan]:
    if goal_test_function(state):
        return Plan([])
    if state in path:
        return _FAILURE
    for action in actions_function(state):
        plan = _and_search(
            results_function(state, action), goal_test_function, results_function, actions_function,
            list(itertools.chain((state, ), path)))
        if plan is not _FAILURE:
            return Plan(list(itertools.chain((action, ), plan)))
    return _FAILURE


def _and_search(
        possible_states: typing.Sequence[State],
        goal_test_function: GoalTestFunction,
        results_function: ResultsFunction,
        actions_function: ActionsFunction,
        path: typing.Sequence[State]
) -> typing.Optional[Plan]:
    subplans = []
    for state in possible_states:
        plan = or_search(state, goal_test_function, results_function, actions_function, path)
        if plan is _FAILURE:
            return _FAILURE
        subplans.append(ConditionalSubplan(state, plan))
    return Plan(subplans)
