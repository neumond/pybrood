from collections import OrderedDict
from .cdeclparser import lines_to_statements
from ..utils import squash_spaces


OBJ_ENUM_NS_MAP = {
    'BulletType': 'BWAPI::BulletTypes::',
    'Color': 'BWAPI::Colors::',
    'DamageType': 'BWAPI::DamageTypes::',
    'Error': 'BWAPI::Errors::',
    'ExplosionType': 'BWAPI::ExplosionTypes::',
    'GameType': 'BWAPI::GameTypes::',
    'Order': 'BWAPI::Orders::',
    'PlayerType': 'BWAPI::PlayerTypes::',
    'Race': 'BWAPI::Races::',
    'TechType': 'BWAPI::TechTypes::',
    'UnitCommandType': 'BWAPI::UnitCommandTypes::',
    'UnitSizeType': 'BWAPI::UnitSizeTypes::',
    'UnitType': 'BWAPI::UnitTypes::',
    'UpgradeType': 'BWAPI::UpgradeTypes::',
    'WeaponType': 'BWAPI::WeaponTypes::',
}


def take_enums(line_gen):
    result = []
    for expr in lines_to_statements(line_gen):
        expr = squash_spaces(expr).split(' ')
        assert expr[0] == 'extern'
        assert expr[1] == 'const'
        # assert expr[2] == cls.mapped_class
        assert len(expr) == 4
        # result[expr[3]] = cls.namespace + expr[3]
        result.append(expr[3])
    return result


def transform_objenum_names(items):
    for item in items:
        if item == 'None':
            yield 'None_'  # None is python keyword
        else:
            yield item


def parse_object_enums(incflines):
    result = OrderedDict()

    def add(fn):
        k = fn.__name__
        v = take_enums(fn())
        result[k] = {
            'items': list(zip(v, transform_objenum_names(v))),
            'namespace': OBJ_ENUM_NS_MAP[k],
        }
        return fn

    @add
    def BulletType():
        f = incflines('BulletType.h')
        yield from f(87, 123)

    @add
    def Color():
        f = incflines('Color.h')
        yield from f(61, 95)

    @add
    def DamageType():
        f = incflines('DamageType.h')
        yield from f(60, 66)

    @add
    def Error():
        f = incflines('Error.h')
        yield from f(75, 102)

    @add
    def ExplosionType():
        f = incflines('ExplosionType.h')
        yield from f(68, 92)

    @add
    def GameType():
        f = incflines('GameType.h')
        yield from f(62, 76)

    @add
    def Order():
        f = incflines('Order.h')
        yield from f(235, 390)

    @add
    def PlayerType():
        f = incflines('PlayerType.h')
        yield from f(68, 78)

    @add
    def Race():
        f = incflines('Race.h')
        yield from f(98, 103)

    @add
    def TechType():
        f = incflines('TechType.h')
        yield from f(165, 210)

    @add
    def UnitCommandType():
        f = incflines('UnitCommandType.h')
        yield from f(89, 134)

    @add
    def UnitSizeType():
        f = incflines('UnitSizeType.h')
        yield from f(55, 60)

    @add
    def UnitType():
        f = incflines('UnitType.h')
        yield from f(951, 1234)

    @add
    def UpgradeType():
        f = incflines('UpgradeType.h')
        yield from f(183, 245)

    @add
    def WeaponType():
        f = incflines('WeaponType.h')
        yield from f(330, 439)

    return result
