from collections import OrderedDict
from .cdeclparser import lines_to_statements


PURE_ENUM_MAP = {
    'CoordinateType': 'BWAPI::CoordinateType::Enum',
    'EventType': 'BWAPI::EventType::Enum',
    'Flag': 'BWAPI::Flag::Enum',
    'MouseButton': 'BWAPI::MouseButton',
    'Key': 'BWAPI::Key',
    'Latency': 'BWAPI::Latency::Enum',
    'TournamentAction': 'BWAPI::Tournament::ActionID',
    'TextColor': 'BWAPI::Text::Enum',
    'TextSize': 'BWAPI::Text::Size::Enum',
}


def take_pure_enums(line_gen):
    result = []
    for e in lines_to_statements(line_gen, separator=','):
        if '=' in e:
            e = e.split('=')[0]
        e = e.strip()
        result.append(e)
    return result


def parse_pure_enums(incflines):
    result = OrderedDict()

    def add(fn):
        k = fn.__name__
        result[k] = {
            'items': take_pure_enums(fn()),
            'bw_class_full': PURE_ENUM_MAP[k],
        }
        return fn

    @add
    def CoordinateType():
        f = incflines('CoordinateType.h')
        yield from f(10, 20)

    @add
    def EventType():
        f = incflines('EventType.h')
        yield from f(10, 29)

    @add
    def Flag():
        f = incflines('Flag.h')
        yield from f(12, 20)

    @add
    def MouseButton():
        f = incflines('Input.h')
        yield from f(8, 11)

    @add
    def Key():
        f = incflines('Input.h')
        yield from f(18, 249)

    @add
    def Latency():
        f = incflines('Latency.h')
        yield from f(12, 18)

    @add
    def TournamentAction():
        f = incflines('TournamentAction.h')
        yield from f(13, 50)

    @add
    def TextColor():
        f = incflines('Color.h')
        yield from f(105, 185)

    @add
    def TextSize():
        f = incflines('Color.h')
        yield from f(194, 204)

    return result
