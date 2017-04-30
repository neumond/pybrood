from ..utils import flines, squash_spaces
from os.path import join


def nametype_split(line):
    line = line.strip()
    c = 0
    for ch in reversed(line):
        if ch.isalnum() or ch == '_':
            c += 1
        else:
            break
    return squash_spaces(line[:-c].strip()), line[-c:].strip()


def no_bwapi_in_type(line):
    if line.startswith('BWAPI::'):
        return line[len('BWAPI::'):]
    return line


def parse_arg(line):
    line = line.strip()
    opt_value, is_const = None, False
    if '=' in line:
        line, opt_value = line.split('=')
        line, opt_value = line.strip(), opt_value.strip()
    if line.startswith('const '):
        line = line[len('const '):].strip()
        is_const = True
    a_type, a_name = nametype_split(line)
    return {
        'type': no_bwapi_in_type(a_type),
        'name': a_name,
        'opt_value': opt_value,
        'const': is_const
    }


def split_function_line(line):
    b, after_line = line.rsplit(')', 1)
    lvl = 0
    for i, ch in enumerate(reversed(b)):
        if ch == ')':
            lvl += 1
        elif ch == '(':
            lvl -= 1
            if lvl < 0:
                break
    else:
        raise ValueError('Bad function definition ' + line)
    args_line = b[-i:] if i > 0 else ''
    fname_line = b[:-i-1]
    return fname_line, args_line, after_line


def parse_func(line):
    fname_line, args_line, after_line = split_function_line(line)
    if '=' in after_line:
        after_line = after_line.split('=', 1)[0]

    ret_type, func_name = nametype_split(fname_line.strip())
    ret_type = squash_spaces(ret_type.strip())
    ret_type = ret_type.split(' ')
    ret_const = False
    while True:
        if ret_type[0] == 'virtual':
            ret_type.pop(0)
            continue
        if ret_type[0] == 'const':
            ret_type.pop(0)
            ret_const = True
            continue
        break
    ret_type = ' '.join(ret_type)

    after = squash_spaces(after_line.strip())
    assert after in ('', 'const')
    return {
        'rtype': no_bwapi_in_type(ret_type),
        'rconst': ret_const,
        'name': func_name,
        'args': list(map(parse_arg, filter(lambda x: x, args_line.strip().split(',')))),
        'selfconst': after == 'const',
    }


def lines_to_statements(lines, separator=';'):
    all_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('//'):
            continue
        all_lines.append(line)
    all_lines = '\n'.join(all_lines)
    for func in all_lines.split(separator):
        func = func.strip()
        if not func:
            continue
        yield func


def incflines(BWAPI_INCLUDE_DIR, *fname):
    return flines(join(BWAPI_INCLUDE_DIR, *fname))
