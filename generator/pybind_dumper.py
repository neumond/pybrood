from collections import defaultdict
from .utils import transform_case


def default_member_type_rule(f):
    if not f['args'] and f['rtype'] != 'void':
        return 'def_property_readonly'
    return 'def'


def default_naming_rule(f, mtype):
    return transform_case(f['name'])


class Accumulator:
    '''
    Purpose of this class is to collect definitions you'll pass to pybind.
    It contains transformed-to-python names, decisions about definitions,
    and, more importantly it decides whether you need to add explicit signature to an overloaded method.
    '''

    def __init__(self, member_type_rule=default_member_type_rule, naming_rule=default_naming_rule):
        self.mod_defs = []
        self.prop_names = set()
        self.meth_names = set()
        self.member_type_rule = member_type_rule
        self.naming_rule = naming_rule
        self.includes = set()

    def __call__(self, f, processed):
        member_type = self.member_type_rule(f)
        name = self.naming_rule(f, member_type)
        record = {
            'type': member_type,
            'py_name': name,
            'orig_name': f['name'],
            'processed': processed,
            'require_signature': False,
        }
        if member_type == 'def':
            assert name not in self.prop_names, name
            self.meth_names.add(name)
            record['require_signature'] = True
        elif member_type == 'def_property_readonly':
            assert name not in self.prop_names, name
            assert name not in self.meth_names, name
            self.prop_names.add(name)
        else:
            raise ValueError('Unsupported member type {}'.format(member_type))
        self.mod_defs.append(record)
        self.includes |= processed['includes']

    def assemble(self):
        name_freq = defaultdict(lambda: 0)
        for x in self.mod_defs:
            if x['require_signature']:
                name_freq[x['orig_name']] += 1
        for x in self.mod_defs:
            if x['require_signature'] and name_freq[x['orig_name']] == 1:
                x['require_signature'] = False
            yield x
