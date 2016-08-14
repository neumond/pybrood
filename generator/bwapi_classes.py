from .classes import BaseClassFile, BaseWrappedClassFile
from os.path import join
from .utils import flines
from .config import BWAPI_INCLUDE_DIR


def incflines(*fname):
    return flines(join(BWAPI_INCLUDE_DIR, *fname))


class TypeMixin:
    # manually pass couple of baseclass methods from 'Type.h'
    @staticmethod
    def lines():
        yield 'int getID() const;'
        yield 'const std::string &getName() const;'


class BulletFile(BaseWrappedClassFile):
    mapped_class = 'Bullet'

    @staticmethod
    def lines():
        f = incflines('Bullet.h')
        yield from f(39, 167)


class BulletTypeFile(BaseClassFile):
    mapped_class = 'BulletType'
    enum_namespace = 'BWAPI::BulletTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('BulletType.h')
        yield from f(87, 123)


class ClientFile(BaseClassFile):
    mapped_class = 'Client'

    @staticmethod
    def lines():
        f = incflines('Client', 'Client.h')
        yield from f(20, 23)


class ColorFile(BaseClassFile):
    mapped_class = 'Color'
    enum_namespace = 'BWAPI::Color'
    constructors = '''
    TODO
    '''

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('Color.h')
        yield from f(40, 53)

    @staticmethod
    def enum_lines():
        f = incflines('Color.h')
        yield from f(61, 95)


class DamageTypeFile(BaseClassFile):
    mapped_class = 'DamageType'
    enum_namespace = 'BWAPI::DamageTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('DamageType.h')
        yield from f(60, 66)


class ErrorFile(BaseClassFile):
    mapped_class = 'Error'
    enum_namespace = 'BWAPI::Errors'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('Error.h')
        yield from f(75, 102)


class ExplosionTypeFile(BaseClassFile):
    mapped_class = 'ExplosionType'
    enum_namespace = 'BWAPI::ExplosionTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('ExplosionType.h')
        yield from f(68, 92)


class ForceFile(BaseWrappedClassFile):
    mapped_class = 'Force'

    @staticmethod
    def lines():
        f = incflines('Force.h')
        yield from f(25, 63)


class GameFile(BaseWrappedClassFile):
    mapped_class = 'Game'
    unboxed = True

    @staticmethod
    def lines():
        f = incflines('Game.h')
        yield from f(55, 1705)

        # TODO: iostream operator <<
        # TODO: flush()


class GameTypeFile(BaseClassFile):
    mapped_class = 'GameType'
    enum_namespace = 'BWAPI::GameTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('GameType.h')
        yield from f(62, 76)


class OrderFile(BaseClassFile):
    mapped_class = 'Order'
    enum_namespace = 'BWAPI::Orders'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('Order.h')
        yield from f(235, 390)


class PlayerFile(BaseWrappedClassFile):
    mapped_class = 'Player'

    @staticmethod
    def lines():
        f = incflines('Player.h')
        yield from f(38, 641)


class PlayerTypeFile(BaseClassFile):
    mapped_class = 'PlayerType'
    enum_namespace = 'BWAPI::PlayerTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('PlayerType.h')
        yield from f(45, 57)

    @staticmethod
    def enum_lines():
        f = incflines('PlayerType.h')
        yield from f(68, 78)


class RaceFile(BaseClassFile):
    mapped_class = 'Race'
    enum_namespace = 'BWAPI::Races'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('Race.h')
        yield from f(46, 87)

    @staticmethod
    def enum_lines():
        f = incflines('Race.h')
        yield from f(98, 103)


class RegionFile(BaseWrappedClassFile):
    mapped_class = 'Region'

    @staticmethod
    def lines():
        f = incflines('Region.h')
        yield from f(30, 132)


class TechTypeFile(BaseClassFile):
    mapped_class = 'TechType'
    enum_namespace = 'BWAPI::TechTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('TechType.h')
        yield from f(79, 154)

    @staticmethod
    def enum_lines():
        f = incflines('TechType.h')
        yield from f(165, 210)


class UnitFile(BaseWrappedClassFile):
    mapped_class = 'Unit'

    @staticmethod
    def lines():
        f = incflines('Unit.h')
        yield from f(60, 2458)

    @staticmethod
    def member_type_rule(f):
        if f['name'] == 'exists':
            return 'def_property_readonly'
        return BaseClassFile.member_type_rule(f)

    @staticmethod
    def naming_rule(f, mtype):
        if f['name'] == 'getUpgrade':
            return 'current_upgrade'
        return BaseClassFile.naming_rule(f, mtype)


class UnitCommandTypeFile(BaseClassFile):
    mapped_class = 'UnitCommandType'
    enum_namespace = 'BWAPI::UnitCommandTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('UnitCommandType.h')
        yield from f(89, 134)


class UnitSizeTypeFile(BaseClassFile):
    mapped_class = 'UnitSizeType'
    enum_namespace = 'BWAPI::UnitSizeTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()

    @staticmethod
    def enum_lines():
        f = incflines('UnitSizeType.h')
        yield from f(55, 60)


class UnitTypeFile(BaseClassFile):
    mapped_class = 'UnitType'
    enum_namespace = 'BWAPI::UnitTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('UnitType.h')
        yield from f(279, 902)

    @staticmethod
    def enum_lines():
        f = incflines('UnitType.h')
        yield from f(951, 1234)


class UpgradeTypeFile(BaseClassFile):
    mapped_class = 'UpgradeType'
    enum_namespace = 'BWAPI::UpgradeTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('UpgradeType.h')
        yield from f(93, 172)

    @staticmethod
    def enum_lines():
        f = incflines('UpgradeType.h')
        yield from f(183, 245)


class WeaponTypeFile(BaseClassFile):
    mapped_class = 'WeaponType'
    enum_namespace = 'BWAPI::WeaponTypes'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('WeaponType.h')
        yield from f(153, 305)

    @staticmethod
    def enum_lines():
        f = incflines('WeaponType.h')
        yield from f(330, 439)
