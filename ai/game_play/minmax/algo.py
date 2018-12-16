from ai.game_play.minmax import ScoreFunction, CutoffFunction, NodeWithScore
from ai.search_tree.common_types import Node, GenericGraph


def minmax_decision(
        node: Node, graph: GenericGraph,
        score_function: ScoreFunction,
        cutoff_function: CutoffFunction=lambda d: d) -> NodeWithScore:
    children = list(cutoff_function(graph.get_children(node)))
    if not children:
        return NodeWithScore(node, score_function(node), -1, 0)
    children_minmax = tuple(minmax_decision(c, graph, score_function, cutoff_function=cutoff_function) for c in children)
    if node.depth % 2 == 0:
        aggregate = max
    else:
        aggregate = min

    # print('cur node: \n{}'.format(node.state))
    # for c in children_minmax:
    #     print('Child: \n{}\nValue {}\nScore {}\n'.format(
    #         c.node.state, c.node.state.get_value(), c.score))
    best_child_index = aggregate(
        range(len(children_minmax)),
        key=lambda d: children_minmax[d].score * 1000 - children_minmax[d].steps_to_best_move)
    _, score, _, steps_to_best_move = children_minmax[best_child_index]
    return NodeWithScore(node, score, best_child_index, steps_to_best_move + 1)
