from . import weakrefs
from . import singletons
from . import skel


skel.pre()

weakrefs.UnitFile.perform()
weakrefs.UnitTypeFile.perform()
weakrefs.ForceFile.perform()
weakrefs.PlayerFile.perform()
weakrefs.BulletTypeFile.perform()
weakrefs.DamageTypeFile.perform()
weakrefs.UpgradeTypeFile.perform()
weakrefs.WeaponTypeFile.perform()
weakrefs.PlayerTypeFile.perform()

singletons.main()

skel.post()
