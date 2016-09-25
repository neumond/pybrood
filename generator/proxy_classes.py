from .config import GEN_OUTPUT_DIR
from os.path import join
from .utils import render_template


PROXY_CLASSES = {'Region', 'Player', 'Unit', 'Bullet', 'Force'}


def make_header_signature(func, class_name):
    argline = ', '.join(a['type'] for a in func['args'])
    return '{} {}({})'.format(func['rtype'], func['name'], argline)


def make_method(func, class_name):
    argline = ', '.join('{} {}'.format(a['type'], a['name']) for a in func['args'])
    argnames = ', '.join(a['name'] for a in func['args'])
    return '{} {}::{}({}){{\n    return obj->{}({});\n}}'.format(
        func['rtype'], class_name, func['name'], argline, func['name'], argnames
    )


def write_class_header(class_name, class_data):
    methods = [make_header_signature(func, class_name) for func in class_data['methods']]
    return render_template('proxy_header.jinja2', py_name=class_name, methods=methods)


def write_class_code(class_name, class_data):
    hfile = class_name.lower() + '.h'
    methods = [make_method(func, class_name) for func in class_data['methods']]
    return render_template('proxy_body.jinja2', py_name=class_name, header_file=hfile, methods=methods)


def main(classes_data):
    for k in PROXY_CLASSES:
        klow = k.lower()
        with open(join(GEN_OUTPUT_DIR, 'include', '{}.h'.format(klow)), 'w') as f:
            f.write(write_class_header(k, classes_data[k]))
        with open(join(GEN_OUTPUT_DIR, 'src', '{}.cpp'.format(klow)), 'w') as f:
            f.write(write_class_code(k, classes_data[k]))
