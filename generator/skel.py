from .config import GEN_OUTPUT_DIR, BWAPI_DIR, PYBIND_DIR
from os import mkdir, listdir
from os.path import join, isdir, relpath
from .utils import render_template
from pathlib import PureWindowsPath
from shutil import rmtree
from .parser import parse_pureenums
# from .parser.objenums import main as get_data_objenums
# from .direct_classes import main as get_data_classes
# from .proxy_classes import main as make_proxy_classes


def render_pureenums():
    for py_name, v in parse_pureenums().items():
        yield render_template('pureenum.jinja2', py_name=py_name, **v)


# def render_classes():
#     cl_data = get_data_classes()
#     for py_name, v in cl_data.items():
#         yield render_template('direct_class.jinja2', py_name=py_name, **v)
#     make_proxy_classes(cl_data)


# def render_objenums():
#     for py_name, v in get_data_objenums().items():
#         yield render_template('objenum.jinja2', py_name=py_name, **v)


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

    with open(join(GEN_OUTPUT_DIR, 'include', 'common.h'), 'w') as f:
        f.write(render_template('common_h.jinja2', classes=[]))


def post():
    pureenums = list(render_pureenums())
    # classes = list(render_classes())
    classes = []
    # objenums = list(render_objenums())
    objenums = []

    h_files = listdir(join(GEN_OUTPUT_DIR, 'include'))
    h_files.remove('common.h')

    with open(join(GEN_OUTPUT_DIR, 'pybrood.cpp'), 'w') as f:
        f.write(render_template(
            'pybrood_cpp.jinja2',
            pureenums=pureenums,
            classes=classes,
            objenums=objenums,
            h_files=h_files,
        ))

    with open(join(GEN_OUTPUT_DIR, 'pybrood.vcxproj'), 'w') as f:
        f.write(render_template(
            'vcproj.jinja2',
            bwapi_dir=PureWindowsPath(relpath(BWAPI_DIR, GEN_OUTPUT_DIR)),
            pybind_dir=PureWindowsPath(relpath(PYBIND_DIR, GEN_OUTPUT_DIR)),
            cpp_files=listdir(join(GEN_OUTPUT_DIR, 'src')),
        ))
