# Pybrood

[![docs](https://readthedocs.org/projects/pybrood/badge/?version=latest)](http://pybrood.readthedocs.io/en/latest/)

Binding made as from-scratch code generator, outputting msvc project.

## Precompiled installation

Requirements:

- Windows 7 32 bit (just exactly SSCAIT requirement)
  NOTE: I couldn't successfully run BWAPI injector under Wine, although recently I've been told
  [it's possible](https://github.com/TorchCraft/TorchCraft/blob/master/docs/user/bwapi_on_linux.md).
- [Python 3.5](https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe)
- Installed BWAPI and SC

```
pip install pybrood
```

## Documentation

[Read the docs](http://pybrood.readthedocs.io/en/latest/)

## Compiling from source

Additional requirements:

- [Visual C++ build tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) or complete Visual Studio.
  NOTE: pick the version of compiler/studio considering [build tools used by python](https://wiki.python.org/moin/WindowsCompilers)
- [BWAPI 4.1.2 sources](https://github.com/bwapi/bwapi/releases/tag/v4.1.2)
  you need `BWAPI.lib` and `BWAPIClient.lib` built against chosen compiler to link pybrood module
- Most fresh (dec 2016) [Pybind11 headers](https://github.com/pybind/pybind11)

#### Building BWAPI.lib and BWAPIClient.lib

You may experience "access denied" errors while working directly in "program files/BWAPI".
Better use separately cloned git repo of BWAPI where you have full access.

For `msbuild` invocation use special VC++ related cmd shell from Launch menu.
Otherwise you can use usual cmd shell.

1. Make some changes in bwapi source files first:

   - disable mass file copying in `bwapi/BWAPILIB/BWAPILIB.vcxproj`:

     - line 64: `<PreLinkEvent>` → `<!-- PreLinkEvent>`
     - line 94: `</PreLinkEvent>` → `</PreLinkEvent -->`

   - create file `bwapi/svnrev.h`:

     Figure out revision number:

     ```bash
     cd bwapi
     echo $(( $(git rev-list HEAD --count) + 2383 ))
     ```

     ```cpp
     static const int SVN_REV = 4708;
     #include "starcraftver.h"
     ```

     This prevents "Client and Server are not compatible" error.

2. Build BWAPI.lib:

   ```
   cd bwapi\BWAPILIB\
   msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32
   ```

   Output file is `bwapi/lib/BWAPI.lib`.

3. Build BWAPIClient.lib:

   ```
   cd bwapi\BWAPIClient\
   msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32
   ```

   Output file is `bwapi/lib/BWAPIClient.lib`.

#### Building Pybrood

0. `pip install -r generator/requirements.txt`
1. Setup paths in [generator/config.py](generator/config.py).
2. Run the generator `python3.5 -m generator`.
3. `cd` to freshly generated `output` folder and run `build.bat` (it's just the same msbuild command).
4. Copy/symlink `output/Release/inner.pyd` into `pybrood` directory.
   `inner.pyd` is a required submodule of `pybrood`.
5. Now you should be able to `import pybrood`.
6. Optionally you can build your local copy of documentation:
   ```
   cd output/docs/
   sphinx-build . -b html _build/html
   ```
