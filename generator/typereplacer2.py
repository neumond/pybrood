from copy import deepcopy

from .common import DiscardFunction


ARG_KEYS = {'const', 'type', 'opt_value'}
FUNC_KEYS = {'rconst', 'selfconst', 'rtype', 'args'}


def passover(item, keyset, as_is, **newdata):
    item = deepcopy(item)
    for k in keyset:
        if k in item and k not in as_is:
            del item[k]
    item.update(newdata)
    return item


def arg_replacer(a):
    if a.get('type') in ('Position', 'WalkPosition', 'TilePosition'):
        assert 'arg_code' not in a
        opt_value = a['opt_value']
        if opt_value is not None:
            assert 'Positions' in opt_value
            opt_value = 'Pybrood::' + opt_value
        return passover(
            a, ARG_KEYS, {'const'},
            type='Pybrood::UniversalPosition',
            opt_value=opt_value,
            arg_code='{bwtype}({aname}[0], {aname}[1])'.format(bwtype=a['type'], aname=a['name']),
        )

    if a.get('type') in ('UnitFilter', 'UnitFilter &', 'UnitCommand'):
        assert 'arg_code' not in a
        if a['opt_value'] is None:
            raise DiscardFunction  # Some UnitFilter argument is required, we can't provide it
        return passover(
            a, ARG_KEYS, set(),
            arg_code='nullptr',
        )

    return a


def func_replacer(f):
    if f['rtype'] in ('Position', 'WalkPosition', 'TilePosition'):
        yield passover(
            f, FUNC_KEYS, {'rconst', 'selfconst', 'args'},
            rtype='Pybrood::UniversalPosition',
            ret_code='{{_voidreturn}}Pybrood::convert_position<BWAPI::{}>({{_expr}});'.format(f['rtype']),
        )
        return

    if f['rtype'] in ('UnitFilter', 'UnitFilter &', 'UnitCommand'):
        raise DiscardFunction

    # Split methods accepting PositionOrUnit instances
    pu = False
    for i, a in enumerate(f['args']):
        if a.get('type') == 'PositionOrUnit':
            assert pu is False
            pu = i
    if pu is not False:
        ags1, ags2 = deepcopy(f['args']), deepcopy(f['args'])
        pua1, pua2 = ags1[pu], ags2[pu]
        pua1['type'] = 'Position'
        pua2['type'] = 'Unit'
        if f['args'][pu]['opt_value'] is not None:
            assert f['args'][pu]['opt_value'] == 'nullptr'
            pua1['opt_value'] = 'Positions::Unknown'
            pua2['opt_value'] = 'nullptr'
        ags1[pu] = arg_replacer(pua1)
        yield passover(
            f, FUNC_KEYS, {'rconst', 'selfconst', 'rtype'},
            args=ags1,
        )
        yield passover(
            f, FUNC_KEYS, {'rconst', 'selfconst', 'rtype'},
            args=ags2,
        )
        return

    yield f
    return
