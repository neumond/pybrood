# Pybrood

[![docs](https://readthedocs.org/projects/pybrood/badge/?version=latest)](http://pybrood.readthedocs.io/en/latest/)

Binding made as from-scratch code generator, outputting msvc project.

## Requirements

- Windows 7 32 bit (just exactly SSCAIT requirement)
  NOTE: I couldn't successfully run BWAPI injector under Wine, although recently I've been told
  [it's possible](https://github.com/TorchCraft/TorchCraft/blob/master/docs/user/bwapi_on_linux.md).
- [Python 3.5](https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe)
- [Visual C++ build tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) or complete Visual Studio.
  NOTE: pick the version of compiler/studio considering [build tools used by python](https://wiki.python.org/moin/WindowsCompilers)
- [BWAPI 4.1.2 sources](https://github.com/bwapi/bwapi/releases/tag/v4.1.2) (small patching required)
- Most fresh (dec 2016) [Pybind11 headers](https://github.com/pybind/pybind11)

## Building BWAPI

You may experience "access denied" errors while working directly in "program files/BWAPI".
Better use separately cloned git repo of BWAPI where you have full access.

For `msbuild` invocation use special VC++ related cmd shell from Launch menu.
Otherwise you can use usual cmd shell.

1. Make little fix in `bwapi/include/BWAPI/SetContainer.h:54`:
   at very end of class add `SetContainer& operator=(const SetContainer&) = default;`
   to get rid of `attempting to reference a deleted function` error.
2. Goto bwapi dir, then `msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32`.
   This will build whole solution (except BWAPILibTest and BWMemoryEdit).
   Separate projects can be built by cd to project dir and launching same command.
   In my case I have vs2015 (dictated by python3.5 choice), thus I've forced toolset version with `/p:PlatformToolset=v140`.
3. Building plugininjector requires replacing paths in vcxproj file:
   replace all `../` to `../../` until msbuild passes (that's simply bad paths for copy command).
4. Running ExampleAIClient.exe (you need to build it manually, exactly same msbuild command)
   will message you about incompatible server, you need to install your freshly built files:
   - `bwapi\Release_Binary\Chaoslauncher\Plugins\BWAPI_PluginInjector.bwl` into `C:\Program files\BWAPI\Chaoslauncher\Plugins\`
   - `bwapi\bwapi\Release\BWAPI.dll` into `C:\Program files\StarCraft\bwapi-data\`

## Building Pybrood

1. Setup paths in [config.py](generator/config.py).
2. Run the generator `python3.5 -m generator`.
3. `cd` to freshly generated `output` folder and run `build.bat` (it's just the same msbuild command).
4. Now you can copy/symlink `output/Release/pybrood.pyd` into directory with your code.
   It will be importable as usual python module: `import pybrood`.

## Documentation

[Read the docs](http://pybrood.readthedocs.io/en/latest/)
