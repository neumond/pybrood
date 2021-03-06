from .common import atype_or_dots, DiscardFunction


STRF = 'Pybrood::string_replace(line, "%", "%%").c_str()'
TOLIST = '''
auto c = {source};
py::list result;
for (auto it = c.begin(); it != c.end(); ++it){{{{
    result.append({element});
}}}}
return result;
'''.strip()
# element='*it'


REPLACEMENTS = {
    'Game::vPrintf': {
        'name': 'print',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'va_list elist; Broodwar->vPrintf({}, elist);'.format(STRF),
    },
    'Game::vSendText': {
        'name': 'sendText',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'va_list elist; Broodwar->vSendText({}, elist);'.format(STRF),
    },
    'Game::vSendTextEx': {
        'name': 'sendTextEx',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'bool', 'name': 'toAllies', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'va_list elist; Broodwar->vSendTextEx({{toAllies}}, {}, elist);'.format(STRF),
    },
    'Game::vDrawText': NotImplemented,
    'Game::drawText': {
        'name': 'drawText',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'CoordinateType::Enum', 'name': 'ctype', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawText({{ctype}}, {{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextMap({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'Position', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextMap({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextMouse({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'Position', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextMouse({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextScreen({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'Position', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'ret_code': 'Broodwar->drawTextScreen({{p}}, {});'.format(STRF),
    },
    'Unitset::setClientInfo': NotImplemented,
    'Game::getEvents': NotImplemented,  # TODO: return back
}


for t in (
    'BulletType', 'Color', 'DamageType', 'Error', 'ExplosionType', 'GameType', 'Order', 'PlayerType', 'Race',
    'TechType', 'UnitCommandType', 'UnitSizeType', 'UnitType', 'UpgradeType', 'WeaponType'
):
    # fighting with inline methods
    REPLACEMENTS['{}::getID'.format(t)] = {
        'name': 'getID',
        'rconst': False, 'rtype': 'int', 'selfconst': True,
        'args': [],
    }
    REPLACEMENTS['{}::getName'.format(t)] = {
        'name': 'getName',
        'rconst': True, 'rtype': 'std::string', 'selfconst': True,
        'args': [],
    }


for t, pcls in (('Game::getNukeDots', 'Position'), ('Game::getStartLocations', 'TilePosition')):
    m = t.split('::', 1)[1]
    REPLACEMENTS[t] = {
        'name': m,
        'rconst': False, 'rtype': 'py::list', 'selfconst': True,
        'args': [],
        'ret_code': TOLIST.format(
            source='Broodwar->{}()'.format(m),
            element='Pybrood::convert_position<{}>(*it)'.format(pcls),
        ),
    }


for t in (
    'Playerset::getRaces', 'UnitType::abilities', 'UnitType::researchesWhat', 'UnitType::upgrades',
    'UnitType::upgradesWhat', 'Unit::getTrainingQueue',
    'TechType::whatUses', 'UnitType::buildsWhat', 'UpgradeType::whatUses',
):
    m = t.split('::', 1)[1]
    REPLACEMENTS[t] = {
        'name': m,
        'rconst': False, 'rtype': 'py::list', 'selfconst': True, 'args': [],
        'ret_code': TOLIST.format(source='instance.{}()'.format(m), element='*it'),
    }


def get_replacement_inner(func, class_name):
    k = '{}::{}'.format(class_name, func['name'])
    if k in REPLACEMENTS:
        return REPLACEMENTS[k]
    k = (k, ) + tuple(atype_or_dots(a) for a in func['args'])
    if k in REPLACEMENTS:
        return REPLACEMENTS[k]


def get_replacement(func, class_name):
    repl = get_replacement_inner(func, class_name)
    if repl is NotImplemented:
        raise DiscardFunction
    elif repl is None:
        return func
    return repl


def custom_replacements(class_data, class_name):
    methods = []
    for func in class_data['methods']:
        try:
            methods.append(get_replacement(func, class_name))
        except DiscardFunction:
            pass
    class_data['methods'] = methods
