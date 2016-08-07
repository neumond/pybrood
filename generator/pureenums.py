from .utils import jin_env, flines
from html import unescape as html_unescape
from os.path import join
from .config import GEN_OUTPUT_DIR, BWAPI_INCLUDE_DIR
from .cdeclparser import lines_to_statements


def file_parser(f):
    result = []
    for e in lines_to_statements(f.enum_lines(), separator=','):
        if '=' in e:
            e = e.split('=')[0]
        e = e.strip()
        result.append(e)
    return {
        'items': result,
        'py_name': f.py_name,
        'bw_class_full': f.bw_class_full,
    }


class BasePureEnumFile:
    py_name = NotImplemented
    bw_class_full = NotImplemented

    @staticmethod
    def enum_lines():
        raise NotImplementedError

    @classmethod
    def perform(cls):
        context = file_parser(cls)
        lcl = cls.py_name.lower()
        with open(join(GEN_OUTPUT_DIR, 'pybind', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('pureenum.jinja2').render(**context)))


class CoordinateTypeFile(BasePureEnumFile):
    py_name = 'CoordinateType'
    bw_class_full = 'BWAPI::CoordinateType::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'CoordinateType.h'))
        yield from f(10, 20)


class EventTypeFile(BasePureEnumFile):
    py_name = 'EventType'
    bw_class_full = 'BWAPI::EventType::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'EventType.h'))
        yield from f(10, 29)


class FlagFile(BasePureEnumFile):
    py_name = 'Flag'
    bw_class_full = 'BWAPI::Flag::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Flag.h'))
        yield from f(12, 20)


class MouseButtonFile(BasePureEnumFile):
    py_name = 'MouseButton'
    bw_class_full = 'BWAPI::MouseButton'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Input.h'))
        yield from f(8, 11)


class KeyFile(BasePureEnumFile):
    py_name = 'Key'
    bw_class_full = 'BWAPI::Key'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Input.h'))
        yield from f(18, 249)


class LatencyFile(BasePureEnumFile):
    py_name = 'Latency'
    bw_class_full = 'BWAPI::Latency::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Latency.h'))
        yield from f(12, 18)


class TournamentActionFile(BasePureEnumFile):
    py_name = 'TournamentAction'
    bw_class_full = 'BWAPI::Tournament::ActionID'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'TournamentAction.h'))
        yield from f(13, 50)


class TextColorFile(BasePureEnumFile):
    py_name = 'TextColor'
    bw_class_full = 'BWAPI::Text::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Color.h'))
        yield from f(105, 185)


class TextSizeFile(BasePureEnumFile):
    py_name = 'TextSize'
    bw_class_full = 'BWAPI::Text::Size::Enum'

    @staticmethod
    def enum_lines():
        f = flines(join(BWAPI_INCLUDE_DIR, 'Color.h'))
        yield from f(194, 204)
