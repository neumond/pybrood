Region
======

Class
-----

.. py:class:: pybrood.Region

    .. py:method:: getID() -> int
    .. py:method:: getRegionGroupID() -> int
    .. py:method:: getCenter() -> Tuple[int, int]
    .. py:method:: isHigherGround() -> bool
    .. py:method:: getDefensePriority() -> int
    .. py:method:: isAccessible() -> bool
    .. py:method:: getNeighbors() -> Regionset
    .. py:method:: getBoundsLeft() -> int
    .. py:method:: getBoundsTop() -> int
    .. py:method:: getBoundsRight() -> int
    .. py:method:: getBoundsBottom() -> int
    .. py:method:: getClosestAccessibleRegion() -> Region
    .. py:method:: getClosestInaccessibleRegion() -> Region
    .. py:method:: getDistance(other: Region) -> int
    .. py:method:: getUnits() -> Unitset

