from collections import OrderedDict
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
    ITEMS = OrderedDict()

    def add(fn):
        ITEMS[fn.__name__] = fn
        return fn

    @add
    def Color():
        yield from type_lines()
        f = incflines('Color.h')
        yield from f(40, 53)

    @add
    def DamageType():
        yield from type_lines()

    @add
    def Error():
        yield from type_lines()

    @add
    def ExplosionType():
        yield from type_lines()

    @add
    def GameType():
        yield from type_lines()

    @add
    def Order():
        yield from type_lines()

    @add
    def PlayerType():
        yield from type_lines()
        f = incflines('PlayerType.h')
        yield from f(45, 57)

    @add
    def Race():
        yield from type_lines()
        f = incflines('Race.h')
        yield from f(46, 87)

    @add
    def TechType():
        yield from type_lines()
        f = incflines('TechType.h')
        yield from f(79, 154)

    @add
    def UnitCommandType():
        yield from type_lines()

    @add
    def UnitSizeType():
        yield from type_lines()

    @add
    def UnitType():
        yield from type_lines()
        f = incflines('UnitType.h')
        yield from f(279, 902)

    @add
    def UpgradeType():
        yield from type_lines()
        f = incflines('UpgradeType.h')
        yield from f(93, 172)

    @add
    def WeaponType():
        yield from type_lines()
        f = incflines('WeaponType.h')
        yield from f(153, 305)

    # ================================

    @add
    def Bullet():
        f = incflines('Bullet.h')
        yield from f(39, 167)

    @add
    def Bulletset():
        # f = incflines('Bulletset.h')
        yield ''

    @add
    def Player():
        f = incflines('Player.h')
        yield from f(38, 641)

    @add
    def Playerset():
        f = incflines('Playerset.h')
        yield from f(19, 41)

    @add
    def Region():
        f = incflines('Region.h')
        yield from f(30, 132)

    @add
    def Regionset():
        f = incflines('Regionset.h')
        yield from f(19, 23)

    @add
    def Unit():
        f = incflines('Unit.h')
        yield from f(60, 2458)

    @add
    def Unitset():
        f = incflines('Unitset.h')
        yield from f(27, 183)

    @add
    def Force():
        f = incflines('Force.h')
        yield from f(25, 63)

    @add
    def Forceset():
        f = incflines('Forceset.h')
        yield from f(18, 19)

    # ================================

    @add
    def Game():
        f = incflines('Game.h')
        yield from f(55, 783)
        # skipping variadic printf-like functions
        yield from f(801, 811)
        yield from f(825, 834)
        yield from f(852, 1705)
        # TODO: iostream operator <<
        # TODO: flush()

    @add
    def Client():
        f = incflines('Client', 'Client.h')
        yield from f(20, 23)

    return OrderedDict((k, take_functions(v())) for k, v in ITEMS.items())


def main():
    result = OrderedDict()
    for k, v in parse_classes().items():
        result[k] = {
            'methods': v,
            'bw_class_full': CLASS_MAP[k],
        }
    return result
