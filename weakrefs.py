from sys import stderr
from collections import defaultdict
from cdumper import indent_lines, transform_case
from cdeclparser import parse_func, lines_to_funclines
from typereplacer import replace_all_args, replace_return


def fmt_func(f, obj_op):
    a_lines, a_exprs, a_codes, a_sigs = replace_all_args(f, sig_prepend_ns=True)
    assert all(x is None for x in a_codes), 'Argument preparation code is not supported'
    inner_expr = 'obj{obj_op}{fname}({a_exprs})'.format(
        obj_op=obj_op, fname=f['name'], a_exprs=', '.join(a_exprs)
    )
    r_type, r_expr = replace_return(f)
    r_expr = r_expr.format(inner_expr)
    code = '''{r_type} {fname}({a_lines}){{
    {inner}
}}'''.format(
        r_type=r_type, fname=f['name'], inner=r_expr, a_lines=', '.join(a_lines)
    )
    sig = '{r_type} {{}}({a_sigs})'.format(r_type=r_type, a_sigs=', '.join(a_sigs))
    return code, sig


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

    def _add_property(self, f, t, sig):
        t = self.rename_rule(f, t, True)
        self.mod_defs.append(
            '{modname}.def_property_readonly("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t
            )
        )
        assert t not in self.prop_names, t
        assert t not in self.meth_names, t
        self.prop_names.add(t)

    def _add_function(self, f, t, sig):
        t = self.rename_rule(f, t, False)
        sig = sig.format('(PyBinding::{derclass}::*)'.format(derclass=self.derived_class))
        self.mod_defs.append((
            f['name'],
            '{modname}.def("{trans_name}", ({sign}) &PyBinding::{derclass}::{fname});'.format(
                modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t,
                sign=sig
            ),
            '{modname}.def("{trans_name}", &PyBinding::{derclass}::{fname});'.format(
                modname=self.mod_name, fname=f['name'], derclass=self.derived_class, trans_name=t
            ),
        ))
        assert t not in self.prop_names, t
        self.meth_names.add(t)

    def __call__(self, f, sig):
        t = transform_case(f['name'])
        if not f['args'] and f['rtype'] != 'void' and self.ro_property_rule(f, t):
            self._add_property(f, t, sig)
        else:
            self._add_function(f, t, sig)

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


def file_parser(f, out_file):
    ma = ModuleAccumulator(f.mapped_class, f.ro_property_rule, f.rename_rule)
    out_file.write('''#ifndef MODCODE

class {derclass}
{{
public:
    BWAPI::{mclass} obj;
    {derclass}(BWAPI::{mclass} iobj) : obj(iobj){{}};
'''.format(
        mclass=ma.mapped_class, derclass=ma.derived_class
    ))

    for func in lines_to_funclines(f.lines()):
        fnc = parse_func(func)
        try:
            code, sig = fmt_func(fnc, f.obj_op)
        except AssertionError as e:
            print(e, file=stderr)
        else:
            ma(fnc, sig)
            out_file.write(indent_lines(code, shift=4))

    out_file.write('''}};

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


class BaseFile:
    mapped_class = NotImplemented
    obj_op = '->'

    @staticmethod
    def lines():
        raise NotImplementedError

    @staticmethod
    def ro_property_rule(f, t):
        return t.startswith(('is_', 'get_'))

    @staticmethod
    def rename_rule(f, t, is_property):
        if not is_property:
            return t
        elif t.startswith(('get_',)):
            return '_'.join(t.split('_')[1:])
        return t


class UnitFile(BaseFile):
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
        elif t.startswith(('get_',)):
            return '_'.join(t.split('_')[1:])
        return t


class UnitTypeFile(BaseFile):
    mapped_class = 'UnitType'
    obj_op = '.'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/UnitType.h') as f:
            for i, line in enumerate(f, start=1):
                if 279 <= i <= 902:
                    yield line


class ForceFile(BaseFile):
    mapped_class = 'Force'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/Force.h') as f:
            for i, line in enumerate(f, start=1):
                if 25 <= i <= 63:
                    yield line


class PlayerFile(BaseFile):
    mapped_class = 'Player'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/Player.h') as f:
            for i, line in enumerate(f, start=1):
                if 38 <= i <= 641:
                    yield line


def main():
    with open('pybinding/unit_auto.cpp', 'w') as f:
        file_parser(UnitFile, f)
    with open('pybinding/unittype_auto.cpp', 'w') as f:
        file_parser(UnitTypeFile, f)
    with open('pybinding/force_auto.cpp', 'w') as f:
        file_parser(ForceFile, f)
    with open('pybinding/player_auto.cpp', 'w') as f:
        file_parser(PlayerFile, f)
