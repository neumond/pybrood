from sys import stdin
import re
from collections import defaultdict


MAPPED_CLASS = 'Unit'
mod_name = 'k_' + MAPPED_CLASS.lower()
derived_class = MAPPED_CLASS + 'Weakref'


weakreffing_map = {
    'Force': 'ForceWeakref',
    'Player': 'PlayerWeakref',
    'Unit': 'UnitWeakref',
}

returned_sets = {
    'Playerset',
    'Forceset',
    'Unitset',
}


print('''#ifndef MODCODE

class {derclass}
{{
public:
    BWAPI::{mclass} obj;
    {derclass}(BWAPI::{mclass} iobj) : obj(iobj){{}};'''.format(
    mclass=MAPPED_CLASS, derclass=derived_class
))


def squash_spaces(line):
    return re.sub('\s+', ' ', line)


def no_bwapi_in_type(line):
    if line.startswith('BWAPI::'):
        return line[len('BWAPI::'):]
    return line


def indent_lines(lines, shift=4):
    if isinstance(lines, str):
        lines = lines.split('\n')
    ind = ' ' * shift
    return '\n'.join(map(lambda x: ind + x, lines))


def parse_arg(line):
    line = line.strip()
    opt_value = None
    if '=' in line:
        line, opt_value = line.split('=')
        line, opt_value = line.strip(), opt_value.strip()
    if line.startswith('const '):
        line = line[len('const '):].strip()
    a_type, a_name = squash_spaces(line).split(' ')
    return no_bwapi_in_type(a_type), a_name, opt_value


def parse_func(line):
    a, b = line.split('(', 1)
    b, c = b.split(')', 1)
    ret_type, func_name = squash_spaces(a.strip()).split(' ')
    return no_bwapi_in_type(ret_type), func_name, list(map(parse_arg, filter(lambda x: x, b.strip().split(','))))


def prep_arg(a):
    rt, n, av = a
    result = '{} {}'.format(rt, n)
    if av is not None:
        result += ' = {}'.format(av)
    return result


def fmt_func(ret_type, func_name, args):
    final_ret = ret_type
    inner_expr = 'obj->{fname}({arg_names})'.format(
        fname=func_name, arg_names=', '.join(n for rt, n, av in args)
    )
    if ret_type in weakreffing_map:
        # py::set getPlayers(){
        #     return set_converter<PlayerWeakref, BWAPI::Playerset>(obj->getPlayers());
        # }
        inner_expr = '{}({})'.format(weakreffing_map[ret_type], inner_expr)
        final_ret = weakreffing_map[ret_type]
    return '''{ret} {fname}({args_as_is}){{
    return {inner};
}}'''.format(
        ret=final_ret,
        fname=func_name,
        args_as_is=', '.join(map(prep_arg, args)),
        inner=inner_expr,
    )


mod_defs = []
prop_names = set()
meth_names = set()


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


def accumulate_mod(ret_type, func_name, args):
    # print(ret_type, func_name, args)
    t = transform_case(func_name)
    if not args and ret_type != 'void' and (
        t.startswith(('is_', 'get_')) or
        t in ('exists', )
    ):
        if t == 'get_upgrade':
            t = 'current_upgrade'
        elif t.startswith(('is_', 'get_')):
            t = '_'.join(t.split('_')[1:])
        mod_defs.append(
            '{modname}.def_property_readonly("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                modname=mod_name, fname=func_name, derclass=derived_class, trans_name=t
            )
        )
        assert t not in prop_names, t
        assert t not in meth_names, t
        prop_names.add(t)
    else:
        signature = '({ret} (PyBinding::{derclass}::*)({atypes}))'.format(
            ret=ret_type, derclass=derived_class,
            atypes=', '.join(rt for rt, n, av in args)
        )
        mod_defs.append((
            func_name,
            '{modname}.def("{trans_name}", {sign} &PyBinding::{derclass}::{fname});'.format(
                modname=mod_name, fname=func_name, derclass=derived_class, trans_name=t,
                sign=signature
            ),
            '{modname}.def("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                modname=mod_name, fname=func_name, derclass=derived_class, trans_name=t
            ),
        ))
        assert t not in prop_names, t
        meth_names.add(t)


def assemble_mod_defs():
    name_freq = defaultdict(lambda: 0)
    for x in mod_defs:
        if isinstance(x, str):
            continue
        name_freq[x[0]] += 1
    for x in mod_defs:
        if isinstance(x, str):
            yield x
        else:
            if name_freq[x[0]] > 1:
                yield x[1]
            else:
                yield x[2]


for line in stdin:
    line = line.strip()
    if not line:
        continue
    if line.startswith('//'):
        continue
    if line.startswith('virtual '):
        line = line[len('virtual '):]
    if line.endswith(' const = 0;'):
        line = line[:-len(' const = 0;')] + ';'
    if line.endswith(' const;'):
        line = line[:-len(' const;')] + ';'

    fnc = parse_func(line)
    accumulate_mod(*fnc)
    print(indent_lines(fmt_func(*fnc), shift=4))


print('''}};

#else

py::class_<PyBinding::{derclass}> {modname}(m, "{mclass}");
{modname}.def("__init__", [](PyBinding::{derclass}){{
    throw std::runtime_error("{mclass} objects can't be instantiated from python side");
}});
{moddefs}

#endif
'''.format(
    mclass=MAPPED_CLASS, modname=mod_name, derclass=derived_class,
    moddefs='\n'.join(assemble_mod_defs()),
))
