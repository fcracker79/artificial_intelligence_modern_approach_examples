import sys
import os

from ai import banner
from ai.search_tree import entry_point as search_tree_entry_point
from ai.search_tree.colored_areas import entry_point as colored_areas_entry_point
from ai.search_tree.eight_queens import entry_point as eight_queens_entry_point
from ai.search_tree.eight_puzzle import entry_point as eight_puzzle_entry_point
from ai.search_tree.eight_queens.min_conflict import min_conflict
from ai.game_play.minmax import entry_point as tic_tac_toe_entry_point
from ai.and_or_search import entry_point as and_or_search_entry_point


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


if __name__ == '__main__':
    sys.stdout = Unbuffered(sys.stdout)
    os.environ['PYTHONUNBUFFERED'] = '1'
    banner.horizontal('SEARCH TREE')
    search_tree_entry_point.entry_point()
    banner.horizontal('END SEARCH TREE')

    print()

    banner.horizontal('COLORED AREAS')
    colored_areas_entry_point.entry_point()
    banner.horizontal('END COLORED AREAS')

    print()

    banner.horizontal('EIGHT QUEENS')
    eight_queens_entry_point.entry_point()
    banner.horizontal('END EIGHT QUEENS')

    print()

    banner.horizontal('EIGHT QUEENS WITH MIN CONFLICTS')
    print('{}, with {} iterations'.format(*min_conflict()))
    banner.horizontal('END EIGHT QUEENS WITH MIN CONFLICTS')

    print()

    banner.horizontal('EIGHT PUZZLE')
    eight_puzzle_entry_point.entry_point()
    banner.horizontal('END EIGHT PUZZLE')

    print()

    banner.horizontal('TIC TAC TOE')
    tic_tac_toe_entry_point.entry_point()
    banner.horizontal('END TIC TAC TOE')

    print()

    banner.horizontal('AND-OR-SEARCH')
    and_or_search_entry_point.entry_point()
    banner.horizontal('END AND-OR-SEARCH')
