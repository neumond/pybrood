from pathlib import PureWindowsPath
from os.path import join, relpath

# paths used at code generation stage
# generator can be launched on different OS, using here agnostic os.path operations

GEN_OUTPUT_DIR = 'output'
BWAPI_SOURCE_DIR = join('..', 'bwapi')
BWAPI_INCLUDE_DIR = join(BWAPI_SOURCE_DIR, 'bwapi', 'include', 'BWAPI')

# paths used at compilation stage
# must be Windows-specific

PYTHON_VERSION = '36'
# default installation path for python libs
PYTHON_DIR = PureWindowsPath('C:/Users/IEUser/AppData/Local/Programs/Python/Python{}-32'.format(PYTHON_VERSION))
# your path to pybind11 here
PYBIND_DIR = PureWindowsPath(relpath(join('..', 'pybind11'), GEN_OUTPUT_DIR))
# your path to bwapi here
BWAPI_DIR = PureWindowsPath(relpath(BWAPI_SOURCE_DIR, GEN_OUTPUT_DIR))


# everything below should work as is

def spaths(*items):
    return ';'.join(map(str, items))


class VCXProjectConfig:
    MSBUILD_COMMAND = 'msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32'

    # substitions in vcxproj file

    INCLUDE_DIRS = spaths(
        PYTHON_DIR.joinpath('include'),
        PYBIND_DIR.joinpath('include'),
        BWAPI_DIR.joinpath('bwapi', 'include'),
    )
    RELEASE_LIBS = spaths(
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPI.lib'),
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPIClient.lib'),
        PYTHON_DIR.joinpath('libs', 'python{}.lib'.format(PYTHON_VERSION)),
    )
    DEBUG_LIBS = spaths(
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPId.lib'),
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPIClientd.lib'),
        # TODO: python debug lib
    )
