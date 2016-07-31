def indent_lines(lines, shift=4):
    if isinstance(lines, str):
        lines = lines.split('\n')
    ind = ' ' * shift
    return ''.join(map(lambda x: ind + x + '\n', lines))


def fmt_arg(a):
    result = '{} {}'.format(a['rtype'], a['name'])
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


def arg_type_for_signature(a):
    r = a['rtype']
    if a['const']:
        r = 'const ' + r
    return r


def enum_types(f):
    yield f['rtype']
    for a in f['args']:
        yield a['rtype']


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
