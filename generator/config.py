from pathlib import PureWindowsPath
from os.path import join, relpath


# paths used at code generation stage

GEN_OUTPUT_DIR = 'output'
PYBIND_DIR = join('..', 'pybind11')  # TODO: not actually used by generator, remove
BWAPI_SOURCE_DIR = join('..', 'bwapi')
BWAPI_INCLUDE_DIR = join(BWAPI_SOURCE_DIR, 'bwapi', 'include', 'BWAPI')


def spaths(*items):
    return ';'.join(map(str, items))


class VCXProjectConfig:
    MSBUILD_COMMAND = 'msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32'

    # substitions in vcxproj file

    PYTHON_DIR = PureWindowsPath('C:/Users/IEUser/AppData/Local/Programs/Python/Python35-32')
    PYBIND_DIR = PureWindowsPath(relpath(PYBIND_DIR, GEN_OUTPUT_DIR))
    BWAPI_DIR = PureWindowsPath(relpath(BWAPI_SOURCE_DIR, GEN_OUTPUT_DIR))

    INCLUDE_DIRS = spaths(
        PYTHON_DIR.joinpath('include'),
        PYBIND_DIR.joinpath('include'),
        BWAPI_DIR.joinpath('bwapi', 'include'),
    )
    RELEASE_LIBS = spaths(
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPI.lib'),
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPIClient.lib'),
        PYTHON_DIR.joinpath('libs', 'python35.lib'),
    )
    DEBUG_LIBS = spaths(
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPId.lib'),
        BWAPI_DIR.joinpath('bwapi', 'lib', 'BWAPIClientd.lib'),
        # TODO: python debug lib
    )
