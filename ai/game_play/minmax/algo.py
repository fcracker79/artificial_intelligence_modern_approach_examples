import sys
import typing

from ai.game_play.minmax import ScoreFunction, CutoffFunction, NodeWithScore
from ai.search_tree.common_types import Node, GenericGraph


def minmax_decision(
        node: Node, graph: GenericGraph,
        score_function: ScoreFunction,
        cutoff_function: CutoffFunction=lambda d: d,
        min_alpha_beta_value: typing.Optional[int]=None) -> typing.Optional[NodeWithScore]:
    children = list(cutoff_function(graph.get_children(node)))
    if not children:
        return NodeWithScore(node, score_function(node), -1, 0)
    if node.depth % 2 == 0:
        aggregate = max
        should_check_for_min_alpha_beta_value = False
    else:
        aggregate = min
        should_check_for_min_alpha_beta_value = True

    if should_check_for_min_alpha_beta_value:
        children_minmax = []
        # I know that MAX has found a node whose score is 'min_alpha_beta_value'.
        # So if a child has a lower score, since I am MIN, that node will never reach
        # a value above that child.
        # So I return None with the meaning of 'no such child'.
        for c in (minmax_decision(c, graph, score_function, cutoff_function=cutoff_function) for c in children):
            if c.score < min_alpha_beta_value:
                return None
            children_minmax.append(c)
    else:
        cur_max = -sys.maxsize
        children_minmax = []
        # Here the order is important.
        # Since I am MAX, I want to choose my score AND prune all next MIN that will neve
        # produce a move that may be interesting.
        # So in theory, if I could heuristically know which order to follow in the children,
        # I could be more efficient in pruning.
        for c in children:
            cur_minmax = minmax_decision(c, graph, score_function, cutoff_function=cutoff_function, min_alpha_beta_value=cur_max)
            if not cur_minmax:
                continue
            children_minmax.append(cur_minmax)
            if cur_minmax.score > cur_max:
                cur_max = cur_minmax.score

    # print('cur node: \n{}'.format(node.state))
    # for c in children_minmax:
    #     print('Child: \n{}\nValue {}\nScore {}\n'.format(
    #         c.node.state, c.node.state.get_value(), c.score))
    best_child_index = aggregate(
        range(len(children_minmax)),
        # We sort by score and then by shortest step. This way I can achieve the
        # result before.
        key=lambda d: children_minmax[d].score * 1000 - children_minmax[d].steps_to_best_move)
    _, score, _, steps_to_best_move = children_minmax[best_child_index]
    return NodeWithScore(node, score, best_child_index, steps_to_best_move + 1)
