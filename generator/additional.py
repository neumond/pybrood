'''
This module is intended for adding custom methods to classes, like ability to iterate, ability to construct, etc
'''


TOLIST = '''
auto c = {source};
py::list result;
for (auto it = c.begin(); it != c.end(); ++it){{{{
    result.append({element});
}}}}
return result;

.def("__iter__", [](std::vector<int> &v) {
       return py::make_iterator(v.begin(), v.end());
    }, py::keep_alive<0, 1>()) /* Keep vector alive while iterator is used */
'''


def improve_container_class(class_data):
    class_data['methods'].append({
        'name': '__iter__',
        'rconst': False, 'rtype': 'void', 'selfconst': False, 'args': [],
        'custom_body': 'return py::make_iterator(instance.begin(), instance.end());',
        'modifiers': ['py::keep_alive<0, 1>()'],
    })
    class_data['methods'].append({
        'name': '__len__',
        'rconst': False, 'rtype': 'size_t', 'selfconst': False, 'args': [],
        'custom_body': 'return instance.size();',
    })
