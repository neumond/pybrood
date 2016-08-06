from sys import stderr
from collections import defaultdict
from cdumper import transform_case
from cdeclparser import parse_func, lines_to_statements, flines, squash_spaces
from typereplacer import replace_all_args, replace_return
import jinja2
from html import unescape as html_unescape


jin_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'), autoescape=False)


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
    return code, {'rtype': r_type, 'args': ', '.join(a_sigs)}


class ModuleAccumulator:
    def __init__(self, ro_property_rule, rename_rule):
        self.mod_defs = []
        self.prop_names = set()
        self.meth_names = set()
        self.ro_property_rule = ro_property_rule
        self.rename_rule = rename_rule

    def _add_property(self, f, t, sig):
        t = self.rename_rule(f, t, True)
        self.mod_defs.append({
            'type': 'def_property_readonly',
            'trans_name': t,
            'method_name': f['name'],
        })
        assert t not in self.prop_names, t
        assert t not in self.meth_names, t
        self.prop_names.add(t)

    def _add_function(self, f, t, sig):
        t = self.rename_rule(f, t, False)
        self.mod_defs.append({
            'type': 'def',
            'trans_name': t,
            'method_name': f['name'],
            'sign': sig,
        })
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
            if x['type'] != 'def':
                continue
            name_freq[x['method_name']] += 1
        for x in self.mod_defs:
            if x['type'] == 'def' and name_freq[x['method_name']] == 1:
                del x['sign']
            yield x


def file_parser(f):
    ma = ModuleAccumulator(f.ro_property_rule, f.rename_rule)
    methods = []
    for func in lines_to_statements(f.lines()):
        fnc = parse_func(func)
        try:
            code, sig = fmt_func(fnc, '->')
        except AssertionError as e:
            print(e, file=stderr)
        else:
            ma(fnc, sig)
            methods.append(code)

    enums = []
    try:
        ls = f.enum_lines()
    except NotImplementedError:
        pass
    else:
        for expr in lines_to_statements(ls):
            expr = squash_spaces(expr).split(' ')
            assert expr[0] == 'extern'
            assert expr[1] == 'const'
            assert expr[2] == f.mapped_class
            assert len(expr) == 4
            enums.append(expr[3])

    return html_unescape(jin_env.get_template('weakref.jinja2').render(
        bw_class=f.mapped_class,
        methods=methods,
        module_defs=ma.assemble(),
        enums=enums,
        enum_namespace=f.enum_namespace,
        make_pointer=f.make_obj_pointer,
    ))


class BaseFile:
    mapped_class = NotImplemented
    enum_namespace = NotImplemented
    make_obj_pointer = False

    @staticmethod
    def lines():
        raise NotImplementedError

    @staticmethod
    def enum_lines():
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

    @classmethod
    def perform(cls):
        with open('pybinding/' + cls.out_file, 'w') as f:
            f.write(file_parser(cls))


class UnitFile(BaseFile):
    mapped_class = 'Unit'
    out_file = 'unit_auto.cpp'

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
    make_obj_pointer = True
    enum_namespace = 'BWAPI::UnitTypes'
    out_file = 'unittype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/UnitType.h')
        yield from f(279, 902)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/UnitType.h')
        yield from f(951, 1234)


class ForceFile(BaseFile):
    mapped_class = 'Force'
    out_file = 'force_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/Force.h')
        yield from f(25, 63)


class PlayerFile(BaseFile):
    mapped_class = 'Player'
    out_file = 'player_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/Player.h')
        yield from f(38, 641)


class BulletTypeFile(BaseFile):
    mapped_class = 'BulletType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::BulletTypes'
    out_file = 'bullettype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/BulletType.h')
        yield from f(75, 75)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/BulletType.h')
        yield from f(87, 123)


class DamageTypeFile(BaseFile):
    mapped_class = 'DamageType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::DamageTypes'
    out_file = 'damagetype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/DamageType.h')
        yield from f(48, 48)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/DamageType.h')
        yield from f(60, 66)


class UpgradeTypeFile(BaseFile):
    mapped_class = 'UpgradeType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::UpgradeTypes'
    out_file = 'upgradetype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/UpgradeType.h')
        yield from f(93, 172)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/UpgradeType.h')
        yield from f(183, 245)


class WeaponTypeFile(BaseFile):
    mapped_class = 'WeaponType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::WeaponTypes'
    out_file = 'weapontype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/WeaponType.h')
        yield from f(153, 305)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/WeaponType.h')
        yield from f(330, 439)


class PlayerTypeFile(BaseFile):
    mapped_class = 'PlayerType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::PlayerTypes'
    out_file = 'playertype_auto.cpp'

    @staticmethod
    def lines():
        f = flines('../bwapi/bwapi/include/BWAPI/PlayerType.h')
        yield from f(45, 57)

    @staticmethod
    def enum_lines():
        f = flines('../bwapi/bwapi/include/BWAPI/PlayerType.h')
        yield from f(68, 78)


def main():
    UnitFile.perform()
    UnitTypeFile.perform()
    ForceFile.perform()
    PlayerFile.perform()
    BulletTypeFile.perform()
    DamageTypeFile.perform()
    UpgradeTypeFile.perform()
    WeaponTypeFile.perform()
    PlayerTypeFile.perform()
