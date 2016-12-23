from os import mkdir, listdir
from os.path import join, isdir, relpath
from collections import defaultdict
from copy import deepcopy
from pathlib import PureWindowsPath
from shutil import rmtree

from .config import GEN_OUTPUT_DIR, BWAPI_DIR, PYBIND_DIR
from .utils import render_template, split_to_well_sized_lines
from .parser import parse_pureenums, parse_classes, parse_objenums
from .proxy_replacements import MethodDiscarded, get_replacement
from .common import atype_or_dots, get_full_argtype, get_full_rettype
from .typereplacer2 import arg_replacer, NoReplacement
from .additional import improve_container_class


NODELETE_CLASSES = {'Client', 'Bullet', 'Force', 'Player', 'Region', 'Unit'}
UNPOINTED_CLASSES = {
    'Bullet': 'BulletInterface',
    'Force': 'ForceInterface',
    'Player': 'PlayerInterface',
    'Region': 'RegionInterface',
    'Unit': 'UnitInterface',
}
FILTER_TYPES = {'UnitFilter', 'UnitFilter &'}
UNITCOMMAND_TYPES = {'UnitCommand'}
ITERABLE_CLASSES = {'Bulletset', 'Forceset', 'Playerset', 'Regionset', 'Unitset'}


def duplicate_for_position_or_unit(class_data):
    methods = []
    for func in class_data['methods']:
        pu = False
        for i, a in enumerate(func['args']):
            if a['type'] == 'PositionOrUnit':
                assert pu is False
                a['PositionOrUnit'] = True
                pu = i
        if pu is False:
            methods.append(func)
        else:
            f1, f2 = deepcopy(func), deepcopy(func)
            f1['args'][pu]['type'] = 'Position'
            f2['args'][pu]['type'] = 'Unit'
            if func['args'][pu]['opt_value'] is not None:
                assert func['args'][pu]['opt_value'] == 'nullptr', repr(func)
                f1['args'][pu]['opt_value'] = 'Positions::Unknown'
                f2['args'][pu]['opt_value'] = 'nullptr'
            methods.append(f1)
            methods.append(f2)
    class_data['methods'] = methods


def remove_everything_with_required_filter(class_data):
    methods = []
    for func in class_data['methods']:
        if not any(a['type'] in FILTER_TYPES and a['opt_value'] is None for a in func['args']):
            methods.append(func)
    class_data['methods'] = methods


def remove_everything_with_required_unitcommand(class_data):
    methods = []
    for func in class_data['methods']:
        if not any(a['type'] in UNITCOMMAND_TYPES and a['opt_value'] is None for a in func['args']):
            methods.append(func)
    class_data['methods'] = methods


def collect_type_list(class_data):
    result = set()
    for func in class_data['methods']:
        result.add(func['rtype'])
        for a in func['args']:
            result.add(a['type'])
    return result


def make_overload_signature(func, class_name):
    argline = ', '.join(atype_or_dots(a) for a in func['args'])
    r = '{} ({}::*)({})'.format(get_full_rettype(func), class_name, argline)
    if func['selfconst']:
        r += ' const'
    return r


def make_overload_signatures(class_data, class_name):
    counts = defaultdict(lambda: 0)
    for func in class_data['methods']:
        counts[func['name']] += 1
    over_meths = {name for name, c in counts.items() if c > 1}

    for func in class_data['methods']:
        if func['name'] in over_meths:
            func['overload_signature'] = make_overload_signature(func, class_name)


WELL_SIZED_LINE = 80


def smart_arg_join(lines, gap):
    joined_lines = split_to_well_sized_lines(lines, WELL_SIZED_LINE, ', ')
    s_lines = (',\n    ' + gap).join(joined_lines)
    if len(joined_lines) > 1:
        s_lines = '\n    ' + gap + s_lines + '\n' + gap
    return s_lines


def make_lambda_overload(class_name, func, force=False, game=False):
    input_lines, call_lines = [], []
    if not game:
        input_lines.append('{}& instance'.format(class_name))
    has_any_replacement = force
    call_line_map = {}
    for a in func['args']:
        try:
            i, c = arg_replacer(a)
            has_any_replacement = True
        except NoReplacement:
            i = '{} {}'.format(get_full_argtype(a), a['name'])
            c = a['name']
        if a.get('PositionOrUnit'):
            has_any_replacement = True
        if i is not None:
            input_lines.append(i)
        else:
            a['RemoveFromDefaults'] = True
        call_lines.append(c)
        call_line_map[a['name']] = c

    if not has_any_replacement and 'custom_body' not in func:
        raise NoReplacement

    s_input_lines = smart_arg_join(input_lines, '')
    s_call_lines = smart_arg_join(call_lines, '    ')

    if 'custom_body' in func:
        body = func['custom_body'].format(**call_line_map)
    else:
        body = '{return_op}{instance}{method_name}({call_args});'.format(
            return_op='' if func['rtype'] == 'void' else 'return ',
            method_name=func['name'],
            call_args=s_call_lines,
            instance='instance.' if not game else 'Broodwar->',
        )

    return (
        '[]({input_args}){lambda_return_type} {{\n'
        '    {body}\n'
        '}}'
    ).format(
        lambda_return_type='' if func['rtype'] == 'void' else ' -> {}'.format(get_full_rettype(func)),
        input_args=s_input_lines,
        body=body,
    )


def make_lambda_overloads(class_data, class_name, force=False, game=False):
    for func in class_data['methods']:
        try:
            func['defcode'] = make_lambda_overload(class_name, func, force=force, game=game)
        except NoReplacement:
            func['defcode'] = '&{}::{}'.format(class_name, func['name'])
            if 'overload_signature' in func:
                func['defcode'] = '({}) {}'.format(func['overload_signature'], func['defcode'])


def custom_replacements(class_data, class_name):
    methods = []
    for func in class_data['methods']:
        try:
            methods.append(get_replacement(func, class_name))
        except MethodDiscarded:
            pass
    class_data['methods'] = methods


DEFAULT_REPLACEMENTS = {
    ('TilePosition', 'TilePositions::None'): ('Pybrood::UniversalPosition', 'Pybrood::TilePositions::None'),
    ('Position', 'Positions::Origin'): ('Pybrood::UniversalPosition', 'Pybrood::Positions::Origin'),
    ('Position', 'Positions::Unknown'): ('Pybrood::UniversalPosition', 'Pybrood::Positions::Unknown'),
}


def make_default_arguments(class_data, class_name, game=False):
    for func in class_data['methods']:
        has_opts = False
        ags = []
        for a in func['args']:
            if a.get('RemoveFromDefaults'):
                continue
            ft = NotImplemented
            if a['opt_value'] is not None:
                ft = (get_full_argtype(a), a['opt_value'])
                repl = DEFAULT_REPLACEMENTS.get(ft)
                if repl is NotImplemented:
                    ft = NotImplemented
                elif repl is not None:
                    ft = repl
            if not (a['opt_value'] is None or ft is NotImplemented):
                ftype, fvalue = ft
                has_opts = True
                cast = '({}) '.format(ftype) if fvalue == 'nullptr' else ''
                ags.append('py::arg("{}") = {}{}'.format(a['name'], cast, fvalue))
            else:
                assert not has_opts
                ags.append('py::arg("{}")'.format(a['name']))
        if has_opts:
            s_lines = split_to_well_sized_lines(ags, WELL_SIZED_LINE, ', ')
            func['defargs'] = (',\n    ' if len(s_lines) > 1 else ', ') + ',\n    '.join(s_lines)


def join_modifiers(class_data):
    for func in class_data['methods']:
        if func.get('modifiers'):
            func['jmods'] = ', ' + ', '.join(func['modifiers'])


def render_pureenums():
    for py_name, v in parse_pureenums().items():
        yield render_template('pureenum.jinja2', py_name=py_name, **v)


def render_classes():
    all_type_list = set()
    all_classes = parse_classes()
    for py_name, v in all_classes.items():
        is_game = py_name == 'Game'
        c = UNPOINTED_CLASSES[py_name] if py_name in UNPOINTED_CLASSES else py_name
        duplicate_for_position_or_unit(v)
        remove_everything_with_required_filter(v)
        remove_everything_with_required_unitcommand(v)
        if py_name in ITERABLE_CLASSES:
            improve_container_class(v)
        make_overload_signatures(v, c)
        custom_replacements(v, c)
        make_lambda_overloads(v, c, force=is_game, game=is_game)
        make_default_arguments(v, c, game=is_game)
        join_modifiers(v)
        all_type_list |= collect_type_list(v)
        if py_name in UNPOINTED_CLASSES:
            v['bw_class_full'] = 'BWAPI::{}'.format(UNPOINTED_CLASSES[py_name])
        yield render_template(
            'game.jinja2' if is_game else 'direct_class.jinja2',
            py_name=py_name,
            nodelete=py_name in NODELETE_CLASSES, **v
        )
    # from pprint import pprint
    # pprint(sorted(all_type_list))


def render_objenums():
    for py_name, v in parse_objenums().items():
        yield render_template('objenum.jinja2', py_name=py_name, **v)


def makedir(*path):
    path = join(*path)
    if isdir(path):
        rmtree(path)
    if not isdir(path):
        mkdir(path)


def pre():
    makedir(GEN_OUTPUT_DIR)
    makedir(GEN_OUTPUT_DIR, 'include')

    with open(join(GEN_OUTPUT_DIR, 'build.bat'), 'w') as f:
        f.write('msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32')

    with open(join(GEN_OUTPUT_DIR, 'include', 'common.h'), 'w') as f:
        f.write(render_template('common_h.jinja2', classes=[]))


def post():
    pureenums = list(render_pureenums())
    classes = list(render_classes())
    objenums = list(render_objenums())

    h_files = listdir(join(GEN_OUTPUT_DIR, 'include'))
    h_files.remove('common.h')

    with open(join(GEN_OUTPUT_DIR, 'pybrood.cpp'), 'w') as f:
        f.write(render_template(
            'pybrood_cpp.jinja2',
            pureenums=pureenums,
            classes=classes,
            objenums=objenums,
            h_files=h_files,
        ))

    with open(join(GEN_OUTPUT_DIR, 'pybrood.vcxproj'), 'w') as f:
        f.write(render_template(
            'vcproj.jinja2',
            bwapi_dir=PureWindowsPath(relpath(BWAPI_DIR, GEN_OUTPUT_DIR)),
            pybind_dir=PureWindowsPath(relpath(PYBIND_DIR, GEN_OUTPUT_DIR)),
            cpp_files=[],
        ))
