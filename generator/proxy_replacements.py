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
        'custom_body': 'va_list elist; instance.vPrintf({}, elist);'.format(STRF),
    },
    'Game::vSendText': {
        'name': 'sendText',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'va_list elist; instance.vSendText({}, elist);'.format(STRF),
    },
    'Game::vSendTextEx': {
        'name': 'sendTextEx',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'bool', 'name': 'toAllies', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'va_list elist; instance.vSendTextEx({{toAllies}}, {}, elist);'.format(STRF),
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
        'custom_body': 'instance.drawText({{ctype}}, {{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextMap({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMap', 'Position', 'const char *', '...'): {
        'name': 'drawTextMap',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextMap({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextMouse({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextMouse', 'Position', 'const char *', '...'): {
        'name': 'drawTextMouse',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextMouse({{p}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'int', 'int', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
            {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextScreen({{x}}, {{y}}, {});'.format(STRF),
    },
    ('Game::drawTextScreen', 'Position', 'const char *', '...'): {
        'name': 'drawTextScreen',
        'rconst': False, 'rtype': 'void', 'selfconst': False,
        'args': [
            {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
            {'const': False, 'type': 'std::string', 'name': 'line', 'opt_value': None},
        ],
        'custom_body': 'instance.drawTextScreen({{p}}, {});'.format(STRF),
    },
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
