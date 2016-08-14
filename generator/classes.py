from .pybind_dumper import Accumulator, default_member_type_rule, default_naming_rule
from .utils import transform_case, jin_env, outerr
from .cdeclparser import lines_to_statements, parse_func
from html import unescape as html_unescape
from os.path import join
from .config import GEN_OUTPUT_DIR
from .typereplacer import process_function


class BaseClassFile:
    mapped_class = NotImplemented
    constructors = ()
    force_lambda = set()
    skip_funcs = set()

    @staticmethod
    def lines():
        raise NotImplementedError

    @staticmethod
    def member_type_rule(f):
        r = default_member_type_rule(f)
        if r == 'def_property_readonly' and not transform_case(f['name']).startswith(('is_', 'get_')):
            return 'def'
        return r

    @staticmethod
    def naming_rule(f, mtype):
        t = default_naming_rule(f, mtype)
        if mtype != 'def_property_readonly':
            return t
        elif t.startswith('get_'):
            return '_'.join(t.split('_')[1:])
        return t

    @classmethod
    def python_name(cls):
        return cls.mapped_class

    @classmethod
    def perform(cls):
        context = cls.assemble_context()
        lcl = cls.python_name().lower()
        with open(join(GEN_OUTPUT_DIR, 'pybind', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('class.jinja2').render(**context)))

    @staticmethod
    def _context_collecting_hook(fnc):
        pass

    _collect = None

    @classmethod
    def assemble_context(cls):
        cls._collect = []
        ma = Accumulator(cls.member_type_rule, cls.naming_rule)
        for fnc in map(parse_func, lines_to_statements(cls.lines())):
            if fnc['name'] in cls.skip_funcs:
                continue
            try:
                processed = process_function(fnc, 'obj.{fname}({args})')
                hooked = cls._context_collecting_hook(fnc)
            except AssertionError as e:
                outerr(e)
            else:
                ma(fnc, processed)
                cls._collect.append(hooked)
        meths = list(ma.assemble())
        for m in meths:
            if m['orig_name'] in cls.force_lambda:
                m['processed']['transformed'] = True
        return {
            'source_ns': 'BWAPI::',
            'source_class': cls.mapped_class,
            'py_name': cls.python_name(),
            'methods': meths,
            'constructors': cls.constructors,
            'helper_ns': 'PyBinding::Wrapper::',
        }


class BaseWrappedClassFile(BaseClassFile):
    unboxed = False
    wobj_op = 'obj->'

    @classmethod
    def perform(cls):
        lcl = cls.python_name().lower()

        context = cls.assemble_context()
        wrap_context = cls.assemble_wrapper_context()

        with open(join(GEN_OUTPUT_DIR, 'include', '{}.h'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('wrapper/h.jinja2').render(**wrap_context)))
        with open(join(GEN_OUTPUT_DIR, 'src', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('wrapper/cpp.jinja2').render(**wrap_context)))

        with open(join(GEN_OUTPUT_DIR, 'pybind', '{}.cpp'.format(lcl)), 'w') as f:
            f.write(html_unescape(jin_env.get_template('class.jinja2').render(**context)))

    @classmethod
    def assemble_context(cls):
        ctx = super().assemble_context()
        # ctx = BaseClassFile.assemble_context(cls)
        ctx['source_ns'] = 'PyBinding::Wrapper::'
        return ctx

    @classmethod
    def _context_collecting_hook(cls, fnc):
        processed = process_function(fnc, cls.wobj_op + '{fname}({args})', asis=True)
        processed['orig'] = fnc
        return processed

    @classmethod
    def assemble_wrapper_context(cls):
        return {
            'source_ns': 'BWAPI::',
            'source_classptr': cls.mapped_class,
            'wrap_class': cls.mapped_class,
            'methods': cls._collect,
            'header_file': cls.include_file(),
            'initmod': '*' if cls.unboxed else '',
        }

    @staticmethod
    def _arg_check(a):
        assert not a['const'], 'Const arguments not supported in wrapped types ' + repr(a)
        assert a['opt_value'] is None, 'Value defaults not supported in wrapped types ' + repr(a)

    @classmethod
    def arg_transformer(cls, a):
        cls._arg_check(a)
        a['type'] = '{ns}' + a['type']

    @staticmethod
    def arg_expr(a):
        return a['name'] + '.obj'

    @staticmethod
    def ret_transformer(f):
        f['rtype'] = '{ns}' + f['rtype']

    @classmethod
    def ret_expr(cls, f):
        return 'return {{ns}}{}({{expr}});'.format(cls.mapped_class)

    @classmethod
    def include_file(cls):
        lcl = cls.python_name().lower()
        return lcl + '.h'
