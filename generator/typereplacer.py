from .cdumper import fmt_arg
from functools import partial
from . import weakrefs


# http://pybind11.readthedocs.io/en/latest/basics.html#supported-data-types
PRIMITIVE_TYPES = {
    'int8_t', 'uint8_t', 'int16_t', 'uint16_t', 'int32_t', 'uint32_t', 'int64_t', 'uint64_t',
    'ssize_t', 'size_t', 'float', 'double', 'bool', 'char', 'wchar_t', 'std::string', 'std::wstring', 'int'
}

CONST_PRIMITIVE_TYPES = {
    'char *', 'wchar_t *', 'std::string &',
}

WEAKREF_MAP = {}
POINTER_FORCE_TYPES = set()
INCLUDE_MAP = {}

for Sub in weakrefs.BaseWeakrefFile.__subclasses__():
    WEAKREF_MAP[Sub.mapped_class] = Sub.weakref_class()
    if Sub.make_obj_pointer:
        POINTER_FORCE_TYPES.add(Sub.mapped_class)
    INCLUDE_MAP[Sub.mapped_class] = Sub.header_file_name()

POSITION_TYPES = {'Position', 'WalkPosition', 'TilePosition'}

# return types only
WEAKREF_SET_MAP = {
    'Bulletset': 'Bullet',

    'Forceset': 'Force',
    'const Forceset&': 'Force',
    'const Forceset &': 'Force',

    'Playerset': 'Player',
    'Playerset&': 'Player',
    'const Playerset&': 'Player',
    'const Playerset &': 'Player',

    'Unitset': 'Unit',
    'const Unitset&': 'Unit',
    'const Unitset &': 'Unit',

    'const UnitType::set&': 'UnitType',
    'const SetContainer<TechType>&': 'TechType',
    'const SetContainer<UpgradeType>&': 'UpgradeType',
}
# from multiple ways choose single TODO
# this is used to cast via set_converter only
WEAKREF_SET_REV_MAP = {
    'Unit': 'BWAPI::Unitset',
    'Force': 'BWAPI::Forceset',
    'Player': 'BWAPI::Playerset',
    'Bullet': 'BWAPI::Bulletset',
    'UnitType': 'BWAPI::UnitType::set',
    'TechType': 'BWAPI::SetContainer<BWAPI::TechType>',
    'UpgradeType': 'BWAPI::SetContainer<BWAPI::UpgradeType>',
}


def get_ns_prepend(a):
    if a['type'] in WEAKREF_MAP or a['type'] in POSITION_TYPES:
        return 'PyBinding::'
    return None


def replace_arg(a):
    '''Fix incoming argument

    void doSomething(int a, Unit u);

    Returns:
    newa, expr, code, incls, use_ns
    1. Transformed argument data, e.g.
        {'name': 'a', 'type': 'int'}
    2. Argument transform expression, for passing into inner function, e.g.
        'a'
        'u.obj'
    3. Argument transform code, serving intermediate data for expression above, e.g.
        'Unit temp_obj = database->fetch_by_id(u.id);\ntemp_obj->reindex();'
    4. Set of include files to deal with mentioned types.
    5. Boolean value whether an argument exists in PyBinding:: namespace.
    '''
    if (a['type'] in PRIMITIVE_TYPES) or (a['const'] and a['type'] in CONST_PRIMITIVE_TYPES):
        return a, a['name'], None, set(), False
    if a['type'] in WEAKREF_MAP:
        assert not a['const'], 'Const arguments not supported in weakref types ' + repr(a)
        assert a['opt_value'] is None, 'Value defaults not supported in weakref types ' + repr(a)
        na = a.copy()
        na['type'] = WEAKREF_MAP[a['type']]
        ptr = '*' if a['type'] in POINTER_FORCE_TYPES else ''
        expr = ptr + na['name'] + '.obj'
        return na, expr, None, {INCLUDE_MAP[a['type']]}, True
    if a['type'] in POSITION_TYPES:
        na = a.copy()
        na['type'] = 'UniversalPosition'
        expr = 'BWAPI::{point}({name}[0], {name}[1])'.format(point=a['type'], name=na['name'])
        return na, expr, None, set(), True
    assert False, 'Bad argument ' + repr(a)


def replace_arg_wrap(a, sig_prepend_ns=False, line_prepend_ns=False):
    newa, expr, code, incls, use_ns = replace_arg(a)
    sig_ns = 'PyBinding::' if sig_prepend_ns and use_ns else None
    line_ns = 'PyBinding::' if line_prepend_ns and use_ns else None
    return (
        fmt_arg(newa, ns=line_ns),
        expr,
        code,
        fmt_arg(newa, opt_value=False, name=False, ns=sig_ns),
        fmt_arg(newa, opt_value=False, ns=line_ns),
        incls
    )


def replace_all_args(f, **kw):
    if not f['args']:
        return (), (), (), (), (), set()
    fun = partial(replace_arg_wrap, **kw)
    result = list(zip(*map(fun, f['args'])))
    result.append(set.union(*result.pop()))
    return tuple(result)


def replace_return_raw(f):
    '''Fix return value

    void doSomething();
    Unit getUnit();
    Forceset allies();

    Returns:
    1. Return type for binding wrapper, e.g.
        'void'
        'UnitWeakref'
        'py::set'
    2. Value transform expression/code, for passing into inner functions, e.g.
        None
        'return UnitWeakref({expr});'
        'return {ns}set_converter<{ns}ForceWeakref, BWAPI::Forceset>({expr});'
    3. Set of include files to deal with mentioned types.
    '''
    if f['rtype'] == 'void':
        return 'void', '{expr};', set()
    if f['rtype'] in PRIMITIVE_TYPES:
        return f['rtype'], 'return {expr};', set()
    if f['rtype'].startswith('const '):
        mt = f['rtype'].split(' ', 1)[1].lstrip()
        if mt in CONST_PRIMITIVE_TYPES:
            return f['rtype'], 'return {expr};', set()
    if f['rtype'] in WEAKREF_MAP:
        wt = WEAKREF_MAP[f['rtype']]
        ptr = '&' if f['rtype'] in POINTER_FORCE_TYPES else ''
        expr = 'return {{ns}}{wt}({p}{{expr}});'.format(wt=wt, p=ptr)
        return '{ns}' + wt, expr, {INCLUDE_MAP[f['rtype']]}
    if f['rtype'] in WEAKREF_SET_MAP:
        base_t = WEAKREF_SET_MAP[f['rtype']]
        wt = WEAKREF_MAP[base_t]
        sc = 'ptr_set_converter' if base_t in POINTER_FORCE_TYPES else 'set_converter'
        expr = 'return {{ns}}{sc}<{{ns}}{wt}, {bwt}>({{expr}});'.format(
            sc=sc, wt=wt, bwt=WEAKREF_SET_REV_MAP[base_t]
        )
        return 'py::set', expr, {INCLUDE_MAP[base_t]}
    if f['rtype'] in POSITION_TYPES:
        return (
            '{ns}UniversalPosition',
            'return {{ns}}convert_position<BWAPI::{tpoint}>({{expr}});'.format(tpoint=f['rtype']),
            set()
        )
    assert False, 'Bad return type ' + repr(f)


def replace_return(f, prepend_ns=False):
    rtype, expr, incls = replace_return_raw(f)
    ns = 'PyBinding::' if prepend_ns else ''
    return rtype.format(ns=ns), expr.format(ns=ns, expr='{}'), incls
