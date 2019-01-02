from pprint import pprint

from ai.csp import backtrack, australia_color_adiacency


def entry_point():
    result = backtrack.backtracking_search(
        australia_color_adiacency.create_csp(),
        australia_color_adiacency.select_unassigned_variable,
        australia_color_adiacency.get_ordered_values
    )
    pprint(result)
    for adiacency in australia_color_adiacency.AUSTRALIA_CONSTRAINED_VARIABLES:
        expected_colors = len(adiacency)
        colors = set(map(result.__getitem__, adiacency))
        if len(colors) != expected_colors:
            raise ValueError


if __name__ == '__main__':
    entry_point()
