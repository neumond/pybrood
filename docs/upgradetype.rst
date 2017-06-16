UpgradeType
===========

Class
-----

.. py:class:: pybrood.UpgradeType

    .. py:method:: getID() -> int
    .. py:method:: getName() -> str
    .. py:method:: getRace() -> Race
    .. py:method:: mineralPrice(level: int=1) -> int
    .. py:method:: mineralPriceFactor() -> int
    .. py:method:: gasPrice(level: int=1) -> int
    .. py:method:: gasPriceFactor() -> int
    .. py:method:: upgradeTime(level: int=1) -> int
    .. py:method:: upgradeTimeFactor() -> int
    .. py:method:: maxRepeats() -> int
    .. py:method:: whatUpgrades() -> UnitType
    .. py:method:: whatsRequired(level: int=1) -> UnitType
    .. py:method:: whatUses() -> list


Enumeration
-----------

.. py:data:: pybrood.UpgradeTypes

    .. py:attribute:: Terran_Infantry_Armor
    .. py:attribute:: Terran_Vehicle_Plating
    .. py:attribute:: Terran_Ship_Plating
    .. py:attribute:: Terran_Infantry_Weapons
    .. py:attribute:: Terran_Vehicle_Weapons
    .. py:attribute:: Terran_Ship_Weapons
    .. py:attribute:: U_238_Shells
    .. py:attribute:: Ion_Thrusters
    .. py:attribute:: Titan_Reactor
    .. py:attribute:: Ocular_Implants
    .. py:attribute:: Moebius_Reactor
    .. py:attribute:: Apollo_Reactor
    .. py:attribute:: Colossus_Reactor
    .. py:attribute:: Caduceus_Reactor
    .. py:attribute:: Charon_Boosters
    .. py:attribute:: Zerg_Carapace
    .. py:attribute:: Zerg_Flyer_Carapace
    .. py:attribute:: Zerg_Melee_Attacks
    .. py:attribute:: Zerg_Missile_Attacks
    .. py:attribute:: Zerg_Flyer_Attacks
    .. py:attribute:: Ventral_Sacs
    .. py:attribute:: Antennae
    .. py:attribute:: Pneumatized_Carapace
    .. py:attribute:: Metabolic_Boost
    .. py:attribute:: Adrenal_Glands
    .. py:attribute:: Muscular_Augments
    .. py:attribute:: Grooved_Spines
    .. py:attribute:: Gamete_Meiosis
    .. py:attribute:: Metasynaptic_Node
    .. py:attribute:: Chitinous_Plating
    .. py:attribute:: Anabolic_Synthesis
    .. py:attribute:: Protoss_Ground_Armor
    .. py:attribute:: Protoss_Air_Armor
    .. py:attribute:: Protoss_Ground_Weapons
    .. py:attribute:: Protoss_Air_Weapons
    .. py:attribute:: Protoss_Plasma_Shields
    .. py:attribute:: Singularity_Charge
    .. py:attribute:: Leg_Enhancements
    .. py:attribute:: Scarab_Damage
    .. py:attribute:: Reaver_Capacity
    .. py:attribute:: Gravitic_Drive
    .. py:attribute:: Sensor_Array
    .. py:attribute:: Gravitic_Boosters
    .. py:attribute:: Khaydarin_Amulet
    .. py:attribute:: Apial_Sensors
    .. py:attribute:: Gravitic_Thrusters
    .. py:attribute:: Carrier_Capacity
    .. py:attribute:: Khaydarin_Core
    .. py:attribute:: Argus_Jewel
    .. py:attribute:: Argus_Talisman
    .. py:attribute:: Upgrade_60
    .. py:attribute:: None_
    .. py:attribute:: Unknown
