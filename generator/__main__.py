from . import skel
from . import pureenums
from . import classes
from . import classenums
from . import bwapi_classes  # noqa
from .typereplacer import register_types

register_types()

skel.pre()

for Sub in classes.BaseClassFile.__subclasses__():
    if Sub is not classes.BaseWrappedClassFile:
        Sub.perform()
for Sub in classes.BaseWrappedClassFile.__subclasses__():
    Sub.perform()
for Sub in classenums.BaseClassEnumFile.__subclasses__():
    Sub.perform()

for Sub in pureenums.BasePureEnumFile.__subclasses__():
    Sub.perform()

skel.post()
