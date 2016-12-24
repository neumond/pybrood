from os.path import dirname, join
import yaml


with open(join(dirname(__file__), 'typemap.yaml')) as f:
    TYPE_MAP = yaml.load(f)
    # from pprint import pprint
    # pprint(TYPE_MAP)
    # exit()


def type_name(t):
    return TYPE_MAP.get(t, {}).get('_name', t)


def format_arg(a):
    if a['type'] not in TYPE_MAP:
        print('Unrecognized type', a['type'])
    dv = ''
    if a['opt_value'] is not None:
        if a['opt_value'] not in TYPE_MAP.get(a['type'], {}):
            print('Unrecognized default value', a['type'], a['opt_value'])
        else:
            dv = '={}'.format(TYPE_MAP[a['type']][a['opt_value']])
    return '{}: {}{}'.format(
        a['name'], type_name(a['type']), dv
    )


def make_docs_for_class(class_data, class_name):
    output = []
    for func in class_data['methods']:
        if func['name'] in ('__iter__', '__len__'):
            continue
        if func['rtype'] != 'void' and func['rtype'] not in TYPE_MAP:
            print('Unrecognized type', func['rtype'])
        line = '{}.{}({}){}'.format(
            class_name,
            func['name'],
            ', '.join(format_arg(a) for a in func['args'] if 'type' in a),
            '' if func['rtype'] == 'void' else ' -> {}'.format(type_name(func['rtype'])),
        )
        output.append(line)
    return output
