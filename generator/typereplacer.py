from .cdumper import fmt_arg, arg_type_for_signature
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


def replace_arg(a, sig_prepend_ns=False, line_prepend_ns=False):
    '''Fix incoming argument

    void doSomething(int a, Unit u);

    Returns:
    1. Argument line for binding wrapper, e.g.
        'int a'
        'UnitWeakref u'
    2. Argument transform expression, for passing into inner function, e.g.
        'a'
        'u.obj'
    3. Argument transform code, serving intermediate data for expression above, e.g.
        'Unit temp_obj = database->fetch_by_id(u.id);\ntemp_obj->reindex();'
    4. Argument signature to assemble method/function type, e.g.
        'int'
        'UnitWeakref'
    5. Same as 1, but without default values.
    6. Set of include files to deal with mentioned types.
    '''
    sig_ns = get_ns_prepend(a) if sig_prepend_ns else None
    line_ns = get_ns_prepend(a) if line_prepend_ns else None

    if a['type'] in PRIMITIVE_TYPES:
        return (
            fmt_arg(a, ns=line_ns),
            a['name'],
            None,
            arg_type_for_signature(a, ns=sig_ns),
            fmt_arg(a, ns=line_ns, opt_value=False),
            set()
        )
    if a['const'] and a['type'] in CONST_PRIMITIVE_TYPES:
        return (
            fmt_arg(a, ns=line_ns),
            a['name'],
            None,
            arg_type_for_signature(a, ns=sig_ns),
            fmt_arg(a, ns=line_ns, opt_value=False),
            set()
        )
    if a['type'] in WEAKREF_MAP:
        assert not a['const'], 'Const arguments not supported in weakref types ' + repr(a)
        assert a['opt_value'] is None, 'Value defaults not supported in weakref types ' + repr(a)
        na = a.copy()
        na['type'] = WEAKREF_MAP[a['type']]
        ptr = '*' if a['type'] in POINTER_FORCE_TYPES else ''
        return (
            fmt_arg(na, ns=line_ns),
            ptr + na['name'] + '.obj',
            None,
            arg_type_for_signature(na, ns=sig_ns),
            fmt_arg(na, ns=line_ns, opt_value=False),
            {INCLUDE_MAP[a['type']]}
        )
    if a['type'] in POSITION_TYPES:
        na = a.copy()
        na['type'] = 'UniversalPosition'
        return (
            fmt_arg(na, ns=line_ns),
            'BWAPI::{point}({name}[0], {name}[1])'.format(point=a['type'], name=na['name']),
            None,
            arg_type_for_signature(na, ns=sig_ns),
            fmt_arg(na, ns=line_ns, opt_value=False),
            set()
        )
    assert False, 'Bad argument ' + repr(a)


def replace_all_args(f, **kw):
    if not f['args']:
        return (), (), (), (), (), set()
    fun = partial(replace_arg, **kw)
    result = list(zip(*map(fun, f['args'])))
    result.append(set.union(*result.pop()))
    return tuple(result)


def replace_return(f, prepend_ns=False):
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
        'return UnitWeakref({});'
        'return PyBinding::set_converter<PyBinding::ForceWeakref, BWAPI::Forceset>({});'
    3. Set of include files to deal with mentioned types.
    '''
    if f['rtype'] == 'void':
        return 'void', '{};', set()
    if f['rtype'] in PRIMITIVE_TYPES:
        return f['rtype'], 'return {};', set()
    if f['rtype'].startswith('const '):
        mt = f['rtype'].split(' ', 1)[1].lstrip()
        if mt in CONST_PRIMITIVE_TYPES:
            return f['rtype'], 'return {};', set()
    if f['rtype'] in WEAKREF_MAP:
        wt = WEAKREF_MAP[f['rtype']]
        if prepend_ns:
            wt = 'PyBinding::' + wt
        ptr = '&' if f['rtype'] in POINTER_FORCE_TYPES else ''
        return wt, 'return {wt}({p}{{}});'.format(wt=wt, p=ptr), {INCLUDE_MAP[f['rtype']]}
    if f['rtype'] in WEAKREF_SET_MAP:
        base_t = WEAKREF_SET_MAP[f['rtype']]
        wt = WEAKREF_MAP[base_t]
        sc = 'ptr_set_converter' if base_t in POINTER_FORCE_TYPES else 'set_converter'
        if prepend_ns:
            wt = 'PyBinding::' + wt
            sc = 'PyBinding::' + sc
        return (
            'py::set',
            'return {sc}<{wt}, {bwt}>({{}});'.format(
                sc=sc, wt=wt, bwt=WEAKREF_SET_REV_MAP[base_t]
            ),
            {INCLUDE_MAP[base_t]}
        )
    if f['rtype'] in POSITION_TYPES:
        rt = 'UniversalPosition'
        sc = 'convert_position'
        if prepend_ns:
            rt = 'PyBinding::' + rt
            sc = 'PyBinding::' + sc
        return (
            rt,
            'return {sc}<BWAPI::{tpoint}>({{}});'.format(sc=sc, tpoint=f['rtype']),
            set()
        )
    assert False, 'Bad return type ' + repr(f)
