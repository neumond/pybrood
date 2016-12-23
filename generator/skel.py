from .config import GEN_OUTPUT_DIR, BWAPI_DIR, PYBIND_DIR
from os import mkdir, listdir
from os.path import join, isdir, relpath
from .utils import render_template
from pathlib import PureWindowsPath
from shutil import rmtree
from .parser import parse_pureenums, parse_classes, parse_objenums
# from .proxy_classes import PROXY_CLASSES, get_replacement_parsed
from .proxy_replacements import MethodDiscarded, get_replacement
from collections import defaultdict
from .common import atype_or_dots, get_full_argtype, get_full_rettype
from .typereplacer2 import arg_replacer, NoReplacement


NODELETE_CLASSES = {'Client', 'Bullet', 'Force', 'Player', 'Region', 'Unit'}
UNPOINTED_CLASSES = {
    'Bullet': 'BulletInterface',
    'Force': 'ForceInterface',
    'Player': 'PlayerInterface',
    'Region': 'RegionInterface',
    'Unit': 'UnitInterface',
}


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


LINE_MAX_LEN_BEFORE_SPLIT = 50


def smart_arg_join(lines, gap):
    s_lines = ', '.join(lines)
    if len(s_lines) > LINE_MAX_LEN_BEFORE_SPLIT:
        s_lines = (',\n    ' + gap).join(lines)
        if len(lines) > 1:
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
            if a['opt_value']:
                i += ' = {}'.format(a['opt_value'])
            c = a['name']
        input_lines.append(i)
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


def render_pureenums():
    for py_name, v in parse_pureenums().items():
        yield render_template('pureenum.jinja2', py_name=py_name, **v)


def render_classes():
    all_classes = parse_classes()
    # game_class = all_classes.pop('Game')
    for py_name, v in all_classes.items():
        is_game = py_name == 'Game'
        c = UNPOINTED_CLASSES[py_name] if py_name in UNPOINTED_CLASSES else py_name
        make_overload_signatures(v, c)
        custom_replacements(v, c)
        make_lambda_overloads(v, c, force=is_game, game=is_game)
        if py_name in UNPOINTED_CLASSES:
            v['bw_class_full'] = 'BWAPI::{}'.format(UNPOINTED_CLASSES[py_name])
        yield render_template(
            'game.jinja2' if is_game else 'direct_class.jinja2',
            py_name=py_name,
            nodelete=py_name in NODELETE_CLASSES, **v
        )


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
    makedir(GEN_OUTPUT_DIR, 'src')
    makedir(GEN_OUTPUT_DIR, 'include')
    makedir(GEN_OUTPUT_DIR, 'pybind')

    with open(join(GEN_OUTPUT_DIR, 'build.bat'), 'w') as f:
        f.write('msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32')

    with open(join(GEN_OUTPUT_DIR, 'include', 'common.h'), 'w') as f:
        f.write(render_template('common_h.jinja2', classes=[]))


def post():
    pureenums = list(render_pureenums())
    # pureenums = []
    classes = list(render_classes())
    # classes = []
    objenums = list(render_objenums())
    # objenums = []

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
            cpp_files=listdir(join(GEN_OUTPUT_DIR, 'src')),
        ))
