py::module m_Game = m.def_submodule("game");


m_Game.def("allies", []() -> py::set {
    return PyBinding::set_converter<PyBinding::PlayerWeakref, BWAPI::Playerset>(BWAPI::Broodwar->allies());
});
// virtual bool 	canBuildHere (TilePosition position, UnitType type, Unit builder=nullptr, bool checkExplored=false)=0
// virtual bool 	canMake (UnitType type, Unit builder=nullptr) const =0
// virtual bool 	canResearch (TechType type, Unit unit=nullptr, bool checkCanIssueCommandType=true)=0
// virtual bool 	canUpgrade (UpgradeType type, Unit unit=nullptr, bool checkCanIssueCommandType=true)=0
m_Game.def("countdown_timer", []() -> int {
    return BWAPI::Broodwar->countdownTimer();
});
m_Game.def("elapsed_time", []() -> int {
    return BWAPI::Broodwar->elapsedTime();
});
m_Game.def("enable_flag", [](int flag){
    BWAPI::Broodwar->enableFlag(flag);
});
m_Game.def("enemies", []() -> py::set {
    return PyBinding::set_converter<PyBinding::PlayerWeakref, BWAPI::Playerset>(BWAPI::Broodwar->enemies());
});
m_Game.def("enemy", []() -> PyBinding::PlayerWeakref {
    return PyBinding::PlayerWeakref(BWAPI::Broodwar->enemy());
});
// virtual const Regionset & 	getAllRegions () const =0
// virtual const Unitset & 	getAllUnits () const =0
// virtual int 	getAPM (bool includeSelects=false) const =0
m_Game.def("get_average_FPS", []() -> double {
    return BWAPI::Broodwar->getAverageFPS();
});
// virtual Unit 	getBestUnit (const BestUnitFilter &best, const UnitFilter &pred, Position center=Positions::Origin, int radius=999999) const =0
// TilePosition 	getBuildLocation (UnitType type, TilePosition desiredPosition, int maxRange=64, bool creep=false) const
// virtual const Bulletset & 	getBullets () const =0
// Unit 	getClosestUnit (Position center, const UnitFilter &pred=nullptr, int radius=999999) const
// virtual Unit 	getClosestUnitInRectangle (Position center, const UnitFilter &pred=nullptr, int left=0, int top=0, int right=999999, int bottom=999999) const =0
// int 	getDamageFrom (UnitType fromType, UnitType toType, Player fromPlayer=nullptr, Player toPlayer=nullptr) const
// int 	getDamageTo (UnitType toType, UnitType fromType, Player toPlayer=nullptr, Player fromPlayer=nullptr) const
// virtual const std::list< Event > & 	getEvents () const =0
m_Game.def("get_force", [](int forceID) -> PyBinding::ForceWeakref {
    return PyBinding::ForceWeakref(BWAPI::Broodwar->getForce(forceID));
});
m_Game.def("get_forces", []() -> py::set {
    return PyBinding::set_converter<PyBinding::ForceWeakref, BWAPI::Forceset>(BWAPI::Broodwar->getForces());
});
m_Game.def("get_FPS", []() -> int {
    return BWAPI::Broodwar->getFPS();
});
m_Game.def("get_frame_count", []() -> int {
    return BWAPI::Broodwar->getFrameCount();
});
// virtual GameType 	getGameType () const =0
// virtual const Unitset & 	getGeysers () const =0
// virtual int 	getGroundHeight (int tileX, int tileY) const =0
// int 	getGroundHeight (TilePosition position) const
// virtual int 	getInstanceNumber () const =0
// virtual bool 	getKeyState (Key key) const =0
// virtual Error 	getLastError () const =0
m_Game.def("get_last_event_time", []() -> int {
    return BWAPI::Broodwar->getLastEventTime();
});
m_Game.def("get_latency", []() -> int {
    return BWAPI::Broodwar->getLatency();
});
m_Game.def("get_latency_frames", []() -> int {
    return BWAPI::Broodwar->getLatencyFrames();
});
m_Game.def("get_latency_time", []() -> int {
    return BWAPI::Broodwar->getLatencyTime();
});
// virtual const Unitset & 	getMinerals () const =0
// virtual Position 	getMousePosition () const =0
// virtual bool 	getMouseState (MouseButton button) const =0
// virtual const Unitset & 	getNeutralUnits () const =0
// virtual const Position::list & 	getNukeDots () const =0
// virtual Player 	getPlayer (int playerID) const =0
// virtual const Playerset & 	getPlayers () const =0
// virtual Region 	getRegion (int regionID) const =0
// virtual BWAPI::Region 	getRegionAt (int x, int y) const =0
// BWAPI::Region 	getRegionAt (BWAPI::Position position) const
m_Game.def("get_remaining_latency_frames", []() -> int {
    return BWAPI::Broodwar->getRemainingLatencyFrames();
});
m_Game.def("get_remaining_latency_time", []() -> int {
    return BWAPI::Broodwar->getRemainingLatencyTime();
});
m_Game.def("get_replay_frame_count", []() -> int {
    return BWAPI::Broodwar->getReplayFrameCount();
});
m_Game.def("get_revision", []() -> int {
    return BWAPI::Broodwar->getRevision();
});
// virtual BWAPI::Position 	getScreenPosition () const =0
// virtual const Unitset & 	getSelectedUnits () const =0
// virtual const TilePosition::list & 	getStartLocations () const =0
// virtual const Unitset & 	getStaticGeysers () const =0
// virtual const Unitset & 	getStaticMinerals () const =0
// virtual const Unitset & 	getStaticNeutralUnits () const =0
// virtual Unit 	getUnit (int unitID) const =0
// Unitset 	getUnitsInRadius (int x, int y, int radius, const UnitFilter &pred=nullptr) const
// Unitset 	getUnitsInRadius (BWAPI::Position center, int radius, const UnitFilter &pred=nullptr) const
// virtual Unitset 	getUnitsInRectangle (int left, int top, int right, int bottom, const UnitFilter &pred=nullptr) const =0
// Unitset 	getUnitsInRectangle (BWAPI::Position topLeft, BWAPI::Position bottomRight, const UnitFilter &pred=nullptr) const
// Unitset 	getUnitsOnTile (int tileX, int tileY, const UnitFilter &pred=nullptr) const
// Unitset 	getUnitsOnTile (BWAPI::TilePosition tile, const UnitFilter &pred=nullptr) const
m_Game.def("has_creep", [](int tileX, int tileY) -> bool {
    return BWAPI::Broodwar->hasCreep(tileX, tileY);
});
// bool 	hasCreep (TilePosition position) const
// bool 	hasPath (Position source, Position destination) const
// bool 	hasPower (int tileX, int tileY, UnitType unitType=UnitTypes::None) const
// bool 	hasPower (TilePosition position, UnitType unitType=UnitTypes::None) const
// bool 	hasPower (int tileX, int tileY, int tileWidth, int tileHeight, UnitType unitType=UnitTypes::None) const
// bool 	hasPower (TilePosition position, int tileWidth, int tileHeight, UnitType unitType=UnitTypes::None) const
// virtual bool 	hasPowerPrecise (int x, int y, UnitType unitType=UnitTypes::None) const =0
// bool 	hasPowerPrecise (Position position, UnitType unitType=UnitTypes::None) const
// virtual Unit 	indexToUnit (int unitIndex) const =0
m_Game.def("is_battle_net", []() -> bool {
    return BWAPI::Broodwar->isBattleNet();
});
// virtual bool 	isBuildable (int tileX, int tileY, bool includeBuildings=false) const =0
// bool 	isBuildable (TilePosition position, bool includeBuildings=false) const
m_Game.def("is_debug", []() -> bool {
    return BWAPI::Broodwar->isDebug();
});
m_Game.def("is_explored", [](int tileX, int tileY) -> bool {
    return BWAPI::Broodwar->isExplored(tileX, tileY);
});
// bool 	isExplored (TilePosition position) const
m_Game.def("is_flag_enabled", [](int flag) -> bool {
    return BWAPI::Broodwar->isFlagEnabled(flag);
});
m_Game.def("is_GUI_enabled", []() -> bool {
    return BWAPI::Broodwar->isGUIEnabled();
});
m_Game.def("is_in_game", []() -> bool {
    return BWAPI::Broodwar->isInGame();
});
m_Game.def("is_lat_com_enabled", []() -> bool {
    return BWAPI::Broodwar->isLatComEnabled();
});
m_Game.def("is_multiplayer", []() -> bool {
    return BWAPI::Broodwar->isMultiplayer();
});
m_Game.def("is_paused", []() -> bool {
    return BWAPI::Broodwar->isPaused();
});
m_Game.def("is_replay", []() -> bool {
    return BWAPI::Broodwar->isReplay();
});
// virtual bool 	issueCommand (const Unitset &units, UnitCommand command)=0
m_Game.def("is_visible", [](int tileX, int tileY) -> bool {
    return BWAPI::Broodwar->isVisible(tileX, tileY);
});
// bool 	isVisible (TilePosition position) const
m_Game.def("is_walkable", [](int walkX, int walkY) -> bool {
    return BWAPI::Broodwar->isWalkable(walkX, walkY);
});
// bool 	isWalkable (BWAPI::WalkPosition position) const
m_Game.def("leave_game", [](){
    BWAPI::Broodwar->leaveGame();
});
m_Game.def("map_file_name", []() -> std::string {
    return BWAPI::Broodwar->mapFileName();
});
m_Game.def("map_hash", []() -> std::string {
    return BWAPI::Broodwar->mapHash();
});
m_Game.def("map_height", []() -> int {
    return BWAPI::Broodwar->mapHeight();
});
m_Game.def("map_name", []() -> std::string {
    return BWAPI::Broodwar->mapName();
});
m_Game.def("map_path_name", []() -> std::string {
    return BWAPI::Broodwar->mapPathName();
});
m_Game.def("map_width", []() -> int {
    return BWAPI::Broodwar->mapWidth();
});
// virtual Player 	neutral () const =0
// virtual Playerset & 	observers ()=0
m_Game.def("pause_game", [](){
    BWAPI::Broodwar->pauseGame();
});
m_Game.def("ping_minimap", [](int x, int y){
    BWAPI::Broodwar->pingMinimap(x, y);
});
// void 	pingMinimap (BWAPI::Position p)
// void 	printf (const char *format,...)
m_Game.def("restart_game", [](){
    BWAPI::Broodwar->restartGame();
});
m_Game.def("resume_game", [](){
    BWAPI::Broodwar->resumeGame();
});
// virtual Player 	self () const =0
// void 	sendText (const char *format,...)
// void 	sendTextEx (bool toAllies, const char *format,...)
// virtual bool 	setAlliance (BWAPI::Player player, bool allied=true, bool alliedVictory=true)=0
// virtual void 	setCommandOptimizationLevel (int level)=0
m_Game.def("set_frame_skip", [](int frameSkip){
    BWAPI::Broodwar->setFrameSkip(frameSkip);
});
m_Game.def("set_GUI", [](bool enabled){
    BWAPI::Broodwar->setGUI(enabled);
});
// virtual bool 	setLastError (BWAPI::Error e=Errors::None) const =0
m_Game.def("set_lat_com", [](bool isEnabled){
    BWAPI::Broodwar->setLatCom(isEnabled);
});
m_Game.def("set_local_speed", [](int speed){
    BWAPI::Broodwar->setLocalSpeed(speed);
});
// virtual bool 	setMap (const char *mapFileName)=0
// bool 	setMap (const std::string &mapFileName)
// virtual bool 	setRevealAll (bool reveal=true)=0
// virtual void 	setScreenPosition (int x, int y)=0
// void 	setScreenPosition (BWAPI::Position p)
// virtual bool 	setVision (BWAPI::Player player, bool enabled=true)=0
// virtual void 	vPrintf (const char *format, va_list args)=0
// void 	vSendText (const char *format, va_list args)
// virtual void 	vSendTextEx (bool toAllies, const char *format, va_list args)=0
