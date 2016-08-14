from .classes import BaseClassFile, BaseWrappedClassFile
from .classenums import BaseClassEnumFile
from os.path import join
from .utils import flines
from .config import BWAPI_INCLUDE_DIR


def incflines(*fname):
    return flines(join(BWAPI_INCLUDE_DIR, *fname))


POSITION_CONSTANTS = ('Invalid', 'None', 'Unknown', 'Origin')


class TypeMixin:
    force_lambda = {'getID', 'getName'}

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


class BulletSetFile(BaseClassFile):
    mapped_class = 'Bulletset'

    @staticmethod
    def lines():
        # f = incflines('Bulletset.h')
        yield ''


class BulletTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'BulletType'


class BulletTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'BulletType'
    namespace = 'BWAPI::BulletTypes::'
    py_name = 'bullet_types'

    @staticmethod
    def lines():
        f = incflines('BulletType.h')
        yield from f(87, 123)


class ClientFile(BaseClassFile):
    mapped_class = 'Client'

    @staticmethod
    def lines():
        f = incflines('Client', 'Client.h')
        yield from f(20, 23)


class ColorFile(TypeMixin, BaseClassFile):
    mapped_class = 'Color'
    constructors = ('int', 'int, int, int')

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('Color.h')
        yield from f(40, 53)


class ColorEnumFile(BaseClassEnumFile):
    mapped_class = 'Color'
    namespace = 'BWAPI::Colors::'
    py_name = 'colors'

    @staticmethod
    def lines():
        f = incflines('Color.h')
        yield from f(61, 95)


class DamageTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'DamageType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class DamageTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'DamageType'
    namespace = 'BWAPI::DamageTypes::'
    py_name = 'damage_types'

    @staticmethod
    def lines():
        f = incflines('DamageType.h')
        yield from f(60, 66)


class ErrorFile(TypeMixin, BaseClassFile):
    mapped_class = 'Error'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class ErrorEnumFile(BaseClassEnumFile):
    mapped_class = 'Error'
    namespace = 'BWAPI::Errors::'
    py_name = 'errors'

    @staticmethod
    def lines():
        f = incflines('Error.h')
        yield from f(75, 102)


class ExplosionTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'ExplosionType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class ExplosionTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'ExplosionType'
    namespace = 'BWAPI::ExplosionTypes::'
    py_name = 'explosion_types'

    @staticmethod
    def lines():
        f = incflines('ExplosionType.h')
        yield from f(68, 92)


class ForceFile(BaseWrappedClassFile):
    mapped_class = 'Force'

    @staticmethod
    def lines():
        f = incflines('Force.h')
        yield from f(25, 63)


class ForceSetFile(BaseClassFile):
    mapped_class = 'Forceset'

    @staticmethod
    def lines():
        f = incflines('Forceset.h')
        yield from f(18, 19)


class GameFile(BaseWrappedClassFile):
    mapped_class = 'GameWrapper'
    unboxed = True
    wobj_op = '(*obj)->'

    @staticmethod
    def lines():
        f = incflines('Game.h')
        yield from f(55, 1705)

        # TODO: iostream operator <<
        # TODO: flush()


class GameTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'GameType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class GameTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'GameType'
    namespace = 'BWAPI::GameTypes::'
    py_name = 'game_types'

    @staticmethod
    def lines():
        f = incflines('GameType.h')
        yield from f(62, 76)


class OrderFile(TypeMixin, BaseClassFile):
    mapped_class = 'Order'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class OrderEnumFile(BaseClassEnumFile):
    mapped_class = 'Order'
    namespace = 'BWAPI::Orders::'
    py_name = 'orders'

    @staticmethod
    def lines():
        f = incflines('Order.h')
        yield from f(235, 390)


class PlayerFile(BaseWrappedClassFile):
    mapped_class = 'Player'

    @staticmethod
    def lines():
        f = incflines('Player.h')
        yield from f(38, 641)


class PlayerSetFile(BaseClassFile):
    mapped_class = 'Playerset'

    @staticmethod
    def lines():
        f = incflines('Playerset.h')
        yield from f(19, 41)


class PlayerTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'PlayerType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('PlayerType.h')
        yield from f(45, 57)


class PlayerTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'PlayerType'
    namespace = 'BWAPI::PlayerTypes::'
    py_name = 'player_types'

    @staticmethod
    def lines():
        f = incflines('PlayerType.h')
        yield from f(68, 78)


# class PositionEnumFile(BaseClassEnumFile):
#     mapped_class = 'Position'
#     namespace = 'PyBinding::Positions::'
#     py_name = 'positions'
#
#     @classmethod
#     def items(cls):
#         return {x: cls.namespace + x for x in POSITION_CONSTANTS}


class RaceFile(TypeMixin, BaseClassFile):
    mapped_class = 'Race'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('Race.h')
        yield from f(46, 87)


class RaceEnumFile(BaseClassEnumFile):
    mapped_class = 'Race'
    namespace = 'BWAPI::Races::'
    py_name = 'races'

    @staticmethod
    def lines():
        f = incflines('Race.h')
        yield from f(98, 103)


class RegionFile(BaseWrappedClassFile):
    mapped_class = 'Region'

    @staticmethod
    def lines():
        f = incflines('Region.h')
        yield from f(30, 132)


class RegionSetFile(BaseClassFile):
    mapped_class = 'Regionset'

    @staticmethod
    def lines():
        f = incflines('Regionset.h')
        yield from f(19, 23)


class TechTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'TechType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('TechType.h')
        yield from f(79, 154)


class TechTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'TechType'
    namespace = 'BWAPI::TechTypes::'
    py_name = 'tech_types'

    @staticmethod
    def lines():
        f = incflines('TechType.h')
        yield from f(165, 210)


# class TilePositionEnumFile(BaseClassEnumFile):
#     mapped_class = 'TilePosition'
#     namespace = 'PyBinding::TilePositions::'
#     py_name = 'tile_positions'
#
#     @classmethod
#     def items(cls):
#         return {x: cls.namespace + x for x in POSITION_CONSTANTS}


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


class UnitCommandTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'UnitCommandType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class UnitCommandTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'UnitCommandType'
    namespace = 'BWAPI::UnitCommandTypes::'
    py_name = 'unit_command_types'

    @staticmethod
    def lines():
        f = incflines('UnitCommandType.h')
        yield from f(89, 134)


class UnitSetFile(BaseClassFile):
    mapped_class = 'Unitset'
    skip_funcs = {'setClientInfo'}

    @staticmethod
    def lines():
        f = incflines('Unitset.h')
        yield from f(27, 183)


class UnitSizeTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'UnitSizeType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()


class UnitSizeTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'UnitSizeType'
    namespace = 'BWAPI::UnitSizeTypes::'
    py_name = 'unit_size_types'

    @staticmethod
    def lines():
        f = incflines('UnitSizeType.h')
        yield from f(55, 60)


class UnitTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'UnitType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('UnitType.h')
        yield from f(279, 902)


class UnitTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'UnitType'
    namespace = 'BWAPI::UnitTypes::'
    py_name = 'unit_types'

    @staticmethod
    def lines():
        f = incflines('UnitType.h')
        yield from f(951, 1234)


class UpgradeTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'UpgradeType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('UpgradeType.h')
        yield from f(93, 172)


class UpgradeTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'UpgradeType'
    namespace = 'BWAPI::UpgradeTypes::'
    py_name = 'upgrade_types'

    @staticmethod
    def lines():
        f = incflines('UpgradeType.h')
        yield from f(183, 245)


class WeaponTypeFile(TypeMixin, BaseClassFile):
    mapped_class = 'WeaponType'

    @staticmethod
    def lines():
        yield from TypeMixin.lines()
        f = incflines('WeaponType.h')
        yield from f(153, 305)


# class WalkPositionEnumFile(BaseClassEnumFile):
#     mapped_class = 'WalkPosition'
#     namespace = 'PyBinding::WalkPositions::'
#     py_name = 'walk_positions'
#
#     @classmethod
#     def items(cls):
#         return {x: cls.namespace + x for x in POSITION_CONSTANTS}


class WeaponTypeEnumFile(BaseClassEnumFile):
    mapped_class = 'WeaponType'
    namespace = 'BWAPI::WeaponTypes::'
    py_name = 'weapon_types'

    @staticmethod
    def lines():
        f = incflines('WeaponType.h')
        yield from f(330, 439)
