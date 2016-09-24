from .parser.classes import main as get_data
# from .typereplacer import transform_input_type, transform_output_type
from collections import defaultdict


def find_overloaded_methods(class_data):
    counts = defaultdict(lambda: 0)
    for func in class_data['methods']:
        counts[func['name']] += 1
    return {name for name, c in counts.items() if c > 1}


def transform_class(class_data):
    for func in class_data['methods']:
        # print(func)
        for arg in func['args']:
            pass
            # transarg = transform_input_type(arg['type'], const=arg['const'])
        # print(' ', f['name'])
        # print(' ', f)
    return class_data


def main():
    tdata = {}
    for py_name, class_data in get_data().items():
        tdata[py_name] = transform_class(class_data)
    return tdata
