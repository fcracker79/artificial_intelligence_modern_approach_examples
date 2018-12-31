import typing

State = typing.TypeVar('State', bound=typing.Hashable)
Action = typing.TypeVar('Action')
Result = typing.NewType('Result', typing.Dict[State, typing.Dict[Action, State]])
GoalFunction = typing.NewType('GoalFunction', typing.Callable[[State], bool])
ActionsFunction = typing.NewType('ActionsFunction', typing.Callable[[State], typing.Sequence[Action]])
UndoFunction = typing.NewType('UndoFunction', typing.Callable[[State, State, Action], Action])
ResultFunction = typing.NewType('ResultFunction', typing.Callable[[Action, State], State])


class Context:
    def __init__(
            self, result: Result, untried: typing.Dict[State, typing.List[Action]],
            unbacktracked: typing.Dict[State, typing.List[State]],
            previous_state: typing.Optional[State],
            previous_action: typing.Optional[Action]
    ):
        self.result = result
        self.untried = untried
        self.unbacktracked = unbacktracked
        self.previous_state = previous_state
        self.previous_action = previous_action


_STOP = object()


def online_dfs_agent(
        state: State, context: Context,
        goal_function: GoalFunction,
        actions_function: ActionsFunction,
        undo_function: UndoFunction) -> Action:
    if goal_function(state):
        if context.previous_state is not None:
            context.result.setdefault(context.previous_state, {})[context.previous_action] = state
        return _STOP

    if state not in context.untried:
        context.untried[state] = actions_function(state)

    if context.previous_state is not None:
        context.result.setdefault(context.previous_state, {})[context.previous_action] = state
        context.unbacktracked.setdefault(state, []).append(context.previous_state)

    if not len(context.untried.get(state, [])):
        if not context.unbacktracked.get(state):
            return _STOP
        back_state = context.unbacktracked[state].pop()
        previous_action = undo_function(state, back_state, context.previous_action)
    else:
        previous_action = context.untried[state].pop()
    context.previous_action = previous_action
    context.previous_state = state
    return previous_action


def run(
        initial_state: State, goal_function: GoalFunction,
        result_function: ResultFunction,
        actions_function: ActionsFunction,
        undo_function: UndoFunction) -> Result:
    context = Context(Result({}), {}, {}, None, None)

    state = initial_state
    while True:
        action = online_dfs_agent(state, context, goal_function, actions_function, undo_function )
        if action is _STOP:
            break
        state = result_function(action, state)
    return context.result
