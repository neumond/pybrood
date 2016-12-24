Player
======

Class
-----

.. py:class:: pybrood.Player

    .. py:method:: getID() -> int

    .. py:method:: getName() -> str

    .. py:method:: getUnits() -> Unitset

    .. py:method:: getRace() -> Race

    .. py:method:: getType() -> PlayerType

    .. py:method:: getForce() -> Force

    .. py:method:: isAlly(player: Player) -> bool

    .. py:method:: isEnemy(player: Player) -> bool

    .. py:method:: isNeutral() -> bool

    .. py:method:: getStartLocation() -> Tuple[int, int]

    .. py:method:: isVictorious() -> bool

    .. py:method:: isDefeated() -> bool

    .. py:method:: leftGame() -> bool

    .. py:method:: minerals() -> int

    .. py:method:: gas() -> int

    .. py:method:: gatheredMinerals() -> int

    .. py:method:: gatheredGas() -> int

    .. py:method:: repairedMinerals() -> int

    .. py:method:: repairedGas() -> int

    .. py:method:: refundedMinerals() -> int

    .. py:method:: refundedGas() -> int

    .. py:method:: spentMinerals() -> int

    .. py:method:: spentGas() -> int

    .. py:method:: supplyTotal(race: Race=Races.None) -> int

    .. py:method:: supplyUsed(race: Race=Races.None) -> int

    .. py:method:: allUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: visibleUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: completedUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: incompleteUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: deadUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: killedUnitCount(unit: UnitType=UnitTypes.AllUnits) -> int

    .. py:method:: getUpgradeLevel(upgrade: UpgradeType) -> int

    .. py:method:: hasResearched(tech: TechType) -> bool

    .. py:method:: isResearching(tech: TechType) -> bool

    .. py:method:: isUpgrading(upgrade: UpgradeType) -> bool

    .. py:method:: getColor() -> Color

    .. py:method:: getTextColor() -> str

    .. py:method:: maxEnergy(unit: UnitType) -> int

    .. py:method:: topSpeed(unit: UnitType) -> float

    .. py:method:: weaponMaxRange(weapon: WeaponType) -> int

    .. py:method:: sightRange(unit: UnitType) -> int

    .. py:method:: weaponDamageCooldown(unit: UnitType) -> int

    .. py:method:: armor(unit: UnitType) -> int

    .. py:method:: damage(wpn: WeaponType) -> int

    .. py:method:: getUnitScore() -> int

    .. py:method:: getKillScore() -> int

    .. py:method:: getBuildingScore() -> int

    .. py:method:: getRazingScore() -> int

    .. py:method:: getCustomScore() -> int

    .. py:method:: isObserver() -> bool

    .. py:method:: getMaxUpgradeLevel(upgrade: UpgradeType) -> int

    .. py:method:: isResearchAvailable(tech: TechType) -> bool

    .. py:method:: isUnitAvailable(unit: UnitType) -> bool

    .. py:method:: hasUnitTypeRequirement(unit: UnitType, amount: int=1) -> bool


