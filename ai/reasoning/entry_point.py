import os

from pyswip import Prolog


def entry_point():
    prolog = Prolog()
    prolog.consult(os.path.join(os.path.dirname(__file__), 'wumpus.pl'))
    next(prolog.query('explore()'))
    win_result = bool(list(prolog.query('win()')))
    lose_result = bool(list(prolog.query('lost()')))
    if not win_result or lose_result:
        raise ValueError(win_result, lose_result)
    print('I won, positions: ')


if __name__ == '__main__':
    entry_point()
