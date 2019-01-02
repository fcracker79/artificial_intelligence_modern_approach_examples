from pprint import pprint

from ai.csp import backtrack, australia_color_adiacency


def entry_point():
    pprint(backtrack.backtracking_search(
        australia_color_adiacency.create_csp(),
        australia_color_adiacency.select_unassigned_variable,
        australia_color_adiacency.get_ordered_values
    ))


if __name__ == '__main__':
    entry_point()
