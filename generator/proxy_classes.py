from .config import GEN_OUTPUT_DIR
from os.path import join
from .utils import render_template
from .parser import parse_classes


PROXY_CLASSES = {'Region', 'Player', 'Unit', 'Bullet', 'Force', 'Game'}
PTR_CLASSES = {'Game'}


def get_full_argtype(a):
    t = a['type']
    if a['const']:
        t = 'const ' + t
    return t


def get_full_rettype(a):
    t = a['rtype']
    if a['rconst']:
        t = 'const ' + t
    return t


def atype_or_dots(a):
    if a['type'] == '':
        return '...'
    return get_full_argtype(a)


def make_header_signature(func, class_name):
    argline = ', '.join(atype_or_dots(a) for a in func['args'])
    return '{} {}({})'.format(get_full_rettype(func), func['name'], argline)


def argument_as_is(a):
    r = '{} {}'.format(get_full_argtype(a), a['name']).strip()
    if a['opt_value'] is not None:
        r += ' = {}'.format(a['opt_value'])
    return r


def make_method(func, class_name):
    argline = ', '.join(argument_as_is(a) for a in func['args'])
    argnames = ', '.join(a['name'] for a in func['args'])
    rst = '' if func['rtype'] == 'void' else 'return '
    return '{} Pybrood{}::{}({}){{\n    {}obj->{}({});\n}}'.format(
        get_full_rettype(func), class_name, func['name'], argline, rst, func['name'], argnames
    )


def write_class_header(class_name, class_data, pointer_type):
    methods = [make_header_signature(func, class_name) for func in class_data['methods']]
    return render_template('proxy_header.jinja2', proxy_type=class_name, methods=methods, pointer_type=pointer_type)


def write_class_code(class_name, class_data, pointer_type):
    hfile = class_name.lower() + '.h'
    methods = [make_method(func, class_name) for func in class_data['methods']]
    return render_template(
        'proxy_body.jinja2', proxy_type=class_name, header_file=hfile, methods=methods, pointer_type=pointer_type
    )


def main():
    classes_data = parse_classes()
    for k in PROXY_CLASSES:
        klow = k.lower()
        pointer_type = 'BWAPI::{}'.format(k)  # avoid ambiguity with proxy types
        if k in PTR_CLASSES:
            pointer_type += '*'
        with open(join(GEN_OUTPUT_DIR, 'include', '{}.h'.format(klow)), 'w') as f:
            f.write(write_class_header(k, classes_data[k], pointer_type))
        with open(join(GEN_OUTPUT_DIR, 'src', '{}.cpp'.format(klow)), 'w') as f:
            f.write(write_class_code(k, classes_data[k], pointer_type))
