Game
====

Class
-----

.. py:class:: pybrood.Game

    .. py:method:: getForces() -> Forceset

    .. py:method:: getPlayers() -> Playerset

    .. py:method:: getAllUnits() -> Unitset

    .. py:method:: getMinerals() -> Unitset

    .. py:method:: getGeysers() -> Unitset

    .. py:method:: getNeutralUnits() -> Unitset

    .. py:method:: getStaticMinerals() -> Unitset

    .. py:method:: getStaticGeysers() -> Unitset

    .. py:method:: getStaticNeutralUnits() -> Unitset

    .. py:method:: getBullets() -> Bulletset

    .. py:method:: getNukeDots() -> list

    .. py:method:: getForce(forceID: int) -> Force

    .. py:method:: getPlayer(playerID: int) -> Player

    .. py:method:: getUnit(unitID: int) -> Unit

    .. py:method:: indexToUnit(unitIndex: int) -> Unit

    .. py:method:: getRegion(regionID: int) -> Region

    .. py:method:: getGameType() -> GameType

    .. py:method:: getLatency() -> int

    .. py:method:: getFrameCount() -> int

    .. py:method:: getReplayFrameCount() -> int

    .. py:method:: getFPS() -> int

    .. py:method:: getAverageFPS() -> float

    .. py:method:: getMousePosition() -> Tuple[int, int]

    .. py:method:: getMouseState(button: MouseButton) -> bool

    .. py:method:: getKeyState(key: Key) -> bool

    .. py:method:: getScreenPosition() -> Tuple[int, int]

    .. py:method:: setScreenPosition(x: int, y: int)

    .. py:method:: setScreenPosition(p: Tuple[int, int])

    .. py:method:: pingMinimap(x: int, y: int)

    .. py:method:: pingMinimap(p: Tuple[int, int])

    .. py:method:: isFlagEnabled(flag: int) -> bool

    .. py:method:: enableFlag(flag: int)

    .. py:method:: getUnitsOnTile(tileX: int, tileY: int) -> Unitset

    .. py:method:: getUnitsOnTile(tile: Tuple[int, int]) -> Unitset

    .. py:method:: getUnitsInRectangle(left: int, top: int, right: int, bottom: int) -> Unitset

    .. py:method:: getUnitsInRectangle(topLeft: Tuple[int, int], bottomRight: Tuple[int, int]) -> Unitset

    .. py:method:: getUnitsInRadius(x: int, y: int, radius: int) -> Unitset

    .. py:method:: getUnitsInRadius(center: Tuple[int, int], radius: int) -> Unitset

    .. py:method:: getClosestUnit(center: Tuple[int, int], radius: int=999999) -> Unit

    .. py:method:: getClosestUnitInRectangle(center: Tuple[int, int], left: int=0, top: int=0, right: int=999999, bottom: int=999999) -> Unit

    .. py:method:: getLastError() -> Error

    .. py:method:: setLastError(e: Error=Errors.None) -> bool

    .. py:method:: mapWidth() -> int

    .. py:method:: mapHeight() -> int

    .. py:method:: mapFileName() -> str

    .. py:method:: mapPathName() -> str

    .. py:method:: mapName() -> str

    .. py:method:: mapHash() -> str

    .. py:method:: isWalkable(walkX: int, walkY: int) -> bool

    .. py:method:: isWalkable(position: Tuple[int, int]) -> bool

    .. py:method:: getGroundHeight(tileX: int, tileY: int) -> int

    .. py:method:: getGroundHeight(position: Tuple[int, int]) -> int

    .. py:method:: isBuildable(tileX: int, tileY: int, includeBuildings: bool=False) -> bool

    .. py:method:: isBuildable(position: Tuple[int, int], includeBuildings: bool=False) -> bool

    .. py:method:: isVisible(tileX: int, tileY: int) -> bool

    .. py:method:: isVisible(position: Tuple[int, int]) -> bool

    .. py:method:: isExplored(tileX: int, tileY: int) -> bool

    .. py:method:: isExplored(position: Tuple[int, int]) -> bool

    .. py:method:: hasCreep(tileX: int, tileY: int) -> bool

    .. py:method:: hasCreep(position: Tuple[int, int]) -> bool

    .. py:method:: hasPowerPrecise(x: int, y: int, unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: hasPowerPrecise(position: Tuple[int, int], unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: hasPower(tileX: int, tileY: int, unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: hasPower(position: Tuple[int, int], unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: hasPower(tileX: int, tileY: int, tileWidth: int, tileHeight: int, unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: hasPower(position: Tuple[int, int], tileWidth: int, tileHeight: int, unitType: UnitType=UnitTypes.None) -> bool

    .. py:method:: canBuildHere(position: Tuple[int, int], type: UnitType, builder: Unit=None, checkExplored: bool=False) -> bool

    .. py:method:: canMake(type: UnitType, builder: Unit=None) -> bool

    .. py:method:: canResearch(type: TechType, unit: Unit=None, checkCanIssueCommandType: bool=True) -> bool

    .. py:method:: canUpgrade(type: UpgradeType, unit: Unit=None, checkCanIssueCommandType: bool=True) -> bool

    .. py:method:: getStartLocations() -> list

    .. py:method:: print(line: str)

    .. py:method:: sendText(line: str)

    .. py:method:: sendTextEx(toAllies: bool, line: str)

    .. py:method:: isInGame() -> bool

    .. py:method:: isMultiplayer() -> bool

    .. py:method:: isBattleNet() -> bool

    .. py:method:: isPaused() -> bool

    .. py:method:: isReplay() -> bool

    .. py:method:: pauseGame()

    .. py:method:: resumeGame()

    .. py:method:: leaveGame()

    .. py:method:: restartGame()

    .. py:method:: setLocalSpeed(speed: int)

    .. py:method:: getSelectedUnits() -> Unitset

    .. py:method:: self() -> Player

    .. py:method:: enemy() -> Player

    .. py:method:: neutral() -> Player

    .. py:method:: allies() -> Playerset

    .. py:method:: enemies() -> Playerset

    .. py:method:: observers() -> Playerset

    .. py:method:: setTextSize(size: TextSize=TextSize.Default)

    .. py:method:: drawText(ctype: CoordinateType, x: int, y: int, line: str)

    .. py:method:: drawTextMap(x: int, y: int, line: str)

    .. py:method:: drawTextMap(p: Tuple[int, int], line: str)

    .. py:method:: drawTextMouse(x: int, y: int, line: str)

    .. py:method:: drawTextMouse(p: Tuple[int, int], line: str)

    .. py:method:: drawTextScreen(x: int, y: int, line: str)

    .. py:method:: drawTextScreen(p: Tuple[int, int], line: str)

    .. py:method:: drawBox(ctype: CoordinateType, left: int, top: int, right: int, bottom: int, color: Color, isSolid: bool=False)

    .. py:method:: drawBoxMap(left: int, top: int, right: int, bottom: int, color: Color, isSolid: bool=False)

    .. py:method:: drawBoxMap(leftTop: Tuple[int, int], rightBottom: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawBoxMouse(left: int, top: int, right: int, bottom: int, color: Color, isSolid: bool=False)

    .. py:method:: drawBoxMouse(leftTop: Tuple[int, int], rightBottom: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawBoxScreen(left: int, top: int, right: int, bottom: int, color: Color, isSolid: bool=False)

    .. py:method:: drawBoxScreen(leftTop: Tuple[int, int], rightBottom: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawTriangle(ctype: CoordinateType, ax: int, ay: int, bx: int, by: int, cx: int, cy: int, color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleMap(ax: int, ay: int, bx: int, by: int, cx: int, cy: int, color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleMap(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleMouse(ax: int, ay: int, bx: int, by: int, cx: int, cy: int, color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleMouse(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleScreen(ax: int, ay: int, bx: int, by: int, cx: int, cy: int, color: Color, isSolid: bool=False)

    .. py:method:: drawTriangleScreen(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int], color: Color, isSolid: bool=False)

    .. py:method:: drawCircle(ctype: CoordinateType, x: int, y: int, radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleMap(x: int, y: int, radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleMap(p: Tuple[int, int], radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleMouse(x: int, y: int, radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleMouse(p: Tuple[int, int], radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleScreen(x: int, y: int, radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawCircleScreen(p: Tuple[int, int], radius: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipse(ctype: CoordinateType, x: int, y: int, xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseMap(x: int, y: int, xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseMap(p: Tuple[int, int], xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseMouse(x: int, y: int, xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseMouse(p: Tuple[int, int], xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseScreen(x: int, y: int, xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawEllipseScreen(p: Tuple[int, int], xrad: int, yrad: int, color: Color, isSolid: bool=False)

    .. py:method:: drawDot(ctype: CoordinateType, x: int, y: int, color: Color)

    .. py:method:: drawDotMap(x: int, y: int, color: Color)

    .. py:method:: drawDotMap(p: Tuple[int, int], color: Color)

    .. py:method:: drawDotMouse(x: int, y: int, color: Color)

    .. py:method:: drawDotMouse(p: Tuple[int, int], color: Color)

    .. py:method:: drawDotScreen(x: int, y: int, color: Color)

    .. py:method:: drawDotScreen(p: Tuple[int, int], color: Color)

    .. py:method:: drawLine(ctype: CoordinateType, x1: int, y1: int, x2: int, y2: int, color: Color)

    .. py:method:: drawLineMap(x1: int, y1: int, x2: int, y2: int, color: Color)

    .. py:method:: drawLineMap(a: Tuple[int, int], b: Tuple[int, int], color: Color)

    .. py:method:: drawLineMouse(x1: int, y1: int, x2: int, y2: int, color: Color)

    .. py:method:: drawLineMouse(a: Tuple[int, int], b: Tuple[int, int], color: Color)

    .. py:method:: drawLineScreen(x1: int, y1: int, x2: int, y2: int, color: Color)

    .. py:method:: drawLineScreen(a: Tuple[int, int], b: Tuple[int, int], color: Color)

    .. py:method:: getLatencyFrames() -> int

    .. py:method:: getLatencyTime() -> int

    .. py:method:: getRemainingLatencyFrames() -> int

    .. py:method:: getRemainingLatencyTime() -> int

    .. py:method:: getRevision() -> int

    .. py:method:: isDebug() -> bool

    .. py:method:: isLatComEnabled() -> bool

    .. py:method:: setLatCom(isEnabled: bool)

    .. py:method:: isGUIEnabled() -> bool

    .. py:method:: setGUI(enabled: bool)

    .. py:method:: getInstanceNumber() -> int

    .. py:method:: getAPM(includeSelects: bool=False) -> int

    .. py:method:: setMap(mapFileName: str) -> bool

    .. py:method:: setMap(mapFileName: str) -> bool

    .. py:method:: setFrameSkip(frameSkip: int)

    .. py:method:: hasPath(source: Tuple[int, int], destination: Tuple[int, int]) -> bool

    .. py:method:: setAlliance(player: Player, allied: bool=True, alliedVictory: bool=True) -> bool

    .. py:method:: setVision(player: Player, enabled: bool=True) -> bool

    .. py:method:: elapsedTime() -> int

    .. py:method:: setCommandOptimizationLevel(level: int)

    .. py:method:: countdownTimer() -> int

    .. py:method:: getAllRegions() -> Regionset

    .. py:method:: getRegionAt(x: int, y: int) -> Region

    .. py:method:: getRegionAt(position: Tuple[int, int]) -> Region

    .. py:method:: getLastEventTime() -> int

    .. py:method:: setRevealAll(reveal: bool=True) -> bool

    .. py:method:: getBuildLocation(type: UnitType, desiredPosition: Tuple[int, int], maxRange: int=64, creep: bool=False) -> Tuple[int, int]

    .. py:method:: getDamageFrom(fromType: UnitType, toType: UnitType, fromPlayer: Player=None, toPlayer: Player=None) -> int

    .. py:method:: getDamageTo(toType: UnitType, fromType: UnitType, toPlayer: Player=None, fromPlayer: Player=None) -> int


