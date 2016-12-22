from .common import atype_or_dots


REPLACEMENTS = {
    'Game::vPrintf': {
        'parsed': {
            'name': 'print',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'va_list elist; obj->vPrintf(line, elist);',
    },
    'Game::vSendText': {
        'parsed': {
            'name': 'sendText',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'va_list elist; obj->vSendText(line, elist);',
    },
    'Game::vSendTextEx': {
        'parsed': {
            'name': 'sendTextEx',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'bool', 'name': 'toAllies', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'va_list elist; obj->vSendTextEx(toAllies, line, elist);',
    },
    'Game::vDrawText': NotImplemented,
    'Game::drawText': {
        'parsed': {
            'name': 'drawText',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'CoordinateType::Enum', 'name': 'ctype', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawText(ctype, x, y, line);',
    },
    ('Game::drawTextMap', 'int', 'int', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextMap',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextMap(x, y, line);',
    },
    ('Game::drawTextMap', 'Position', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextMap',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextMap(p, line);',
    },
    ('Game::drawTextMouse', 'int', 'int', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextMouse',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextMouse(x, y, line);',
    },
    ('Game::drawTextMouse', 'Position', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextMouse',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextMouse(p, line);',
    },
    ('Game::drawTextScreen', 'int', 'int', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextScreen',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'int', 'name': 'x', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'y', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextScreen(x, y, line);',
    },
    ('Game::drawTextScreen', 'Position', 'const char *', '...'): {
        'parsed': {
            'name': 'drawTextScreen',
            'rconst': False, 'rtype': 'void',
            'args': [
                {'const': False, 'type': 'Position', 'name': 'p', 'opt_value': None},
                {'const': True, 'type': 'char *', 'name': 'line', 'opt_value': None},
            ],
        },
        'body': 'obj->drawTextScreen(p, line);',
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
    return repl
