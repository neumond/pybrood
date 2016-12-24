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
