Unit
====

Class
-----

.. py:class:: pybrood.Unit

    .. py:method:: getID() -> int

    .. py:method:: exists() -> bool

    .. py:method:: getReplayID() -> int

    .. py:method:: getPlayer() -> Player

    .. py:method:: getType() -> UnitType

    .. py:method:: getPosition() -> Tuple[int, int]

    .. py:method:: getTilePosition() -> Tuple[int, int]

    .. py:method:: getAngle() -> float

    .. py:method:: getVelocityX() -> float

    .. py:method:: getVelocityY() -> float

    .. py:method:: getRegion() -> Region

    .. py:method:: getLeft() -> int

    .. py:method:: getTop() -> int

    .. py:method:: getRight() -> int

    .. py:method:: getBottom() -> int

    .. py:method:: getHitPoints() -> int

    .. py:method:: getShields() -> int

    .. py:method:: getEnergy() -> int

    .. py:method:: getResources() -> int

    .. py:method:: getResourceGroup() -> int

    .. py:method:: getDistance(target: Tuple[int, int]) -> int

    .. py:method:: getDistance(target: Unit) -> int

    .. py:method:: hasPath(target: Tuple[int, int]) -> bool

    .. py:method:: hasPath(target: Unit) -> bool

    .. py:method:: getLastCommandFrame() -> int

    .. py:method:: getLastAttackingPlayer() -> Player

    .. py:method:: getInitialType() -> UnitType

    .. py:method:: getInitialPosition() -> Tuple[int, int]

    .. py:method:: getInitialTilePosition() -> Tuple[int, int]

    .. py:method:: getInitialHitPoints() -> int

    .. py:method:: getInitialResources() -> int

    .. py:method:: getKillCount() -> int

    .. py:method:: getAcidSporeCount() -> int

    .. py:method:: getInterceptorCount() -> int

    .. py:method:: getScarabCount() -> int

    .. py:method:: getSpiderMineCount() -> int

    .. py:method:: getGroundWeaponCooldown() -> int

    .. py:method:: getAirWeaponCooldown() -> int

    .. py:method:: getSpellCooldown() -> int

    .. py:method:: getDefenseMatrixPoints() -> int

    .. py:method:: getDefenseMatrixTimer() -> int

    .. py:method:: getEnsnareTimer() -> int

    .. py:method:: getIrradiateTimer() -> int

    .. py:method:: getLockdownTimer() -> int

    .. py:method:: getMaelstromTimer() -> int

    .. py:method:: getOrderTimer() -> int

    .. py:method:: getPlagueTimer() -> int

    .. py:method:: getRemoveTimer() -> int

    .. py:method:: getStasisTimer() -> int

    .. py:method:: getStimTimer() -> int

    .. py:method:: getBuildType() -> UnitType

    .. py:method:: getTrainingQueue() -> List[UnitType]

    .. py:method:: getTech() -> TechType

    .. py:method:: getUpgrade() -> UpgradeType

    .. py:method:: getRemainingBuildTime() -> int

    .. py:method:: getRemainingTrainTime() -> int

    .. py:method:: getRemainingResearchTime() -> int

    .. py:method:: getRemainingUpgradeTime() -> int

    .. py:method:: getBuildUnit() -> Unit

    .. py:method:: getTarget() -> Unit

    .. py:method:: getTargetPosition() -> Tuple[int, int]

    .. py:method:: getOrder() -> Order

    .. py:method:: getSecondaryOrder() -> Order

    .. py:method:: getOrderTarget() -> Unit

    .. py:method:: getOrderTargetPosition() -> Tuple[int, int]

    .. py:method:: getRallyPosition() -> Tuple[int, int]

    .. py:method:: getRallyUnit() -> Unit

    .. py:method:: getAddon() -> Unit

    .. py:method:: getNydusExit() -> Unit

    .. py:method:: getPowerUp() -> Unit

    .. py:method:: getTransport() -> Unit

    .. py:method:: getLoadedUnits() -> Unitset

    .. py:method:: getSpaceRemaining() -> int

    .. py:method:: getCarrier() -> Unit

    .. py:method:: getInterceptors() -> Unitset

    .. py:method:: getHatchery() -> Unit

    .. py:method:: getLarva() -> Unitset

    .. py:method:: getUnitsInRadius(radius: int) -> Unitset

    .. py:method:: getUnitsInWeaponRange(weapon: WeaponType) -> Unitset

    .. py:method:: getClosestUnit(radius: int=999999) -> Unit

    .. py:method:: hasNuke() -> bool

    .. py:method:: isAccelerating() -> bool

    .. py:method:: isAttacking() -> bool

    .. py:method:: isAttackFrame() -> bool

    .. py:method:: isBeingConstructed() -> bool

    .. py:method:: isBeingGathered() -> bool

    .. py:method:: isBeingHealed() -> bool

    .. py:method:: isBlind() -> bool

    .. py:method:: isBraking() -> bool

    .. py:method:: isBurrowed() -> bool

    .. py:method:: isCarryingGas() -> bool

    .. py:method:: isCarryingMinerals() -> bool

    .. py:method:: isCloaked() -> bool

    .. py:method:: isCompleted() -> bool

    .. py:method:: isConstructing() -> bool

    .. py:method:: isDefenseMatrixed() -> bool

    .. py:method:: isDetected() -> bool

    .. py:method:: isEnsnared() -> bool

    .. py:method:: isFlying() -> bool

    .. py:method:: isFollowing() -> bool

    .. py:method:: isGatheringGas() -> bool

    .. py:method:: isGatheringMinerals() -> bool

    .. py:method:: isHallucination() -> bool

    .. py:method:: isHoldingPosition() -> bool

    .. py:method:: isIdle() -> bool

    .. py:method:: isInterruptible() -> bool

    .. py:method:: isInvincible() -> bool

    .. py:method:: isInWeaponRange(target: Unit) -> bool

    .. py:method:: isIrradiated() -> bool

    .. py:method:: isLifted() -> bool

    .. py:method:: isLoaded() -> bool

    .. py:method:: isLockedDown() -> bool

    .. py:method:: isMaelstrommed() -> bool

    .. py:method:: isMorphing() -> bool

    .. py:method:: isMoving() -> bool

    .. py:method:: isParasited() -> bool

    .. py:method:: isPatrolling() -> bool

    .. py:method:: isPlagued() -> bool

    .. py:method:: isRepairing() -> bool

    .. py:method:: isResearching() -> bool

    .. py:method:: isSelected() -> bool

    .. py:method:: isSieged() -> bool

    .. py:method:: isStartingAttack() -> bool

    .. py:method:: isStasised() -> bool

    .. py:method:: isStimmed() -> bool

    .. py:method:: isStuck() -> bool

    .. py:method:: isTraining() -> bool

    .. py:method:: isUnderAttack() -> bool

    .. py:method:: isUnderDarkSwarm() -> bool

    .. py:method:: isUnderDisruptionWeb() -> bool

    .. py:method:: isUnderStorm() -> bool

    .. py:method:: isPowered() -> bool

    .. py:method:: isUpgrading() -> bool

    .. py:method:: isVisible(player: Player=None) -> bool

    .. py:method:: isTargetable() -> bool

    .. py:method:: attack(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool

    .. py:method:: attack(target: Unit, shiftQueueCommand: bool=False) -> bool

    .. py:method:: build(type: UnitType, target: Tuple[int, int]=TILEPOSITION_NONE) -> bool

    .. py:method:: buildAddon(type: UnitType) -> bool

    .. py:method:: train(type: UnitType=UnitTypes.None) -> bool

    .. py:method:: morph(type: UnitType) -> bool

    .. py:method:: research(tech: TechType) -> bool

    .. py:method:: upgrade(upgrade: UpgradeType) -> bool

    .. py:method:: setRallyPoint(target: Tuple[int, int]) -> bool

    .. py:method:: setRallyPoint(target: Unit) -> bool

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

    .. py:method:: land(target: Tuple[int, int]) -> bool

    .. py:method:: load(target: Unit, shiftQueueCommand: bool=False) -> bool

    .. py:method:: unload(target: Unit) -> bool

    .. py:method:: unloadAll(shiftQueueCommand: bool=False) -> bool

    .. py:method:: unloadAll(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool

    .. py:method:: rightClick(target: Tuple[int, int], shiftQueueCommand: bool=False) -> bool

    .. py:method:: rightClick(target: Unit, shiftQueueCommand: bool=False) -> bool

    .. py:method:: haltConstruction() -> bool

    .. py:method:: cancelConstruction() -> bool

    .. py:method:: cancelAddon() -> bool

    .. py:method:: cancelTrain(slot: int=-2) -> bool

    .. py:method:: cancelMorph() -> bool

    .. py:method:: cancelResearch() -> bool

    .. py:method:: cancelUpgrade() -> bool

    .. py:method:: useTech(tech: TechType, target: Tuple[int, int]=POSITION_UNKNOWN) -> bool

    .. py:method:: useTech(tech: TechType, target: Unit=None) -> bool

    .. py:method:: placeCOP(target: Tuple[int, int]) -> bool

    .. py:method:: canCommand() -> bool

    .. py:method:: canCommandGrouped(checkCommandibility: bool=True) -> bool

    .. py:method:: canIssueCommandType(ct: UnitCommandType, checkCommandibility: bool=True) -> bool

    .. py:method:: canIssueCommandTypeGrouped(ct: UnitCommandType, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canTargetUnit(targetUnit: Unit, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttack(checkCommandibility: bool=True) -> bool

    .. py:method:: canAttack(target: Tuple[int, int], checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttack(target: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackGrouped(target: Tuple[int, int], checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackGrouped(target: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackMove(checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackMoveGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackUnit(checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackUnit(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackUnitGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canAttackUnitGrouped(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canBuild(checkCommandibility: bool=True) -> bool

    .. py:method:: canBuild(uType: UnitType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canBuild(uType: UnitType, tilePos: Tuple[int, int], checkTargetUnitType: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canBuildAddon(checkCommandibility: bool=True) -> bool

    .. py:method:: canBuildAddon(uType: UnitType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canTrain(checkCommandibility: bool=True) -> bool

    .. py:method:: canTrain(uType: UnitType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canMorph(checkCommandibility: bool=True) -> bool

    .. py:method:: canMorph(uType: UnitType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canResearch(checkCommandibility: bool=True) -> bool

    .. py:method:: canResearch(type: TechType, checkCanIssueCommandType: bool=True) -> bool

    .. py:method:: canUpgrade(checkCommandibility: bool=True) -> bool

    .. py:method:: canUpgrade(type: UpgradeType, checkCanIssueCommandType: bool=True) -> bool

    .. py:method:: canSetRallyPoint(checkCommandibility: bool=True) -> bool

    .. py:method:: canSetRallyPoint(target: Tuple[int, int], checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canSetRallyPoint(target: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canSetRallyPosition(checkCommandibility: bool=True) -> bool

    .. py:method:: canSetRallyUnit(checkCommandibility: bool=True) -> bool

    .. py:method:: canSetRallyUnit(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canMove(checkCommandibility: bool=True) -> bool

    .. py:method:: canMoveGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canPatrol(checkCommandibility: bool=True) -> bool

    .. py:method:: canPatrolGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canFollow(checkCommandibility: bool=True) -> bool

    .. py:method:: canFollow(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canGather(checkCommandibility: bool=True) -> bool

    .. py:method:: canGather(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canReturnCargo(checkCommandibility: bool=True) -> bool

    .. py:method:: canHoldPosition(checkCommandibility: bool=True) -> bool

    .. py:method:: canStop(checkCommandibility: bool=True) -> bool

    .. py:method:: canRepair(checkCommandibility: bool=True) -> bool

    .. py:method:: canRepair(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canBurrow(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnburrow(checkCommandibility: bool=True) -> bool

    .. py:method:: canCloak(checkCommandibility: bool=True) -> bool

    .. py:method:: canDecloak(checkCommandibility: bool=True) -> bool

    .. py:method:: canSiege(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnsiege(checkCommandibility: bool=True) -> bool

    .. py:method:: canLift(checkCommandibility: bool=True) -> bool

    .. py:method:: canLand(checkCommandibility: bool=True) -> bool

    .. py:method:: canLand(target: Tuple[int, int], checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canLoad(checkCommandibility: bool=True) -> bool

    .. py:method:: canLoad(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUnloadWithOrWithoutTarget(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnloadAtPosition(targDropPos: Tuple[int, int], checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUnload(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnload(targetUnit: Unit, checkCanTargetUnit: bool=True, checkPosition: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUnloadAll(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnloadAllPosition(checkCommandibility: bool=True) -> bool

    .. py:method:: canUnloadAllPosition(targDropPos: Tuple[int, int], checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClick(checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClick(target: Tuple[int, int], checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClick(target: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickGrouped(target: Tuple[int, int], checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickGrouped(target: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickPosition(checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickPositionGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickUnit(checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickUnit(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickUnitGrouped(checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canRightClickUnitGrouped(targetUnit: Unit, checkCanTargetUnit: bool=True, checkCanIssueCommandType: bool=True, checkCommandibilityGrouped: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canHaltConstruction(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelConstruction(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelAddon(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelTrain(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelTrainSlot(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelTrainSlot(slot: int, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelMorph(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelResearch(checkCommandibility: bool=True) -> bool

    .. py:method:: canCancelUpgrade(checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechWithOrWithoutTarget(checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechWithOrWithoutTarget(tech: TechType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTech(tech: TechType, target: Tuple[int, int]=POSITION_UNKNOWN, checkCanTargetUnit: bool=True, checkTargetsType: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTech(tech: TechType, target: Unit=None, checkCanTargetUnit: bool=True, checkTargetsType: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechWithoutTarget(tech: TechType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechUnit(tech: TechType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechUnit(tech: TechType, targetUnit: Unit, checkCanTargetUnit: bool=True, checkTargetsUnits: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechPosition(tech: TechType, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canUseTechPosition(tech: TechType, target: Tuple[int, int], checkTargetsPositions: bool=True, checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool

    .. py:method:: canPlaceCOP(checkCommandibility: bool=True) -> bool

    .. py:method:: canPlaceCOP(target: Tuple[int, int], checkCanIssueCommandType: bool=True, checkCommandibility: bool=True) -> bool


