from .cdeclparser import lines_to_statements, parse_func, incflines


CLASS_MAP = {
    'Bullet': 'BWAPI::Bullet',
    'Bulletset': 'BWAPI::Bulletset',
    'Client': 'BWAPI::Client',
    'Color': 'BWAPI::Color',
    'DamageType': 'BWAPI::DamageType',
    'Error': 'BWAPI::Error',
    'ExplosionType': 'BWAPI::ExplosionType',
    'Force': 'BWAPI::Force',
    'Forceset': 'BWAPI::Forceset',
    'Game': 'BWAPI::Game',
    'GameType': 'BWAPI::GameType',
    'Order': 'BWAPI::Order',
    'Player': 'BWAPI::Player',
    'Playerset': 'BWAPI::Playerset',
    'PlayerType': 'BWAPI::PlayerType',
    'Race': 'BWAPI::Race',
    'Region': 'BWAPI::Region',
    'Regionset': 'BWAPI::Regionset',
    'TechType': 'BWAPI::TechType',
    'Unit': 'BWAPI::Unit',
    'UnitCommandType': 'BWAPI::UnitCommandType',
    'Unitset': 'BWAPI::Unitset',
    'UnitSizeType': 'BWAPI::UnitSizeType',
    'UnitType': 'BWAPI::UnitType',
    'UpgradeType': 'BWAPI::UpgradeType',
    'WeaponType': 'BWAPI::WeaponType',
}


def take_functions(line_gen):
    return [fnc for fnc in map(parse_func, lines_to_statements(line_gen))]


def type_lines():
    yield 'int getID() const;'
    yield 'const std::string &getName() const;'


def parse_classes():
    def Bullet():
        f = incflines('Bullet.h')
        yield from f(39, 167)

    def Bulletset():
        # f = incflines('Bulletset.h')
        yield ''

    def Client():
        f = incflines('Client', 'Client.h')
        yield from f(20, 23)

    def Color():
        yield from type_lines()
        f = incflines('Color.h')
        yield from f(40, 53)

    def DamageType():
        yield from type_lines()

    def Error():
        yield from type_lines()

    def ExplosionType():
        yield from type_lines()

    def Force():
        f = incflines('Force.h')
        yield from f(25, 63)

    def Forceset():
        f = incflines('Forceset.h')
        yield from f(18, 19)

    def Game():
        f = incflines('Game.h')
        yield from f(55, 1705)
        # TODO: iostream operator <<
        # TODO: flush()

    def GameType():
        yield from type_lines()

    def Order():
        yield from type_lines()

    def Player():
        f = incflines('Player.h')
        yield from f(38, 641)

    def Playerset():
        f = incflines('Playerset.h')
        yield from f(19, 41)

    def PlayerType():
        yield from type_lines()
        f = incflines('PlayerType.h')
        yield from f(45, 57)

    def Race():
        yield from type_lines()
        f = incflines('Race.h')
        yield from f(46, 87)

    def Region():
        f = incflines('Region.h')
        yield from f(30, 132)

    def Regionset():
        f = incflines('Regionset.h')
        yield from f(19, 23)

    def TechType():
        yield from type_lines()
        f = incflines('TechType.h')
        yield from f(79, 154)

    def Unit():
        f = incflines('Unit.h')
        yield from f(60, 2458)

    def UnitCommandType():
        yield from type_lines()

    def Unitset():
        f = incflines('Unitset.h')
        yield from f(27, 183)

    def UnitSizeType():
        yield from type_lines()

    def UnitType():
        yield from type_lines()
        f = incflines('UnitType.h')
        yield from f(279, 902)

    def UpgradeType():
        yield from type_lines()
        f = incflines('UpgradeType.h')
        yield from f(93, 172)

    def WeaponType():
        yield from type_lines()
        f = incflines('WeaponType.h')
        yield from f(153, 305)

    return {k: take_functions(v()) for k, v in vars().items()}


def main():
    result = {}
    for k, v in parse_classes().items():
        result[k] = {
            'methods': v,
            'bw_class_full': CLASS_MAP[k],
        }
    return result
