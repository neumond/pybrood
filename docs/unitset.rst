Unitset
=======

Class
-----

.. py:class:: pybrood.Unitset

    .. py:method:: getPosition() -> Tuple[int, int]
    .. py:method:: getLoadedUnits() -> Unitset
    .. py:method:: getInterceptors() -> Unitset
    .. py:method:: getLarva() -> Unitset
    .. py:method:: getUnitsInRadius(radius: int) -> Unitset
    .. py:method:: getClosestUnit(radius: int=999999) -> Unit
    .. py:method:: attack(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool
    .. py:method:: attack(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: build(type: UnitType, target: Tuple[int, int]=TILEPOSITION_NONE) -> bool
    .. py:method:: buildAddon(type: UnitType) -> bool
    .. py:method:: train(type: UnitType) -> bool
    .. py:method:: morph(type: UnitType) -> bool
    .. py:method:: setRallyPoint(target: Unit) -> bool
    .. py:method:: setRallyPoint(target: Tuple[int, int]) -> bool
    .. py:method:: move(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool
    .. py:method:: patrol(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool
    .. py:method:: holdPosition(shiftQueueCommand: bool=False) -> bool
    .. py:method:: stop(shiftQueueCommand: bool=False) -> bool
    .. py:method:: follow(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: gather(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: returnCargo(shiftQueueCommand: bool=False) -> bool
    .. py:method:: repair(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: burrow() -> bool
    .. py:method:: unburrow() -> bool
    .. py:method:: cloak() -> bool
    .. py:method:: decloak() -> bool
    .. py:method:: siege() -> bool
    .. py:method:: unsiege() -> bool
    .. py:method:: lift() -> bool
    .. py:method:: load(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: unloadAll(shiftQueueCommand: bool=False) -> bool
    .. py:method:: unloadAll(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool
    .. py:method:: rightClick(target: Unit, shiftQueueCommand: bool=False) -> bool
    .. py:method:: rightClick(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool
    .. py:method:: haltConstruction() -> bool
    .. py:method:: cancelConstruction() -> bool
    .. py:method:: cancelAddon() -> bool
    .. py:method:: cancelTrain(slot: int=-2) -> bool
    .. py:method:: cancelMorph() -> bool
    .. py:method:: cancelResearch() -> bool
    .. py:method:: cancelUpgrade() -> bool
    .. py:method:: useTech(tech: TechType, target: Unit=None) -> bool
    .. py:method:: useTech(tech: TechType, target: Tuple[int, int]) -> bool

