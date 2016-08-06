def fmt_arg(a, ns=None):
    result = '{} {}'.format(a['type'], a['name'])
    if ns is not None:
        result = ns + result
    if a['opt_value'] is not None:
        result += ' = {}'.format(a['opt_value'])
    if a['const']:
        result = 'const ' + result
    return result


def fmt_func_head(f):
    after = ' '.join(f['after'])
    if after:
        after = ' ' + after + ' '
    return '{} {}({}){}'.format(
        f['rtype'], f['name'],
        ', '.join(fmt_arg(a) for a in f['args']),
        after
    )


def arg_type_for_signature(a, ns=None):
    r = a['type']
    if ns is not None:
        r = ns + r
    if a['const']:
        r = 'const ' + r
    return r


def enum_types(f):
    yield f['rtype']
    for a in f['args']:
        yield a['type']


def transform_case(name):
    upse, pos, out = 0, 0, []
    for i, ch in enumerate(name):
        if ch.isupper():
            if upse == 0:
                out.append(name[pos:i].lower())
                pos = i
            upse += 1
        else:
            if upse > 1:
                out.append(name[pos:i].lower())
                pos = i
            upse = 0
    if upse == 0:
        out.append(name[pos:].lower())
    else:
        out.append(name[pos:].lower())
    return '_'.join(filter(lambda x: x, out))
