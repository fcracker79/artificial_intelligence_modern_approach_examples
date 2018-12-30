from pprint import pprint

from ai.and_or_search.algo import or_search
from ai.and_or_search.vacuum_world import VacuumState, VacuumPosition, vacuum_goal_test_function, \
    vacuum_results_function, vacuum_actions_function


def entry_point():
    result = or_search(
        VacuumState(
            VacuumPosition.LEFT,
            False, False
        ),
        vacuum_goal_test_function,
        vacuum_results_function,
        vacuum_actions_function
    )
    pprint(result)


if __name__ == '__main__':
    entry_point()
