from .cdeclparser import lines_to_statements
from .utils import squash_spaces, jin_env
from os.path import join
from html import unescape as html_unescape
from .config import GEN_OUTPUT_DIR


class BaseClassEnumFile:
    mapped_class = NotImplemented
    namespace = NotImplemented
    py_name = NotImplemented

    @staticmethod
    def lines():
        raise NotImplementedError

    @classmethod
    def items(cls):
        result = {}
        for expr in lines_to_statements(cls.lines()):
            expr = squash_spaces(expr).split(' ')
            assert expr[0] == 'extern'
            assert expr[1] == 'const'
            assert expr[2] == cls.mapped_class
            assert len(expr) == 4
            result[expr[3]] = cls.namespace + expr[3]
        return result

    @classmethod
    def assemble_context(cls):
        return {
            'py_name': cls.py_name,
            'items': cls.items(),
        }

    @classmethod
    def perform(cls):
        context = cls.assemble_context()
        lcl = cls.mapped_class.lower() + '_items'
        with open(join(GEN_OUTPUT_DIR, 'pybind', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('classenum.jinja2').render(**context)))
