from .cdumper import fmt_arg, arg_type_for_signature
from functools import partial


# http://pybind11.readthedocs.io/en/latest/basics.html#supported-data-types
PRIMITIVE_TYPES = {
    'int8_t', 'uint8_t', 'int16_t', 'uint16_t', 'int32_t', 'uint32_t', 'int64_t', 'uint64_t',
    'ssize_t', 'size_t', 'float', 'double', 'bool', 'char', 'wchar_t', 'std::string', 'std::wstring', 'int'
}

CONST_PRIMITIVE_TYPES = {
    'char *', 'wchar_t *'
}

WEAKREF_MAP = {
    'Force': 'ForceWeakref',
    'Player': 'PlayerWeakref',
    'Unit': 'UnitWeakref',
    'UnitType': 'UnitTypeWeakref',
    'BulletType': 'BulletTypeWeakref',
    'DamageType': 'DamageTypeWeakref',
    'UpgradeType': 'UpgradeTypeWeakref',
    'WeaponType': 'WeaponTypeWeakref',
    'PlayerType': 'PlayerTypeWeakref',
}

POINTER_FORCE_TYPES = {
    'UnitType',
    'BulletType',
    'DamageType',
    'UpgradeType',
    'WeaponType',
    'PlayerType',
}

# return types only
WEAKREF_SET_MAP = {
    'Forceset': 'Force',
    'Playerset': 'Player',
    'Unitset': 'Unit',
    'const Unitset&': 'Unit',
    'const Unitset &': 'Unit',
    'const Forceset&': 'Force',
    'const Forceset &': 'Force',
    'const Playerset&': 'Player',
    'const Playerset &': 'Player',
    # 'const UnitType::set&': 'UnitType',
}
WEAKREF_SET_REV_MAP = {
    'Unit': 'Unitset',
    'Force': 'Forceset',
    'Player': 'Playerset',
    # 'UnitType': 'UnitType::set',
}


def get_ns_prepend(a):
    if a['type'] in WEAKREF_MAP:
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
    '''
    sig_ns = get_ns_prepend(a) if sig_prepend_ns else None
    line_ns = get_ns_prepend(a) if line_prepend_ns else None

    if a['type'] in PRIMITIVE_TYPES:
        return fmt_arg(a, ns=line_ns), a['name'], None, arg_type_for_signature(a, ns=sig_ns)
    if a['const'] and a['type'] in CONST_PRIMITIVE_TYPES:
        return fmt_arg(a, ns=line_ns), a['name'], None, arg_type_for_signature(a, ns=sig_ns)
    if a['type'] in WEAKREF_MAP:
        assert not a['const'], 'Const arguments not supported in weakref types ' + repr(a)
        assert a['opt_value'] is None, 'Value defaults not supported in weakref types ' + repr(a)
        na = a.copy()
        na['type'] = WEAKREF_MAP[a['type']]
        ptr = '*' if a['type'] in POINTER_FORCE_TYPES else ''
        return fmt_arg(na, ns=line_ns), ptr + na['name'] + '.obj', None, arg_type_for_signature(na, ns=sig_ns)
    assert False, 'Bad argument ' + repr(a)


def replace_all_args(f, **kw):
    if not f['args']:
        return (), (), (), ()
    fun = partial(replace_arg, **kw)
    return zip(*map(fun, f['args']))


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
    '''
    if f['rtype'] == 'void':
        return 'void', '{};'
    if f['rtype'] in PRIMITIVE_TYPES:
        return f['rtype'], 'return {};'
    if f['rtype'] in WEAKREF_MAP:
        wt = WEAKREF_MAP[f['rtype']]
        if prepend_ns:
            wt = 'PyBinding::' + wt
        ptr = '&' if f['rtype'] in POINTER_FORCE_TYPES else ''
        return wt, 'return {wt}({p}{{}});'.format(wt=wt, p=ptr)
    if f['rtype'] in WEAKREF_SET_MAP:
        base_t = WEAKREF_SET_MAP[f['rtype']]
        wt = WEAKREF_MAP[base_t]
        if prepend_ns:
            wt = 'PyBinding::' + wt
        return 'py::set', 'return PyBinding::set_converter<{wt}, BWAPI::{bwt}>({{}});'.format(
            wt=wt, bwt=WEAKREF_SET_REV_MAP[base_t]
        )
    assert False, 'Bad return type ' + repr(f)
