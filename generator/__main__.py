from . import weakrefs
from . import singletons
from . import skel


skel.pre()

for Sub in weakrefs.BaseWeakrefFile.__subclasses__():
    Sub.perform()

singletons.main()

skel.post()
