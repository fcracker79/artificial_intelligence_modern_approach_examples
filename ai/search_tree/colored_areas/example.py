from ai.search_tree.colored_areas.colored_areas import ColoredAreas


_AREAS_COUNT = 5
_AREAS = tuple('area{}'.format(i) for i in range(_AREAS_COUNT))
_COLORS = ('red', 'green', 'blue')
example = ColoredAreas(_AREAS, _COLORS)

for i, area in enumerate(_AREAS):
    if i == _AREAS_COUNT - 1:
        example.add_adiacency(_AREAS[-1], _AREAS[0])
    else:
        example.add_adiacency(area, _AREAS[i + 1])
