UnitType
========

Class
-----

.. py:class:: pybrood.UnitType

    .. py:method:: getID() -> int

    .. py:method:: getName() -> str

    .. py:method:: getRace() -> Race

    .. py:method:: whatBuilds() -> Tuple[UnitType, int]

    .. py:method:: requiredUnits() -> Dict[UnitType, int]

    .. py:method:: requiredTech() -> TechType

    .. py:method:: cloakingTech() -> TechType

    .. py:method:: abilities() -> list

    .. py:method:: upgrades() -> list

    .. py:method:: armorUpgrade() -> UpgradeType

    .. py:method:: maxHitPoints() -> int

    .. py:method:: maxShields() -> int

    .. py:method:: maxEnergy() -> int

    .. py:method:: armor() -> int

    .. py:method:: mineralPrice() -> int

    .. py:method:: gasPrice() -> int

    .. py:method:: buildTime() -> int

    .. py:method:: supplyRequired() -> int

    .. py:method:: supplyProvided() -> int

    .. py:method:: spaceRequired() -> int

    .. py:method:: spaceProvided() -> int

    .. py:method:: buildScore() -> int

    .. py:method:: destroyScore() -> int

    .. py:method:: size() -> UnitSizeType

    .. py:method:: tileWidth() -> int

    .. py:method:: tileHeight() -> int

    .. py:method:: tileSize() -> Tuple[int, int]

    .. py:method:: dimensionLeft() -> int

    .. py:method:: dimensionUp() -> int

    .. py:method:: dimensionRight() -> int

    .. py:method:: dimensionDown() -> int

    .. py:method:: width() -> int

    .. py:method:: height() -> int

    .. py:method:: seekRange() -> int

    .. py:method:: sightRange() -> int

    .. py:method:: groundWeapon() -> WeaponType

    .. py:method:: maxGroundHits() -> int

    .. py:method:: airWeapon() -> WeaponType

    .. py:method:: maxAirHits() -> int

    .. py:method:: topSpeed() -> float

    .. py:method:: acceleration() -> int

    .. py:method:: haltDistance() -> int

    .. py:method:: turnRadius() -> int

    .. py:method:: canProduce() -> bool

    .. py:method:: canAttack() -> bool

    .. py:method:: canMove() -> bool

    .. py:method:: isFlyer() -> bool

    .. py:method:: regeneratesHP() -> bool

    .. py:method:: isSpellcaster() -> bool

    .. py:method:: hasPermanentCloak() -> bool

    .. py:method:: isInvincible() -> bool

    .. py:method:: isOrganic() -> bool

    .. py:method:: isMechanical() -> bool

    .. py:method:: isRobotic() -> bool

    .. py:method:: isDetector() -> bool

    .. py:method:: isResourceContainer() -> bool

    .. py:method:: isResourceDepot() -> bool

    .. py:method:: isRefinery() -> bool

    .. py:method:: isWorker() -> bool

    .. py:method:: requiresPsi() -> bool

    .. py:method:: requiresCreep() -> bool

    .. py:method:: isTwoUnitsInOneEgg() -> bool

    .. py:method:: isBurrowable() -> bool

    .. py:method:: isCloakable() -> bool

    .. py:method:: isBuilding() -> bool

    .. py:method:: isAddon() -> bool

    .. py:method:: isFlyingBuilding() -> bool

    .. py:method:: isNeutral() -> bool

    .. py:method:: isHero() -> bool

    .. py:method:: isPowerup() -> bool

    .. py:method:: isBeacon() -> bool

    .. py:method:: isFlagBeacon() -> bool

    .. py:method:: isSpecialBuilding() -> bool

    .. py:method:: isSpell() -> bool

    .. py:method:: producesCreep() -> bool

    .. py:method:: producesLarva() -> bool

    .. py:method:: isMineralField() -> bool

    .. py:method:: isCritter() -> bool

    .. py:method:: canBuildAddon() -> bool

    .. py:method:: buildsWhat() -> list

    .. py:method:: researchesWhat() -> list

    .. py:method:: upgradesWhat() -> list



Enumeration
-----------

.. py:data:: pybrood.UnitTypes

    .. py:attribute:: Terran_Firebat
    .. py:attribute:: Terran_Ghost
    .. py:attribute:: Terran_Goliath
    .. py:attribute:: Terran_Marine
    .. py:attribute:: Terran_Medic
    .. py:attribute:: Terran_SCV
    .. py:attribute:: Terran_Siege_Tank_Siege_Mode
    .. py:attribute:: Terran_Siege_Tank_Tank_Mode
    .. py:attribute:: Terran_Vulture
    .. py:attribute:: Terran_Vulture_Spider_Mine
    .. py:attribute:: Terran_Battlecruiser
    .. py:attribute:: Terran_Dropship
    .. py:attribute:: Terran_Nuclear_Missile
    .. py:attribute:: Terran_Science_Vessel
    .. py:attribute:: Terran_Valkyrie
    .. py:attribute:: Terran_Wraith
    .. py:attribute:: Hero_Alan_Schezar
    .. py:attribute:: Hero_Alexei_Stukov
    .. py:attribute:: Hero_Arcturus_Mengsk
    .. py:attribute:: Hero_Edmund_Duke_Tank_Mode
    .. py:attribute:: Hero_Edmund_Duke_Siege_Mode
    .. py:attribute:: Hero_Gerard_DuGalle
    .. py:attribute:: Hero_Gui_Montag
    .. py:attribute:: Hero_Hyperion
    .. py:attribute:: Hero_Jim_Raynor_Marine
    .. py:attribute:: Hero_Jim_Raynor_Vulture
    .. py:attribute:: Hero_Magellan
    .. py:attribute:: Hero_Norad_II
    .. py:attribute:: Hero_Samir_Duran
    .. py:attribute:: Hero_Sarah_Kerrigan
    .. py:attribute:: Hero_Tom_Kazansky
    .. py:attribute:: Terran_Civilian
    .. py:attribute:: Terran_Academy
    .. py:attribute:: Terran_Armory
    .. py:attribute:: Terran_Barracks
    .. py:attribute:: Terran_Bunker
    .. py:attribute:: Terran_Command_Center
    .. py:attribute:: Terran_Engineering_Bay
    .. py:attribute:: Terran_Factory
    .. py:attribute:: Terran_Missile_Turret
    .. py:attribute:: Terran_Refinery
    .. py:attribute:: Terran_Science_Facility
    .. py:attribute:: Terran_Starport
    .. py:attribute:: Terran_Supply_Depot
    .. py:attribute:: Terran_Comsat_Station
    .. py:attribute:: Terran_Control_Tower
    .. py:attribute:: Terran_Covert_Ops
    .. py:attribute:: Terran_Machine_Shop
    .. py:attribute:: Terran_Nuclear_Silo
    .. py:attribute:: Terran_Physics_Lab
    .. py:attribute:: Special_Crashed_Norad_II
    .. py:attribute:: Special_Ion_Cannon
    .. py:attribute:: Special_Power_Generator
    .. py:attribute:: Special_Psi_Disrupter
    .. py:attribute:: Protoss_Archon
    .. py:attribute:: Protoss_Dark_Archon
    .. py:attribute:: Protoss_Dark_Templar
    .. py:attribute:: Protoss_Dragoon
    .. py:attribute:: Protoss_High_Templar
    .. py:attribute:: Protoss_Probe
    .. py:attribute:: Protoss_Reaver
    .. py:attribute:: Protoss_Scarab
    .. py:attribute:: Protoss_Zealot
    .. py:attribute:: Protoss_Arbiter
    .. py:attribute:: Protoss_Carrier
    .. py:attribute:: Protoss_Corsair
    .. py:attribute:: Protoss_Interceptor
    .. py:attribute:: Protoss_Observer
    .. py:attribute:: Protoss_Scout
    .. py:attribute:: Protoss_Shuttle
    .. py:attribute:: Hero_Aldaris
    .. py:attribute:: Hero_Artanis
    .. py:attribute:: Hero_Danimoth
    .. py:attribute:: Hero_Dark_Templar
    .. py:attribute:: Hero_Fenix_Dragoon
    .. py:attribute:: Hero_Fenix_Zealot
    .. py:attribute:: Hero_Gantrithor
    .. py:attribute:: Hero_Mojo
    .. py:attribute:: Hero_Raszagal
    .. py:attribute:: Hero_Tassadar
    .. py:attribute:: Hero_Tassadar_Zeratul_Archon
    .. py:attribute:: Hero_Warbringer
    .. py:attribute:: Hero_Zeratul
    .. py:attribute:: Protoss_Arbiter_Tribunal
    .. py:attribute:: Protoss_Assimilator
    .. py:attribute:: Protoss_Citadel_of_Adun
    .. py:attribute:: Protoss_Cybernetics_Core
    .. py:attribute:: Protoss_Fleet_Beacon
    .. py:attribute:: Protoss_Forge
    .. py:attribute:: Protoss_Gateway
    .. py:attribute:: Protoss_Nexus
    .. py:attribute:: Protoss_Observatory
    .. py:attribute:: Protoss_Photon_Cannon
    .. py:attribute:: Protoss_Pylon
    .. py:attribute:: Protoss_Robotics_Facility
    .. py:attribute:: Protoss_Robotics_Support_Bay
    .. py:attribute:: Protoss_Shield_Battery
    .. py:attribute:: Protoss_Stargate
    .. py:attribute:: Protoss_Templar_Archives
    .. py:attribute:: Special_Khaydarin_Crystal_Form
    .. py:attribute:: Special_Protoss_Temple
    .. py:attribute:: Special_Stasis_Cell_Prison
    .. py:attribute:: Special_Warp_Gate
    .. py:attribute:: Special_XelNaga_Temple
    .. py:attribute:: Zerg_Broodling
    .. py:attribute:: Zerg_Defiler
    .. py:attribute:: Zerg_Drone
    .. py:attribute:: Zerg_Egg
    .. py:attribute:: Zerg_Hydralisk
    .. py:attribute:: Zerg_Infested_Terran
    .. py:attribute:: Zerg_Larva
    .. py:attribute:: Zerg_Lurker
    .. py:attribute:: Zerg_Lurker_Egg
    .. py:attribute:: Zerg_Ultralisk
    .. py:attribute:: Zerg_Zergling
    .. py:attribute:: Zerg_Cocoon
    .. py:attribute:: Zerg_Devourer
    .. py:attribute:: Zerg_Guardian
    .. py:attribute:: Zerg_Mutalisk
    .. py:attribute:: Zerg_Overlord
    .. py:attribute:: Zerg_Queen
    .. py:attribute:: Zerg_Scourge
    .. py:attribute:: Hero_Devouring_One
    .. py:attribute:: Hero_Hunter_Killer
    .. py:attribute:: Hero_Infested_Duran
    .. py:attribute:: Hero_Infested_Kerrigan
    .. py:attribute:: Hero_Kukulza_Guardian
    .. py:attribute:: Hero_Kukulza_Mutalisk
    .. py:attribute:: Hero_Matriarch
    .. py:attribute:: Hero_Torrasque
    .. py:attribute:: Hero_Unclean_One
    .. py:attribute:: Hero_Yggdrasill
    .. py:attribute:: Zerg_Creep_Colony
    .. py:attribute:: Zerg_Defiler_Mound
    .. py:attribute:: Zerg_Evolution_Chamber
    .. py:attribute:: Zerg_Extractor
    .. py:attribute:: Zerg_Greater_Spire
    .. py:attribute:: Zerg_Hatchery
    .. py:attribute:: Zerg_Hive
    .. py:attribute:: Zerg_Hydralisk_Den
    .. py:attribute:: Zerg_Infested_Command_Center
    .. py:attribute:: Zerg_Lair
    .. py:attribute:: Zerg_Nydus_Canal
    .. py:attribute:: Zerg_Queens_Nest
    .. py:attribute:: Zerg_Spawning_Pool
    .. py:attribute:: Zerg_Spire
    .. py:attribute:: Zerg_Spore_Colony
    .. py:attribute:: Zerg_Sunken_Colony
    .. py:attribute:: Zerg_Ultralisk_Cavern
    .. py:attribute:: Special_Cerebrate
    .. py:attribute:: Special_Cerebrate_Daggoth
    .. py:attribute:: Special_Mature_Chrysalis
    .. py:attribute:: Special_Overmind
    .. py:attribute:: Special_Overmind_Cocoon
    .. py:attribute:: Special_Overmind_With_Shell
    .. py:attribute:: Critter_Bengalaas
    .. py:attribute:: Critter_Kakaru
    .. py:attribute:: Critter_Ragnasaur
    .. py:attribute:: Critter_Rhynadon
    .. py:attribute:: Critter_Scantid
    .. py:attribute:: Critter_Ursadon
    .. py:attribute:: Resource_Mineral_Field
    .. py:attribute:: Resource_Mineral_Field_Type_2
    .. py:attribute:: Resource_Mineral_Field_Type_3
    .. py:attribute:: Resource_Vespene_Geyser
    .. py:attribute:: Spell_Dark_Swarm
    .. py:attribute:: Spell_Disruption_Web
    .. py:attribute:: Spell_Scanner_Sweep
    .. py:attribute:: Special_Protoss_Beacon
    .. py:attribute:: Special_Protoss_Flag_Beacon
    .. py:attribute:: Special_Terran_Beacon
    .. py:attribute:: Special_Terran_Flag_Beacon
    .. py:attribute:: Special_Zerg_Beacon
    .. py:attribute:: Special_Zerg_Flag_Beacon
    .. py:attribute:: Powerup_Data_Disk
    .. py:attribute:: Powerup_Flag
    .. py:attribute:: Powerup_Khalis_Crystal
    .. py:attribute:: Powerup_Khaydarin_Crystal
    .. py:attribute:: Powerup_Mineral_Cluster_Type_1
    .. py:attribute:: Powerup_Mineral_Cluster_Type_2
    .. py:attribute:: Powerup_Protoss_Gas_Orb_Type_1
    .. py:attribute:: Powerup_Protoss_Gas_Orb_Type_2
    .. py:attribute:: Powerup_Psi_Emitter
    .. py:attribute:: Powerup_Terran_Gas_Tank_Type_1
    .. py:attribute:: Powerup_Terran_Gas_Tank_Type_2
    .. py:attribute:: Powerup_Uraj_Crystal
    .. py:attribute:: Powerup_Young_Chrysalis
    .. py:attribute:: Powerup_Zerg_Gas_Sac_Type_1
    .. py:attribute:: Powerup_Zerg_Gas_Sac_Type_2
    .. py:attribute:: Special_Floor_Gun_Trap
    .. py:attribute:: Special_Floor_Missile_Trap
    .. py:attribute:: Special_Right_Wall_Flame_Trap
    .. py:attribute:: Special_Right_Wall_Missile_Trap
    .. py:attribute:: Special_Wall_Flame_Trap
    .. py:attribute:: Special_Wall_Missile_Trap
    .. py:attribute:: Special_Pit_Door
    .. py:attribute:: Special_Right_Pit_Door
    .. py:attribute:: Special_Right_Upper_Level_Door
    .. py:attribute:: Special_Upper_Level_Door
    .. py:attribute:: Special_Cargo_Ship
    .. py:attribute:: Special_Floor_Hatch
    .. py:attribute:: Special_Independant_Starport
    .. py:attribute:: Special_Map_Revealer
    .. py:attribute:: Special_Mercenary_Gunship
    .. py:attribute:: Special_Start_Location
    .. py:attribute:: None
    .. py:attribute:: AllUnits
    .. py:attribute:: Men
    .. py:attribute:: Buildings
    .. py:attribute:: Factories
    .. py:attribute:: Unknown
