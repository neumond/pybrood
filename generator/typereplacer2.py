class NoReplacement(Exception):
    pass


def arg_replacer(a):
    if a['type'] in ('Position', 'WalkPosition', 'TilePosition'):
        return (
            'Pybrood::UniversalPosition {}'.format(a['name']),
            '{bwtype}({aname}[0], {aname}[1])'.format(aname=a['name'], bwtype=a['type'])
        )
    if a['type'] == 'PositionOrUnit':
        # TODO: duplicate methods for overloading
        return (
            'Pybrood::UniversalPosition {}'.format(a['name']),
            'PositionOrUnit(Position({aname}[0], {aname}[1]))'.format(aname=a['name'])
        )
    raise NoReplacement
