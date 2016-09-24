from .parser.classes import main as get_data
# from .typereplacer import transform_input_type, transform_output_type
from collections import defaultdict


PRE_TYPE_MAP = {
    'std::string &': 'std::string&',
    'UnitFilter &': 'BWAPI::UnitFilter&',
    'Unitset &': 'BWAPI::Unitset&',
    'std::pair< UnitType, int >': 'std::pair<BWAPI::UnitType, int>',
    'UnitType::set&': 'BWAPI::UnitType::set&',
    'void *': 'void*',
    'Regionset &': 'BWAPI::Regionset&',
    'std::map< UnitType, int >&': 'std::map<BWAPI::UnitType, int>&',
    'std::list< Event >&': 'std::list<BWAPI::Event>&',
    'SetContainer<TechType>&': 'BWAPI::SetContainer<BWAPI::TechType>&',
    'SetContainer<UpgradeType>&': 'BWAPI::SetContainer<BWAPI::UpgradeType>&',
    'BestUnitFilter &': 'BWAPI::BestUnitFilter&',
    'char *': 'char*',
}


for t in ('void', 'int', 'bool', 'std::string', 'double', 'char', '', 'va_list'):
    PRE_TYPE_MAP[t] = t
for t in (
    'Position', 'Playerset', 'Race', 'Unitset', 'UnitType', 'Player', 'BulletType', 'TechType', 'Forceset&',
    'Playerset&', 'UpgradeType', 'DamageType', 'WeaponType', 'PlayerType', 'Unitset&', 'Unit', 'Order',
    'Bulletset&', 'Region', 'Race::set', 'TilePosition', 'ExplosionType', 'UnitCommand', 'Position::list&',
    'PositionOrUnit', 'UnitType::list', 'UnitCommandType', 'Force', 'Color', 'GameType', 'UnitSizeType',
    'MouseButton', 'Key', 'Error', 'WalkPosition', 'TilePosition::list&', 'Text::Size::Enum',
    'CoordinateType::Enum',
):
    PRE_TYPE_MAP[t] = 'BWAPI::' + t


def presub_type(t):
    if t in PRE_TYPE_MAP:
        return PRE_TYPE_MAP[t]
    assert False, 'Unknown type "{}"'.format(t)


def presub_types(class_data):
    for func in class_data['methods']:
        func['rtype'] = presub_type(func['rtype'])
        for arg in func['args']:
            arg['type'] = presub_type(arg['type'])


def make_overload_signature(func, class_name):
    argline = ', '.join(a['type'] for a in func['args'])
    return '{} ({}::*)({})'.format(func['rtype'], class_name, argline)


def make_overload_signatures(class_data, class_name):
    counts = defaultdict(lambda: 0)
    for func in class_data['methods']:
        counts[func['name']] += 1
    over_meths = {name for name, c in counts.items() if c > 1}

    for func in class_data['methods']:
        if func['name'] in over_meths:
            func['overload_signature'] = make_overload_signature(func, class_name)


def transform_class(class_data, class_name):
    presub_types(class_data)
    make_overload_signatures(class_data, class_name)
    return class_data


def main():
    tdata = {}
    for py_name, class_data in get_data().items():
        tdata[py_name] = transform_class(class_data, py_name)
    return tdata
