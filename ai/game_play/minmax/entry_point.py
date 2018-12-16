from ai.game_play.minmax.algo import minmax_decision
from ai.game_play.minmax.cutoff_functions import max_depth
from ai.game_play.minmax.tris import TrisGraph, TrisState
from ai.search_tree.common_types import Node


_CUTOFF_FUNCTION_DEPTH = 5


def entry_point(ask_for_choice: bool=False):
    g = TrisGraph()
    root = Node(TrisState(), None, 0, 0)

    while True:
        # Here I choose the best move
        root, score, best_move, _ = minmax_decision(
            root, g, lambda n: n.state.get_value(), max_depth(_CUTOFF_FUNCTION_DEPTH + root.depth))
        root = g.get_children(root)[best_move]
        print('My move\n', root.state, sep='')
        if root.state.i_win():
            print('I win')
            break
        # My opponent chooses the lowest position
        opponent_choices = g.get_children(root)
        if all(root.state.statuses):
            print('No winner')
            break
        if ask_for_choice:
            for i, v in enumerate(map(lambda d: str(d.state), opponent_choices)):
                print('Choice', i)
                print(v)

            root = opponent_choices[int(input('Choose your move: '))]
        else:
            root = opponent_choices[
                min(range(len(opponent_choices)), key=lambda d: -opponent_choices[d].state.get_other_value())
            ]
        print('Your move\n', root.state, sep='')
        if root.state.you_win():
            print('You win')
            break
        pass


if __name__ == '__main__':
    entry_point(ask_for_choice=True)
