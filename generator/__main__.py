from . import skel, proxy_classes
# from . import pureenums
# from . import classes
# from . import classenums
# from . import bwapi_classes  # noqa


skel.pre()

# proxy_classes.main()

# for Sub in classes.BaseClassFile.__subclasses__():
#     if Sub is not classes.BaseWrappedClassFile:
#         Sub.perform()
# for Sub in classes.BaseWrappedClassFile.__subclasses__():
#     Sub.perform()
# for Sub in classenums.BaseClassEnumFile.__subclasses__():
#     Sub.perform()
#
# for Sub in pureenums.BasePureEnumFile.__subclasses__():
#     Sub.perform()

skel.post()
