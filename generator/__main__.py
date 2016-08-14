# from . import singletons
from . import skel
from . import pureenums
from . import classes
from . import bwapi_classes  # noqa
from .typereplacer import register_types

register_types()

skel.pre()

for Sub in classes.BaseClassFile.__subclasses__():
    if Sub is not classes.BaseWrappedClassFile:
        Sub.perform()
for Sub in classes.BaseWrappedClassFile.__subclasses__():
    Sub.perform()

# singletons.main()

for Sub in pureenums.BasePureEnumFile.__subclasses__():
    Sub.perform()

skel.post()
