'''
This module is intended for adding custom methods to classes, like ability to iterate, ability to construct, etc
'''


def improve_container_class(class_data):
    class_data['methods'].append({
        'name': '__iter__',
        'rconst': False, 'rtype': 'void', 'selfconst': False, 'args': [],
        'ret_code': 'return py::make_iterator(instance.begin(), instance.end());',
        'modifiers': ['py::keep_alive<0, 1>()'],
    })
    class_data['methods'].append({
        'name': '__len__',
        'rconst': False, 'rtype': 'size_t', 'selfconst': False, 'args': [],
        'ret_code': 'return instance.size();',
    })


def make_constructable(py_class_name, class_data):
    if py_class_name == 'Color':
        class_data['methods'].insert(0, {
            'name': '__init__',
            'rconst': False, 'rtype': 'void', 'selfconst': False, 'args': [
                {'const': False, 'type': 'int', 'name': 'red', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'green', 'opt_value': None},
                {'const': False, 'type': 'int', 'name': 'blue', 'opt_value': None},
            ],
            'ret_code': 'new (&instance) Color({_args});',
        })


def make_equality_op(class_data, class_name):
    class_data['methods'].append({
        'name': '__eq__',
        'rconst': False, 'rtype': 'bool', 'selfconst': False, 'args': [
            {'const': False, 'type': class_name + '&', 'name': 'other', 'opt_value': None},
        ],
        'ret_code': 'return instance.getID() == other.getID();',
    })
