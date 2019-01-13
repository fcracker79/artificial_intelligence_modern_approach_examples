import os
from pprint import pprint

from pyswip import Prolog


def entry_point():
    prolog = Prolog()
    prolog.consult(os.path.join(os.path.dirname(__file__), 'wumpus.pl'))
    steps = list(map(lambda d: d.value, next(prolog.query('explore(X)'))['X']))
    win_result = bool(list(prolog.query('win(_)')))
    lose_result = bool(list(prolog.query('lost(_)')))
    if not win_result or lose_result:
        raise ValueError(win_result, lose_result)
    print('I won, positions: ')
    pprint(steps)


if __name__ == '__main__':
    entry_point()
