from pprint import pprint

from ai.search_tree.online_search.algo import run, Result, State
from ai.search_tree.online_search.simple_tiles import INITIAL_STATE, simple_tiles_goal_function, \
    simple_tiles_result_function, simple_tiles_actions_function, simple_tiles_undo_function


_TAB_SIZE = 4


def _print_result(state: State, result: Result, indent: int=0):
    if state not in result:
        return
    for action, child_state in result[state].items():
        print(' ' * indent, action)
        _print_result(child_state, result, indent=indent + _TAB_SIZE)


def entry_point():
    result = run(
        INITIAL_STATE,
        simple_tiles_goal_function,
        simple_tiles_result_function,
        simple_tiles_actions_function,
        simple_tiles_undo_function
    )
    print('Initial state')
    _print_result(INITIAL_STATE, result)


if __name__ == '__main__':
    entry_point()
