from ai.probabilistic_reasoning.bayesian_network import BayesianNetwork, BayesianVariable

_INDENT = 2


def _print_bayesian_node(node: BayesianVariable, spaces: int=0):
    print('{spaces}{variable_id}({variable_data})'.format(
        spaces=' ' * spaces, variable_id=node.id, variable_data=node.data
    ))
    for child in node.children:
        _print_bayesian_node(child, spaces=spaces + _INDENT)


def print_bayesian_network(bayesian_network: BayesianNetwork):
    for node in bayesian_network:
        _print_bayesian_node(node)
