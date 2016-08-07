from .config import GEN_OUTPUT_DIR, BWAPI_DIR, PYBIND_DIR
from os import mkdir, listdir
from os.path import join, isdir, relpath
from .utils import jin_env
from pathlib import PureWindowsPath
from .typereplacer import WEAKREF_MAP


def makedir(*path):
    path = join(*path)
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
        f.write(jin_env.get_template('common_h.jinja2').render(
            classes=WEAKREF_MAP.values(),
        ))


def post():
    with open(join(GEN_OUTPUT_DIR, 'pybrood.vcxproj'), 'w') as f:
        f.write(jin_env.get_template('vcproj.jinja2').render(
            bwapi_dir=PureWindowsPath(relpath(BWAPI_DIR, GEN_OUTPUT_DIR)),
            pybind_dir=PureWindowsPath(relpath(PYBIND_DIR, GEN_OUTPUT_DIR)),
            cpp_files=listdir(join(GEN_OUTPUT_DIR, 'src')),
        ))

    with open(join(GEN_OUTPUT_DIR, 'pybrood.cpp'), 'w') as f:
        f.write(jin_env.get_template('pybrood_cpp.jinja2').render(
            cpp_files=listdir(join(GEN_OUTPUT_DIR, 'pybind')),
            h_files=filter(lambda x: x != 'common.h', listdir(join(GEN_OUTPUT_DIR, 'include'))),
        ))
