from sys import stderr
import re
from collections import defaultdict


weakreffing_map = {
    'Force': 'ForceWeakref',
    'Player': 'PlayerWeakref',
    'Unit': 'UnitWeakref',
}

returned_sets = {
    'Forceset': 'Force',
    'Playerset': 'Player',
    'Unitset': 'Unit',
}


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


def nametype_split(line):
    line = line.strip()
    c = 0
    for ch in reversed(line):
        if ch.isalnum() or ch == '_':
            c += 1
        else:
            break
    return squash_spaces(line[:-c].strip()), line[-c:].strip()


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
        'rtype': no_bwapi_in_type(a_type),
        'name': a_name,
        'opt_value': opt_value,
        'const': is_const
    }


def parse_func(line):
    a, b = line.rsplit('(', 1)
    b, c = b.rsplit(')', 1)
    ret_type, func_name = nametype_split(a.strip())
    return {
        'rtype': no_bwapi_in_type(ret_type),
        'name': func_name,
        'args': list(map(parse_arg, filter(lambda x: x, b.strip().split(',')))),
    }


def prep_arg(a):
    result = '{} {}'.format(a['rtype'], a['name'])
    if a['opt_value'] is not None:
        result += ' = {}'.format(a['opt_value'])
    if a['const']:
        result = 'const ' + result
    return result


def fmt_func(f):
    final_ret = f['rtype']
    # a_inv, a_sig = [], []
    # for a in f['args']:
    #     if a['rtype'] in weakreffing_map:
    #         x
    #     a_out.append(a['name'])
    inner_expr = 'obj->{fname}({arg_names})'.format(
        fname=f['name'], arg_names=', '.join(a['name'] for a in f['args'])
    )
    if f['rtype'] in weakreffing_map:
        inner_expr = '{}({})'.format(weakreffing_map[f['rtype']], inner_expr)
        final_ret = weakreffing_map[f['rtype']]
    elif f['rtype'] in returned_sets:
        final_ret = 'py::set'
        inner_expr = 'PyBinding::set_converter<{wtype}, BWAPI::{set_type}>({inner})'.format(
            set_type=f['rtype'], inner=inner_expr, wtype=weakreffing_map[returned_sets[f['rtype']]]
        )
    return '''{ret} {fname}({args_as_is}){{
    return {inner};
}}'''.format(
        ret=final_ret,
        fname=f['name'],
        args_as_is=', '.join(map(prep_arg, f['args'])),
        inner=inner_expr,
    )


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


def arg_type_for_signature(a):
    r = a['rtype']
    if a['const']:
        r = 'const ' + r
    return r


def enum_types(f):
    yield f['rtype']
    for a in f['args']:
        yield a['rtype']


KNOWN_TYPES = {
    'int', 'bool', 'double',
    'Unit', 'Force', 'Player',
    'Unitset', 'Forceset', 'Playerset',
}


class ModuleAccumulator:
    def __init__(self, mapped_class, ro_property_rule, rename_rule):
        self.mod_defs = []
        self.prop_names = set()
        self.meth_names = set()
        self.mapped_class = mapped_class
        self.mod_name = 'k_' + mapped_class.lower()
        self.derived_class = mapped_class + 'Weakref'
        self.ro_property_rule = ro_property_rule
        self.rename_rule = rename_rule

    def __call__(self, f):
        t = transform_case(f['name'])
        if not f['args'] and f['rtype'] != 'void' and self.ro_property_rule(f, t):
            t = self.rename_rule(f, t, True)
            self.mod_defs.append(
                '{modname}.def_property_readonly("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                    modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t
                )
            )
            assert t not in self.prop_names, t
            assert t not in self.meth_names, t
            self.prop_names.add(t)
        else:
            t = self.rename_rule(f, t, False)
            signature = '({ret} (PyBinding::{derclass}::*)({atypes}))'.format(
                ret=f['rtype'], derclass=self.derived_class,
                atypes=', '.join(arg_type_for_signature(a) for a in f['args'])
            )
            self.mod_defs.append((
                f['name'],
                '{modname}.def("{trans_name}", {sign} &PyBinding::{derclass}::{fname});'.format(
                    modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t,
                    sign=signature
                ),
                '{modname}.def("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                    modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t
                ),
            ))
            assert t not in self.prop_names, t
            self.meth_names.add(t)

    def assemble(self):
        name_freq = defaultdict(lambda: 0)
        for x in self.mod_defs:
            if isinstance(x, str):
                continue
            name_freq[x[0]] += 1
        for x in self.mod_defs:
            if isinstance(x, str):
                yield x
            else:
                if name_freq[x[0]] > 1:
                    yield x[1]
                else:
                    yield x[2]


def file_parser(f):
    ma = ModuleAccumulator(f.mapped_class, f.ro_property_rule, f.rename_rule)
    print('''#ifndef MODCODE

class {derclass}
{{
public:
    BWAPI::{mclass} obj;
    {derclass}(BWAPI::{mclass} iobj) : obj(iobj){{}};'''.format(
        mclass=ma.mapped_class, derclass=ma.derived_class
    ))

    for line in f.lines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('//'):
            continue
        if line.startswith('virtual '):
            line = line[len('virtual '):]
        if line.endswith(' = 0;'):
            line = line[:-len(' = 0;')] + ';'
        if line.endswith(' const;'):
            line = line[:-len(' const;')] + ';'
        fnc = parse_func(line)
        for t in enum_types(fnc):
            if t not in KNOWN_TYPES:
                print('UNKNOWN TYPE', t, file=stderr)
                break
        else:
            ma(fnc)
            print(indent_lines(fmt_func(fnc), shift=4))

    print('''}};

#else

py::class_<PyBinding::{derclass}> {modname}(m, "{mclass}");
{modname}.def("__init__", [](PyBinding::{derclass}){{
    throw std::runtime_error("{mclass} objects can't be instantiated from python side");
}});
{moddefs}

#endif
'''.format(
        mclass=f.mapped_class, modname=ma.mod_name, derclass=ma.derived_class,
        moddefs='\n'.join(ma.assemble()),
    ))


class UnitFile:
    mapped_class = 'Unit'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/Unit.h') as f:
            for i, line in enumerate(f, start=1):
                # lines 60..2458
                if 60 <= i <= 2458:
                    yield line

    @staticmethod
    def ro_property_rule(f, t):
        return (
            t.startswith(('is_', 'get_')) or
            t in ('exists', )
        )

    @staticmethod
    def rename_rule(f, t, is_property):
        if not is_property:
            return t
        if t == 'get_upgrade':
            return 'current_upgrade'
        elif t.startswith(('is_', 'get_')):
            return '_'.join(t.split('_')[1:])


file_parser(UnitFile)
