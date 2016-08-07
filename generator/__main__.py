from . import weakrefs
from . import singletons
from . import skel
from . import pureenums


skel.pre()

for Sub in weakrefs.BaseWeakrefFile.__subclasses__():
    Sub.perform()

singletons.main()

for Sub in pureenums.BasePureEnumFile.__subclasses__():
    Sub.perform()

skel.post()
