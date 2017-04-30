from collections import OrderedDict
from .cdeclparser import lines_to_statements, parse_func


def take_functions(line_gen):
    return [fnc for fnc in map(parse_func, lines_to_statements(line_gen))]


def type_lines():
    yield 'int getID() const;'
    yield 'const std::string &getName() const;'


def parse_classes(incflines):
    result = OrderedDict()

    def add(fn):
        k = fn.__name__
        result[k] = {
            'methods': take_functions(fn()),
            'bw_class_full': 'BWAPI::{}'.format(k),
        }
        return fn

    @add
    def BulletType():
        yield from type_lines()

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

    return result
