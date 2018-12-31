"""
Simple tiles with some obstacles and a partial view of the environment.
In this example, we just know:
1. Which direction we can go
2. How far we are from the target

The second point is the key element to avoid loops: the function `simple_tiles_actions_function`
takes just the state as argument and should return all the possible actions, included the
one that would take the agent back to the previous state, which would cause the depth-first
path partially skipped, as:
1. Given a state S1, do action A and move to S2
2. From S2, do action B and move back to S1

The A action has not been explored completely, but we will never get back there as we decided
to move back and to S1, where we will evaluate other actions but A.

Alternatively, the agent should keep track of all its previous statuses, but this is out of topic.
"""


import enum
import typing

SimpleTilesState = typing.NamedTuple(
    'SimpleTilesState',
    (
        ('up_blocked', bool),
        ('down_blocked', bool),
        ('left_blocked', bool),
        ('right_blocked', bool),
        ('hidden_row', int),
        ('hidden_col', int)
    )
)


class SimpleTilesAction(enum.IntEnum):
    GO_LEFT = 0
    GO_RIGHT = 1
    GO_UP = 2
    GO_DOWN = 3


def simple_tiles_goal_function(state: SimpleTilesState) -> bool:
    return 1 == state.hidden_row == state.hidden_col


# The agent can only see which directions are clear.
# Unfortunately, since it does not know anything else but that about the environment,
# it could end up in a loop.
# In order to avoid that, we suppose that the agent can choose the action based on the
# distance from the target, thus actions are sorted.
_ACTIONS = {
    (1, 1): [],  # Here I win
    (1, 2): [SimpleTilesAction.GO_LEFT, SimpleTilesAction.GO_RIGHT, SimpleTilesAction.GO_UP][::-1],
    (1, 3): [SimpleTilesAction.GO_LEFT, SimpleTilesAction.GO_UP][::-1],
    (2, 1): [SimpleTilesAction.GO_DOWN][::-1],
    (2, 2): [SimpleTilesAction.GO_DOWN, SimpleTilesAction.GO_UP][::-1],
    (2, 3): [SimpleTilesAction.GO_DOWN, SimpleTilesAction.GO_UP][::-1],
    (3, 1): [SimpleTilesAction.GO_RIGHT][::-1],
    (3, 2): [SimpleTilesAction.GO_DOWN, SimpleTilesAction.GO_LEFT][::-1],
    (3, 3): [SimpleTilesAction.GO_DOWN][::-1]
}


def _status_from_possible_actions_and_position(
        position: typing.Tuple[int, int], actions: typing.Sequence[SimpleTilesAction]
) -> SimpleTilesState:
    up_blocked = down_blocked = left_blocked = right_blocked = True
    for action in actions:
        if action == SimpleTilesAction.GO_RIGHT:
            right_blocked = False
        elif action == SimpleTilesAction.GO_LEFT:
            left_blocked = False
        elif action == SimpleTilesAction.GO_DOWN:
            down_blocked = False
        elif action == SimpleTilesAction.GO_UP:
            up_blocked = False
        else:
            raise ValueError

    return SimpleTilesState(
        up_blocked, down_blocked, left_blocked, right_blocked, position[0], position[1]
    )


_STATUSES = {
    position: _status_from_possible_actions_and_position(position, statuses)
    for position, statuses in _ACTIONS.items()
}


def simple_tiles_actions_function(state: SimpleTilesState) -> typing.List[SimpleTilesAction]:
    return _ACTIONS[(state.hidden_row, state.hidden_col)]


def simple_tiles_undo_function(
        _: SimpleTilesState, __: SimpleTilesState,
        action: SimpleTilesAction) -> SimpleTilesAction:
    if action == SimpleTilesAction.GO_RIGHT:
        return SimpleTilesAction.GO_LEFT
    if action == SimpleTilesAction.GO_LEFT:
        return SimpleTilesAction.GO_RIGHT
    if action == SimpleTilesAction.GO_DOWN:
        return SimpleTilesAction.GO_UP
    if action == SimpleTilesAction.GO_UP:
        return SimpleTilesAction.GO_DOWN
    raise ValueError


def simple_tiles_result_function(action: SimpleTilesAction, state: SimpleTilesState) -> SimpleTilesState:
    if action == SimpleTilesAction.GO_RIGHT:
        position = state.hidden_row, state.hidden_col + 1
    elif action == SimpleTilesAction.GO_LEFT:
        position = state.hidden_row, state.hidden_col - 1
    elif action == SimpleTilesAction.GO_DOWN:
        position = state.hidden_row - 1, state.hidden_col
    elif action == SimpleTilesAction.GO_UP:
        position = state.hidden_row + 1, state.hidden_col
    else:
        raise ValueError
    return _STATUSES[position]


INITIAL_STATE = _STATUSES[(3, 3)]
