from sys import stderr
from collections import defaultdict
from .cdumper import transform_case
from .cdeclparser import parse_func, lines_to_statements
from html import unescape as html_unescape
from .utils import jin_env, squash_spaces, flines
from .config import BWAPI_INCLUDE_DIR, GEN_OUTPUT_DIR
from os.path import join


def fmt_func(f, obj_op):
    from .typereplacer import replace_all_args, replace_return
    a_lines, a_exprs, a_codes, a_sigs, a_lines_nodef, a_incs = replace_all_args(f, sig_prepend_ns=True)
    assert all(x is None for x in a_codes), 'Argument preparation code is not supported'
    inner_expr = 'obj{obj_op}{fname}({a_exprs})'.format(
        obj_op=obj_op, fname=f['name'], a_exprs=', '.join(a_exprs)
    )
    r_type, r_expr, r_incs = replace_return(f)
    r_expr = r_expr.format(inner_expr)
    head = '{r_type} {fname}({{}})'.format(r_type=r_type, fname=f['name'])
    return {
        'fwd': head.format(', '.join(a_lines_nodef)),
        'head': head.format(', '.join(a_lines)),
        'body': r_expr,
        'sign': {'rtype': r_type, 'args': ', '.join(a_sigs)},
        'incs': a_incs | r_incs,
        'rtype': r_type,
        'head_nortype': '{fname}({args})'.format(fname=f['name'], args=', '.join(a_lines)),
    }


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
    methods, includes = [], {f.header_file_name()}
    for func in lines_to_statements(f.lines()):
        fnc = parse_func(func)
        try:
            fobj = fmt_func(fnc, '->')
        except AssertionError as e:
            print(e, file=stderr)
        else:
            ma(fnc, fobj['sign'])
            methods.append(fobj)
            includes |= fobj['incs']

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

    return {
        'bw_class': f.mapped_class,
        'weakref_class': f.weakref_class(),
        'methods': methods,
        'module_defs': list(ma.assemble()),
        'enums': enums,
        'enum_namespace': f.enum_namespace,
        'make_pointer': f.make_obj_pointer,
        'includes': includes,
    }


class BaseWeakrefFile:
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
        context = file_parser(cls)
        lcl = cls.mapped_class.lower()
        with open(join(GEN_OUTPUT_DIR, 'include', cls.header_file_name()), 'w') as f:
            f.write(html_unescape(jin_env.get_template('weakref/h.jinja2').render(**context)))
        with open(join(GEN_OUTPUT_DIR, 'src', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('weakref/cpp.jinja2').render(**context)))
        with open(join(GEN_OUTPUT_DIR, 'pybind', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('weakref/pybind.jinja2').render(**context)))

    @classmethod
    def header_file_name(cls):
        return '{}.h'.format(cls.mapped_class.lower())

    @classmethod
    def weakref_class(cls):
        return cls.mapped_class + 'Weakref'


class BulletTypeFile(BaseWeakrefFile):
    mapped_class = 'BulletType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::BulletTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'BulletType.h'))
        yield from f(75, 75)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'BulletType.h'))
        yield from f(87, 123)


class DamageTypeFile(BaseWeakrefFile):
    mapped_class = 'DamageType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::DamageTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'DamageType.h'))
        yield from f(48, 48)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'DamageType.h'))
        yield from f(60, 66)


class ExplosionTypeFile(BaseWeakrefFile):
    mapped_class = 'ExplosionType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::ExplosionTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'ExplosionType.h'))
        yield from f(56, 56)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'ExplosionType.h'))
        yield from f(68, 92)


class ForceFile(BaseWeakrefFile):
    mapped_class = 'Force'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Force.h'))
        yield from f(25, 63)


class PlayerFile(BaseWeakrefFile):
    mapped_class = 'Player'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Player.h'))
        yield from f(38, 641)


class PlayerTypeFile(BaseWeakrefFile):
    mapped_class = 'PlayerType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::PlayerTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'PlayerType.h'))
        yield from f(45, 57)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'PlayerType.h'))
        yield from f(68, 78)


class RaceFile(BaseWeakrefFile):
    mapped_class = 'Race'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::Races'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Race.h'))
        yield from f(46, 87)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Race.h'))
        yield from f(98, 103)


class TechTypeFile(BaseWeakrefFile):
    mapped_class = 'TechType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::TechTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'TechType.h'))
        yield from f(79, 154)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'TechType.h'))
        yield from f(165, 210)


class UnitFile(BaseWeakrefFile):
    mapped_class = 'Unit'

    @staticmethod
    def lines():
        with open(join(BWAPI_INCLUDE_DIR, 'Unit.h')) as f:
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


class UnitCommandTypeFile(BaseWeakrefFile):
    mapped_class = 'UnitCommandType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::UnitCommandTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UnitCommandType.h'))
        yield from f(77, 77)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UnitCommandType.h'))
        yield from f(89, 134)


class UnitTypeFile(BaseWeakrefFile):
    mapped_class = 'UnitType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::UnitTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UnitType.h'))
        yield from f(279, 902)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UnitType.h'))
        yield from f(951, 1234)


class UpgradeTypeFile(BaseWeakrefFile):
    mapped_class = 'UpgradeType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::UpgradeTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UpgradeType.h'))
        yield from f(93, 172)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'UpgradeType.h'))
        yield from f(183, 245)


class WeaponTypeFile(BaseWeakrefFile):
    mapped_class = 'WeaponType'
    make_obj_pointer = True
    enum_namespace = 'BWAPI::WeaponTypes'

    @staticmethod
    def lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'WeaponType.h'))
        yield from f(153, 305)

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'WeaponType.h'))
        yield from f(330, 439)
