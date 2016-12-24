from os import mkdir
from os.path import join, isdir
from collections import defaultdict, OrderedDict
from shutil import rmtree

from .config import GEN_OUTPUT_DIR, VCXProjectConfig
from .utils import render_template, indent_lines
from .parser import parse_pureenums, parse_classes, parse_objenums
from .proxy_replacements import custom_replacements
from .common import get_full_argtype, get_full_rettype, make_overload_signature
from .typereplacer2 import arg_replacer, func_replacer, DiscardFunction
from .additional import improve_container_class
from .docgen import make_docs_for_class


NODELETE_CLASSES = {'Client', 'Bullet', 'Force', 'Player', 'Region', 'Unit'}
UNPOINTED_CLASSES = {
    'Bullet': 'BulletInterface',
    'Force': 'ForceInterface',
    'Player': 'PlayerInterface',
    'Region': 'RegionInterface',
    'Unit': 'UnitInterface',
}
ITERABLE_CLASSES = {'Bulletset', 'Forceset', 'Playerset', 'Regionset', 'Unitset'}


def make_typereplacing(class_data):
    methods = []
    for func in class_data['methods']:
        try:
            func['args'] = [arg_replacer(a) for a in func['args']]
            new_methods = list(func_replacer(func))
        except DiscardFunction:
            pass
        else:
            methods.extend(new_methods)
    class_data['methods'] = methods


def make_overload_signatures(class_data, class_name):
    counts = defaultdict(lambda: 0)
    for func in class_data['methods']:
        counts[func['name']] += 1
    over_meths = {name for name, c in counts.items() if c > 1}

    for func in class_data['methods']:
        if func['name'] in over_meths:
            func['overload_signature'] = make_overload_signature(func, class_name)


def make_lambda_code(class_name, func, not_instance=False, expression=None):
    arg_lines, call_lines = [], OrderedDict()
    if not not_instance:
        arg_lines.append('{}& instance'.format(class_name))

    is_void_func = func['rtype'] == 'void'

    for a in func['args']:
        if 'type' in a:
            arg_lines.append('{} {}'.format(get_full_argtype(a), a['name']))
        call_lines[a['name']] = a.get('arg_code', a['name'])

    call_statement = func.get('ret_code', '{_voidreturn}{_expr};')
    defsubs = {
        '_fname': func.get('inner_name', func['name']),
        '_args': ', '.join(call_lines.values()),
    }
    defsubs['_expr'] = (expression or 'instance.{_fname}({_args})').format(**defsubs)
    call_statement = call_statement.format(
        _voidreturn='' if is_void_func else 'return ',
        **defsubs, **call_lines
    )

    return (
        '[]({args}){rtype}{{\n'
        '{body}}}'
    ).format(
        rtype='' if is_void_func else ' -> {} '.format(get_full_rettype(func)),
        args=', '.join(arg_lines),
        body=indent_lines(call_statement),
    )


def make_old_lambda_code(class_data, class_name, **kw):
    for func in class_data['methods']:
        func['code'] = make_lambda_code(class_name, func, **kw)


def make_new_lambda_code(class_data, class_name, not_instance=False, **kw):
    for func in class_data['methods']:
        code = make_lambda_code(class_name, func, not_instance=not_instance, **kw)
        if code != func.get('code') or not_instance:
            func['code'] = code
        else:
            func['code'] = '&{}::{}'.format(class_name, func['name'])
            if 'overload_signature' in func:
                func['code'] = '({}) {}'.format(func['overload_signature'], func['code'])


def make_default_arguments(class_data):
    for func in class_data['methods']:
        has_opts = False
        ags = []
        for a in func['args']:
            if 'type' not in a:
                continue
            line = 'py::arg("{}")'.format(a['name'])
            if a['opt_value'] is not None:
                line += ' = {}{}'.format(
                    '({}) '.format(get_full_argtype(a)) if a['opt_value'] == 'nullptr' else '',
                    a['opt_value'],
                )
                has_opts = True
            ags.append(line)
        if has_opts:
            func['arg_defaults'] = ', '.join(ags)


def make_modifiers(class_data):
    for func in class_data['methods']:
        if 'modifiers' in func:
            func['str_modifiers'] = ', '.join(func['modifiers'])


def render_pureenums():
    for py_name, v in parse_pureenums().items():
        yield render_template('pureenum.jinja2', py_name=py_name, **v)


def render_classes():
    all_classes = parse_classes()
    for py_name, v in all_classes.items():
        is_game = py_name == 'Game'
        lambda_kw = {'not_instance': is_game}
        if is_game:
            lambda_kw['expression'] = 'Broodwar->{_fname}({_args})'
        c = UNPOINTED_CLASSES[py_name] if py_name in UNPOINTED_CLASSES else py_name

        make_old_lambda_code(v, c, **lambda_kw)
        custom_replacements(v, c)
        make_typereplacing(v)
        if py_name in ITERABLE_CLASSES:
            improve_container_class(v)

        # here changes are locked, further calls only generate some "output" values
        make_overload_signatures(v, c)
        make_new_lambda_code(v, c, **lambda_kw)
        make_default_arguments(v)
        make_modifiers(v)

        if py_name in UNPOINTED_CLASSES:
            v['bw_class_full'] = 'BWAPI::{}'.format(UNPOINTED_CLASSES[py_name])
        yield (
            py_name,
            render_template(
                'game.jinja2' if is_game else 'direct_class.jinja2',
                py_name=py_name,
                nodelete=py_name in NODELETE_CLASSES, **v
            ),
            make_docs_for_class(v, py_name)
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


def main():
    pureenums = list(render_pureenums())
    class_names, classes, class_docs = zip(*render_classes())
    objenums = list(render_objenums())

    makedir(GEN_OUTPUT_DIR)

    with open(join(GEN_OUTPUT_DIR, 'pybrood.cpp'), 'w') as f:
        f.write(render_template(
            'pybrood_cpp.jinja2',
            pureenums=pureenums,
            classes=classes,
            objenums=objenums,
        ))

    with open(join(GEN_OUTPUT_DIR, 'pybrood.vcxproj'), 'w') as f:
        f.write(render_template(
            'vcproj.jinja2',
            config=VCXProjectConfig,
        ))

    with open(join(GEN_OUTPUT_DIR, 'build.bat'), 'w') as f:
        f.write(VCXProjectConfig.MSBUILD_COMMAND)

    mkdir(join(GEN_OUTPUT_DIR, 'docs'))
    mkdir(join(GEN_OUTPUT_DIR, 'docs', '_build'))
    mkdir(join(GEN_OUTPUT_DIR, 'docs', '_static'))
    mkdir(join(GEN_OUTPUT_DIR, 'docs', '_templates'))
    for cn, methods in zip(class_names, class_docs):
        with open(join(GEN_OUTPUT_DIR, 'docs', cn.lower() + '.rst'), 'w') as f:
            f.write(render_template(
                'docclass.jinja2',
                class_name=cn,
                methods=methods,
            ))
    with open(join(GEN_OUTPUT_DIR, 'docs', 'index.rst'), 'w') as f:
        f.write(render_template(
            'docindex.jinja2',
            classes=class_names,
        ))
    with open(join(GEN_OUTPUT_DIR, 'docs', 'conf.py'), 'w') as f:
        f.write(render_template('rstconf.jinja2'))
