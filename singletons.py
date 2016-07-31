from sys import stderr
from cdeclparser import lines_to_funclines, parse_func
from cdumper import fmt_arg, transform_case, arg_type_for_signature, enum_types


KNOWN_TYPES = {
    'void', 'int', 'bool', 'double', 'std::string', 'std::string &',
    # 'Unit', 'Force', 'Player',
    # 'Unitset', 'Forceset', 'Playerset',
}


def fmt_func(f, obj, pb_module_name):
    t = transform_case(f['name'])
    ret_type = '' if f['rtype'] == 'void' else ' -> {} '.format(f['rtype'])
    arg_names = ', '.join(a['name'] for a in f['args'])
    arg_sig = ', '.join(fmt_arg(a) for a in f['args'])
    ret_expr = '' if f['rtype'] == 'void' else 'return '
    return '''{pb_module_name}.def("{t}", []({arg_sig}){ret_type}{{
    {ret_expr}{obj}{f_name}({arg_names});
}});
'''.format(
        pb_module_name=pb_module_name, obj=obj, t=t, f_name=f['name'], ret_type=ret_type,
        arg_names=arg_names, arg_sig=arg_sig, ret_expr=ret_expr
    )


def file_parser(f, out_file):
    pb_module_name = 'm_' + f.module

    out_file.write('''py::module {pb_module_name} = m.def_submodule("{f_module}");
'''.format(pb_module_name=pb_module_name, f_module=f.module))
    # m_Client.def("is_connected", []() -> bool {
    #     return BWAPI::BWAPIClient.isConnected();
    # });
    # m_Client.def("connect", []() -> bool {
    #     return BWAPI::BWAPIClient.connect();
    # });
    # m_Client.def("disconnect", [](){
    #     BWAPI::BWAPIClient.disconnect();
    # });
    # m_Client.def("update", [](){
    #     BWAPI::BWAPIClient.update();
    # });
    # '''.format(
    #         mclass=ma.mapped_class, derclass=ma.derived_class
    #     ))

    for func in lines_to_funclines(f.lines()):
        fnc = parse_func(func)
        for t in enum_types(fnc):
            if t not in KNOWN_TYPES:
                print('UNKNOWN TYPE', t, file=stderr)
                break
        else:
            out_file.write(fmt_func(fnc, f.obj, pb_module_name))


class BaseFile:
    obj = NotImplemented
    module = NotImplemented

    @staticmethod
    def lines():
        raise NotImplementedError

    # @staticmethod
    # def ro_property_rule(f, t):
    #     return t.startswith(('is_', 'get_'))
    #
    # @staticmethod
    # def rename_rule(f, t, is_property):
    #     if not is_property:
    #         return t
    #     elif t.startswith(('get_',)):
    #         return '_'.join(t.split('_')[1:])
    #     return t


class GameFile(BaseFile):
    obj = 'BWAPI::Broodwar->'
    module = 'game'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/Game.h') as f:
            for i, line in enumerate(f, start=1):
                if 55 <= i <= 1705:
                    yield line


class ClientFile(BaseFile):
    obj = 'BWAPI::BWAPIClient.'
    module = 'client'

    @staticmethod
    def lines():
        with open('../bwapi/bwapi/include/BWAPI/Client/Client.h') as f:
            for i, line in enumerate(f, start=1):
                if 20 <= i <= 23:
                    yield line


def main():
    with open('pybinding/game_auto.cpp', 'w') as f:
        file_parser(GameFile, f)
    with open('pybinding/client_auto.cpp', 'w') as f:
        file_parser(ClientFile, f)
