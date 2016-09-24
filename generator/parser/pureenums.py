from .cdeclparser import lines_to_statements, incflines


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


def parse_pure_enums():
    def CoordinateType():
        f = incflines('CoordinateType.h')
        yield from f(10, 20)

    def EventType():
        f = incflines('EventType.h')
        yield from f(10, 29)

    def Flag():
        f = incflines('Flag.h')
        yield from f(12, 20)

    def MouseButton():
        f = incflines('Input.h')
        yield from f(8, 11)

    def Key():
        f = incflines('Input.h')
        yield from f(18, 249)

    def Latency():
        f = incflines('Latency.h')
        yield from f(12, 18)

    def TournamentAction():
        f = incflines('TournamentAction.h')
        yield from f(13, 50)

    def TextColor():
        f = incflines('Color.h')
        yield from f(105, 185)

    def TextSize():
        f = incflines('Color.h')
        yield from f(194, 204)

    return {k: take_pure_enums(v()) for k, v in vars().items()}


def main():
    result = {}
    for k, v in parse_pure_enums().items():
        result[k] = {
            'items': v,
            'bw_class_full': PURE_ENUM_MAP[k],
        }
    return result
