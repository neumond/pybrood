CPP_MODULE_NAME = 'inner'


class DiscardFunction(Exception):
    pass


def get_full_argtype(a):
    t = a['type']
    if a['const']:
        t = 'const ' + t
    return t


def get_full_rettype(a):
    t = a['rtype']
    if a['rconst']:
        t = 'const ' + t
    return t


def atype_or_dots(a):
    if a['type'] == '':
        return '...'
    return get_full_argtype(a)


def get_all_used_types(f):
    return {f['rtype']} | {a['type'] for a in f['args']}


def make_overload_signature(func, class_name):
    argline = ', '.join(atype_or_dots(a) for a in func['args'] if 'type' in a)
    r = '{} ({}::*)({})'.format(get_full_rettype(func), class_name, argline)
    if func['selfconst']:
        r += ' const'
    return r
