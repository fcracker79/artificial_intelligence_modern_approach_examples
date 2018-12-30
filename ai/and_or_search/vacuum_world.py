import enum
import typing


@enum.unique
class VacuumPosition(enum.IntEnum):
    RIGHT = 0
    LEFT = 1


VacuumState = typing.NamedTuple(
    'VacuumState',
    (
        ('vacuum_position', VacuumPosition),
        ('left_clean', bool),
        ('right_clean', bool)
    )
)


@enum.unique
class VacuumAction(enum.IntEnum):
    SUCK = 1
    LEFT = 2
    RIGHT = 3


def vacuum_goal_test_function(state: VacuumState) -> bool:
    return state.left_clean and state.right_clean


def vacuum_results_function(state: VacuumState, action: VacuumAction) -> typing.Sequence[VacuumState]:
    if action == VacuumAction.RIGHT:
        return [
            VacuumState(
                VacuumPosition.RIGHT,
                state.left_clean, state.right_clean
            )
        ]
    if action == VacuumAction.LEFT:
        return [
            VacuumState(
                VacuumPosition.LEFT,
                state.left_clean, state.right_clean
            )
        ]
    assert action == VacuumAction.SUCK
    if state.vacuum_position == VacuumPosition.RIGHT:
        right_cleans = [True, False] if state.right_clean else [True]
        left_cleans = [True] if state.left_clean else [True, False]
    else:
        left_cleans = [True, False] if state.left_clean else [True]
        right_cleans = [True] if state.right_clean else [True, False]

    return [
        VacuumState(state.vacuum_position, left_clean, right_clean)
        for left_clean in left_cleans for right_clean in right_cleans
    ]


def vacuum_actions_function(state: VacuumState) -> typing.Sequence[VacuumAction]:
    actions = []
    if state.vacuum_position == VacuumPosition.RIGHT:
        actions.append(VacuumAction.LEFT)
        need_to_suck = not state.right_clean
    else:
        actions.append(VacuumAction.RIGHT)
        need_to_suck = not state.left_clean
    if need_to_suck:
        actions.append(VacuumAction.SUCK)
    return actions
