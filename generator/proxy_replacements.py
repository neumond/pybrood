from .common import atype_or_dots


'''
.def("drawText", [](
    Game& instance,
    CoordinateType::Enum ctype,
    int x,
    int y,
    std::string line
){
    // simply omitting variadic part
    instance.drawText(ctype, x, y, Pybrood::string_replace(line, "%", "%%").c_str());
})
'''

STRF = 'Pybrood::string_replace(line, "%", "%%").c_str()'


REPLACEMENTS = {
    'Game::vPrintf': {
        'name': 'print',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'va_list elist; Broodwar->vPrintf({}, elist);'.format(STRF),
    },
    'Game::vSendText': {
        'name': 'sendText',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'va_list elist; Broodwar->vSendText({}, elist);'.format(STRF),
    },
    'Game::vSendTextEx': {
        'name': 'sendTextEx',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'bool', 'name': 'toAllies', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'va_list elist; Broodwar->vSendTextEx({{toAllies}}, {}, elist);'.format(STRF),
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
        'custom_body': 'Broodwar->drawText({{ctype}}, {{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextMap({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'Position', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextMap({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextMouse({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'Position', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextMouse({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextScreen({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'Position', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'Broodwar->drawTextScreen({{p}}, {});'.format(STRF),
    },
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
        'custom_body': 'return instance.getID();',
    }
    REPLACEMENTS['{}::getName'.format(t)] = {
        'name': 'getName',
        'rconst': True, 'rtype': 'std::string', 'selfconst': True,
        'args': [],
        'custom_body': 'return instance.getName();',
    }


class MethodDiscarded(Exception):
    pass


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
        raise MethodDiscarded
    elif repl is None:
        return func
    return repl
