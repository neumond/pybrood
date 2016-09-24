from copy import deepcopy

# http://pybind11.readthedocs.io/en/latest/basics.html#supported-data-types
PRIMITIVE_TYPES = {
    'int8_t', 'uint8_t', 'int16_t', 'uint16_t', 'int32_t', 'uint32_t', 'int64_t', 'uint64_t',
    'ssize_t', 'size_t', 'float', 'double', 'bool', 'char', 'wchar_t', 'std::string', 'std::wstring', 'int'
}
CONST_PRIMITIVE_TYPES = {
    'char *', 'wchar_t *',
}
CONST_REF_PRIMITIVE_TYPES = {
    'std::string',
}
CONST_BWAPI_TYPES = {
    'std::pair< {bwapi}UnitType, int >',
}
CONST_REF_BWAPI_TYPES = {
    '{bwapi}UnitType::set',
    'std::map< {bwapi}UnitType, int >',
    '{bwapi}SetContainer<{bwapi}TechType>',
    '{bwapi}SetContainer<{bwapi}UpgradeType>',
    '{bwapi}Forceset',
    '{bwapi}Playerset',
    '{bwapi}Unitset',
    '{bwapi}Bulletset',
}

POSITION_TYPES = {'Position', 'WalkPosition', 'TilePosition'}

# return types only
WEAKREF_SET_MAP = {
    # 'Bulletset': 'Bullet',
    #
    # 'Forceset': 'Force',
    # 'const Forceset&': 'Force',
    # 'const Forceset &': 'Force',
    #
    # 'Playerset': 'Player',
    # 'Playerset&': 'Player',
    # 'const Playerset&': 'Player',
    # 'const Playerset &': 'Player',
    #
    # 'Unitset': 'Unit',
    # 'const Unitset&': 'Unit',
    # 'const Unitset &': 'Unit',
    #
    # 'const UnitType::set&': 'UnitType',
    # 'const SetContainer<TechType>&': 'TechType',
    # 'const SetContainer<UpgradeType>&': 'UpgradeType',
}
# from multiple ways choose single TODO
# this is used to cast via set_converter only
WEAKREF_SET_REV_MAP = {
    # 'Unit': 'BWAPI::Unitset',
    # 'Force': 'BWAPI::Forceset',
    # 'Player': 'BWAPI::Playerset',
    # 'Bullet': 'BWAPI::Bulletset',
    # 'UnitType': 'BWAPI::UnitType::set',
    # 'TechType': 'BWAPI::SetContainer<BWAPI::TechType>',
    # 'UpgradeType': 'BWAPI::SetContainer<BWAPI::UpgradeType>',
}


ARGUMENT_TYPES = {}
CONST_ARGUMENT_TYPES = {}
AS_IS_ARGUMENT_TYPES = {}
AS_IS_CONST_ARGUMENT_TYPES = {}
# inplace argument transformer, expression maker, code maker, includes, transformed
_NO_ACTION_ARGUMENT = (lambda a: None, lambda a: a['name'], None, set(), False)

RETURN_TYPES = {}
CONST_RETURN_TYPES = {}
AS_IS_RETURN_TYPES = {}
AS_IS_CONST_RETURN_TYPES = {}
# inplace function transformer, expression, includes, transformed
_NO_ACTION_RETURN = (lambda f: None, lambda f: 'return {expr};', set(), False)


def _arg_bwapi_appender():
    def arg_transformer(a):
        a['type'] = 'BWAPI::' + a['type']
        if a['opt_value'] is not None and '::' in a['opt_value']:
            a['opt_value'] = 'BWAPI::' + a['opt_value']
    return arg_transformer, lambda a: a['name'], None, set(), False


def _ret_bwapi_appender():
    def ret_transformer(f):
        f['rtype'] = 'BWAPI::' + f['rtype']
    return ret_transformer, lambda f: 'return {expr};', set(), False


def _arg_position():
    def arg_transformer(a):
        a['type'] = 'PyBinding::UniversalPosition'
        if a['opt_value'] is not None and '::' in a['opt_value']:
            a['opt_value'] = 'PyBinding::' + a['opt_value']

    def arg_expr(a):
        return 'BWAPI::{point}({name}[0], {name}[1])'.format(point=a['type'], name=a['name'])
    return arg_transformer, arg_expr, None, set(), True


def _ret_position():
    def ret_transformer(f):
        f['rtype'] = 'PyBinding::UniversalPosition'

    def ret_expr(f):
        return 'return PyBinding::convert_position<BWAPI::{tpoint}>({{expr}});'.format(tpoint=f['rtype'])
    return ret_transformer, ret_expr, set(), True


def register_types():
    RETURN_TYPES['void'] = (lambda f: None, lambda f: '{expr};', set(), False)
    AS_IS_RETURN_TYPES['void'] = (lambda f: None, lambda f: '{expr};', set(), False)

    for t in PRIMITIVE_TYPES:
        ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        CONST_ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        RETURN_TYPES[t] = _NO_ACTION_RETURN
        CONST_RETURN_TYPES[t] = _NO_ACTION_RETURN

        AS_IS_ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        AS_IS_CONST_ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        AS_IS_RETURN_TYPES[t] = _NO_ACTION_RETURN
        AS_IS_CONST_RETURN_TYPES[t] = _NO_ACTION_RETURN

    for t in CONST_PRIMITIVE_TYPES:
        CONST_ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        CONST_RETURN_TYPES[t] = _NO_ACTION_RETURN

        AS_IS_CONST_ARGUMENT_TYPES[t] = _NO_ACTION_ARGUMENT
        AS_IS_CONST_RETURN_TYPES[t] = _NO_ACTION_RETURN

    for t in CONST_REF_PRIMITIVE_TYPES:
        for s in ('&', ' &'):
            tt = t + s
            CONST_ARGUMENT_TYPES[tt] = _NO_ACTION_ARGUMENT
            CONST_RETURN_TYPES[tt] = _NO_ACTION_RETURN

            AS_IS_CONST_ARGUMENT_TYPES[tt] = _NO_ACTION_ARGUMENT
            AS_IS_CONST_RETURN_TYPES[tt] = _NO_ACTION_RETURN

    for t in CONST_BWAPI_TYPES:
        tname = t.format(bwapi='')
        CONST_ARGUMENT_TYPES[tname] = _NO_ACTION_ARGUMENT
        CONST_RETURN_TYPES[tname] = _NO_ACTION_RETURN

        AS_IS_CONST_ARGUMENT_TYPES[tname] = _NO_ACTION_ARGUMENT
        AS_IS_CONST_RETURN_TYPES[tname] = _NO_ACTION_RETURN

    for t in CONST_REF_BWAPI_TYPES:
        for s in ('&', ' &'):
            tt = (t + s).format(bwapi='')
            CONST_ARGUMENT_TYPES[tt] = _NO_ACTION_ARGUMENT
            CONST_RETURN_TYPES[tt] = _NO_ACTION_RETURN

            AS_IS_CONST_ARGUMENT_TYPES[tt] = _NO_ACTION_ARGUMENT
            AS_IS_CONST_RETURN_TYPES[tt] = _NO_ACTION_RETURN

    from . import classes
    from . import bwapi_classes  # noqa

    for Sub in classes.BaseClassFile.__subclasses__():
        if Sub is not classes.BaseWrappedClassFile:
            t = Sub.mapped_class
            ARGUMENT_TYPES[t] = _arg_bwapi_appender()
            CONST_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
            RETURN_TYPES[t] = _ret_bwapi_appender()
            CONST_RETURN_TYPES[t] = _ret_bwapi_appender()

            AS_IS_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
            AS_IS_CONST_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
            AS_IS_RETURN_TYPES[t] = _ret_bwapi_appender()
            AS_IS_CONST_RETURN_TYPES[t] = _ret_bwapi_appender()
    for Sub in classes.BaseWrappedClassFile.__subclasses__():
        t = Sub.mapped_class
        ARGUMENT_TYPES[t] = (Sub.arg_transformer, Sub.arg_expr, None, {Sub.include_file()}, True)
        CONST_ARGUMENT_TYPES[t] = (Sub.arg_transformer, Sub.arg_expr, None, {Sub.include_file()}, True)
        RETURN_TYPES[t] = (Sub.ret_transformer, Sub.ret_expr, {Sub.include_file()}, True)
        CONST_RETURN_TYPES[t] = (Sub.ret_transformer, Sub.ret_expr, {Sub.include_file()}, True)

        AS_IS_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
        AS_IS_CONST_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
        AS_IS_RETURN_TYPES[t] = _ret_bwapi_appender()
        AS_IS_CONST_RETURN_TYPES[t] = _ret_bwapi_appender()

    for t in ('Position', 'WalkPosition', 'TilePosition'):
        ARGUMENT_TYPES[t] = _arg_position()
        CONST_ARGUMENT_TYPES[t] = _arg_position()
        RETURN_TYPES[t] = _ret_position()
        CONST_RETURN_TYPES[t] = _ret_position()

        AS_IS_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
        AS_IS_CONST_ARGUMENT_TYPES[t] = _arg_bwapi_appender()
        AS_IS_RETURN_TYPES[t] = _ret_bwapi_appender()
        AS_IS_CONST_RETURN_TYPES[t] = _ret_bwapi_appender()


def fmt_arg(a, opt_value=True, name=True):
    result = a['type']
    if name:
        result += ' ' + a['name']
    if opt_value and a['opt_value'] is not None:
        result += ' = {}'.format(a['opt_value'])
    if a['const']:
        result = 'const ' + result
    return result


def replace_arg(a, asis=False):
    '''Fix incoming argument

    void doSomething(int a, Unit u);

    Returns:
    newa, expr, code, incls, use_ns
    1. Transformed argument data, e.g.
        {'name': 'a', 'type': 'int'}
        {'name': 'b', 'type': '{ns}MyType'}
    2. Argument transform expression, for passing into inner function, e.g.
        'a'
        'u.obj'
    3. Argument transform code, serving intermediate data for expression above, e.g.
        'Unit temp_obj = database->fetch_by_id(u.id);\ntemp_obj->reindex();'
    4. Set of include files to deal with mentioned types.

    {ns} is intended to be used with .format(ns='MyNamespace::')
    All string values except include files can contain it.

    or

    None
    if no transformation is needed
    equivalent to
    (a, a['name'], None, set())
    '''

    if asis:
        storage = AS_IS_CONST_ARGUMENT_TYPES if a['const'] else AS_IS_ARGUMENT_TYPES
    else:
        storage = CONST_ARGUMENT_TYPES if a['const'] else ARGUMENT_TYPES
    assert a['type'] in storage, 'bad argument type ' + repr(a)
    arg_transformer, expr_maker, code_maker, includes, transformed = storage[a['type']]
    newa = deepcopy(a)
    arg_transformer(newa)
    return newa, expr_maker(a), None if code_maker is None else code_maker(a), includes, transformed


def replace_all_args(f, asis=False):
    transformed = False
    all_incls = set()
    full_code, all_exprs, all_args = [], [], []
    for a in f['args']:
        newa, expr, code, incls, tup = replace_arg(a, asis=asis)
        transformed |= tup
        if code is not None:
            full_code.extend(code.split('\n'))
        all_incls |= incls
        all_exprs.append(expr)
        all_args.append(newa)

    return {
        'transformed': transformed,
        'includes': all_incls,
        # all lines below need .format(ns=...)
        'expression': ', '.join(all_exprs),
        'code': '\n'.join(full_code),
        'argline_full': ', '.join(fmt_arg(a) for a in all_args),
        'argline_nodefaults': ', '.join(fmt_arg(a, opt_value=False) for a in all_args),
        'argline_signature': ', '.join(fmt_arg(a, opt_value=False, name=False) for a in all_args),
    }


def replace_return(f, asis=False):
    '''Fix return value

    void doSomething();
    Unit getUnit();
    Forceset allies();

    Returns:
    1. Return type for binding wrapper, e.g.
        'void'
        '{ns}UnitWeakref'
        'py::set'
    2. Value transform expression/code, for passing into inner functions, e.g.
        'return UnitWeakref({expr});'
        'return {ns}set_converter<{ns}ForceWeakref, BWAPI::Forceset>({expr});'
    3. Set of include files to deal with mentioned types.
    4. Boolean flag if function needs transformation
    '''
    if asis:
        storage = AS_IS_CONST_RETURN_TYPES if f['rconst'] else AS_IS_RETURN_TYPES
    else:
        storage = CONST_RETURN_TYPES if f['rconst'] else RETURN_TYPES
    assert f['rtype'] in storage, 'bad return type ' + repr(f)
    ret_transformer, expr_maker, includes, transformed = storage[f['rtype']]
    newf = deepcopy(f)
    ret_transformer(newf)
    return newf, expr_maker(f), includes, transformed

    # if f['rtype'] in WRAPPED_SET:
    #     wt = WRAPPED_SET[f['rtype']]
    #     expr = 'return {{ns}}{wt}({{expr}});'.format(wt=wt)
    #     return '{ns}' + wt, expr, set(), True
    # if f['rtype'] in WEAKREF_SET_MAP:
    #     base_t = WEAKREF_SET_MAP[f['rtype']]
    #     wt = WRAPPED_SET[base_t]
    #     # sc = 'ptr_set_converter' if base_t in POINTER_FORCE_TYPES else 'set_converter'
    #     sc = 'set_converter'
    #     expr = 'return {{ns}}{sc}<{{ns}}{wt}, {bwt}>({{expr}});'.format(
    #         sc=sc, wt=wt, bwt=WEAKREF_SET_REV_MAP[base_t]
    #     )
    #     return 'py::set', expr, set(), True
    # if f['rtype'] in POSITION_TYPES:
    #     return (
    #         '{ns}UniversalPosition',
    #         'return {{ns}}convert_position<BWAPI::{tpoint}>({{expr}});'.format(tpoint=f['rtype']),
    #         set(), True
    #     )
    # assert False, 'Bad return type ' + repr(f)


def process_function(f, obj_op_line, asis=False):
    '''
    obj_op_line examples:
    'obj->{fname}({args})'
    '{fname}({args})'
    'obj.{fname}({args})'
    '''
    argrep = replace_all_args(f, asis=asis)
    result = {'name': f['name']}
    newf, retexpr, result['includes'], result['transformed'] = replace_return(f, asis=asis)
    result['rettype'] = newf['rtype']
    if newf['rconst']:
        result['rettype'] = 'const ' + result['rettype']
    result['transformed'] |= argrep['transformed']
    result['includes'] |= argrep['includes']
    result['func_body'] = (argrep['code'] + '\n' + retexpr.format(
        expr=obj_op_line.format(args=argrep['expression'], fname=f['name'], ns='{ns}'),
        ns='{ns}'
    )).strip()
    for k in ('argline_full', 'argline_nodefaults', 'argline_signature'):
        result[k] = argrep[k]
    return result


# === new api ===


def transform_input_type(vtype, const=False):
    if vtype in PRIMITIVE_TYPES:
        return


def transform_output_type(vtype, const=False):
    pass
