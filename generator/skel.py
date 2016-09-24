from .config import GEN_OUTPUT_DIR, BWAPI_DIR, PYBIND_DIR
from os import mkdir, listdir
from os.path import join, isdir, relpath
from .utils import render_template
from pathlib import PureWindowsPath
from shutil import rmtree
# from .classes import BaseWrappedClassFile
from .parser.pureenums import main as get_data_pureenums
from .parser.objenums import main as get_data_objenums
from .direct_classes import main as get_data_classes


def render_pureenums():
    for py_name, v in get_data_pureenums().items():
        yield render_template('pureenum.jinja2', py_name=py_name, **v)


def render_classes():
    for py_name, v in get_data_classes().items():
        yield render_template('direct_class.jinja2', py_name=py_name, **v)


def render_objenums():
    for py_name, v in get_data_objenums().items():
        yield render_template('objenum.jinja2', py_name=py_name, **v)


def makedir(*path):
    path = join(*path)
    if isdir(path):
        rmtree(path)
    if not isdir(path):
        mkdir(path)


def pre():
    makedir(GEN_OUTPUT_DIR)
    makedir(GEN_OUTPUT_DIR, 'src')
    makedir(GEN_OUTPUT_DIR, 'include')
    makedir(GEN_OUTPUT_DIR, 'pybind')

    with open(join(GEN_OUTPUT_DIR, 'build.bat'), 'w') as f:
        f.write('msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32')

    # with open(join(GEN_OUTPUT_DIR, 'include', 'common.h'), 'w') as f:
    #     f.write(html_unescape(jin_env.get_template('common_h.jinja2').render(
    #         classes=cs,
    #     )))


def all_cpp_files():
    items = listdir(join(GEN_OUTPUT_DIR, 'pybind'))
    a, b = [], []
    for x in items:
        (b if x.endswith('_items.cpp') else a).append(x)
    return a + b


def post():
    with open(join(GEN_OUTPUT_DIR, 'pybrood.vcxproj'), 'w') as f:
        f.write(render_template(
            'vcproj.jinja2',
            bwapi_dir=PureWindowsPath(relpath(BWAPI_DIR, GEN_OUTPUT_DIR)),
            pybind_dir=PureWindowsPath(relpath(PYBIND_DIR, GEN_OUTPUT_DIR)),
            cpp_files=listdir(join(GEN_OUTPUT_DIR, 'src')),
        ))

    with open(join(GEN_OUTPUT_DIR, 'pybrood.cpp'), 'w') as f:
        f.write(render_template(
            'pybrood_cpp.jinja2',
            pureenums=list(render_pureenums()),
            classes=list(render_classes()),
            objenums=list(render_objenums()),
        ))
        # cpp_files=all_cpp_files(),
        # h_files=filter(lambda x: x != 'common.h', listdir(join(GEN_OUTPUT_DIR, 'include'))),
