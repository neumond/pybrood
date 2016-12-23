class NoReplacement(Exception):
    pass


def arg_replacer(a):
    if a['type'] in ('Position', 'WalkPosition', 'TilePosition'):
        return (
            'Pybrood::UniversalPosition {}'.format(a['name']),
            '{bwtype}({aname}[0], {aname}[1])'.format(aname=a['name'], bwtype=a['type']),
        )
    if a['type'] in ('UnitFilter', 'UnitFilter &'):
        return (
            None,
            'nullptr',
        )
    raise NoReplacement
