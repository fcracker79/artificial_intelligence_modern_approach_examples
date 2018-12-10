import sys
import os

from ai import banner
from ai.search_tree import entry_point as search_tree_entry_point
from ai.search_tree.colored_areas import entry_point as colored_areas_entry_point
from ai.search_tree.eight_queens import entry_point as eight_queens_entry_point
from ai.search_tree.eight_puzzle import entry_point as eight_puzzle_entry_point


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

    banner.horizontal('COLORED AREAS')
    colored_areas_entry_point.entry_point()
    banner.horizontal('END COLORED AREAS')

    banner.horizontal('EIGHT QUEENS')
    eight_queens_entry_point.entry_point()
    banner.horizontal('END EIGHT QUEENS')

    banner.horizontal('8-PUZZLE')
    eight_puzzle_entry_point.entry_point()
    banner.horizontal('END 8-PUZZLE')
