#ifndef MODCODE

class PlayerWeakref
{
protected:
    BWAPI::Player obj;
public:
    PlayerWeakref(BWAPI::Player iobj) : obj(iobj){};
    int getID(){ return obj->getID(); };
    std::string getName(){ return obj->getName(); };
    // virtual const Unitset &getUnits() const = 0;
    // virtual Race getRace() const = 0;
    // virtual PlayerType getType() const = 0;
    ForceWeakref getForce(){ return ForceWeakref(obj->getForce()); };
    bool isAlly(const PlayerWeakref player){
        return obj->isAlly(player.obj);
    }
    bool isEnemy(const PlayerWeakref player){
        return obj->isEnemy(player.obj);
    }
    bool isNeutral(){ return obj->isNeutral(); };
    // virtual TilePosition getStartLocation() const = 0;
    bool isVictorious(){ return obj->isVictorious(); };
    bool isDefeated(){ return obj->isDefeated(); };
    bool leftGame(){ return obj->leftGame(); };
    int minerals(){ return obj->minerals(); };
    int gas(){ return obj->gas(); };
    int gatheredMinerals(){ return obj->gatheredMinerals(); };
    int gatheredGas(){ return obj->gatheredGas(); };
    int repairedMinerals(){ return obj->repairedMinerals(); };
    int repairedGas(){ return obj->repairedGas(); };
    int refundedMinerals(){ return obj->refundedMinerals(); };
    int refundedGas(){ return obj->refundedGas(); };
    int spentMinerals(){ return obj->spentMinerals(); };
    int spentGas(){ return obj->spentGas(); };
    // int supplyTotal(Race race = Races::None) const = 0;
    // int supplyUsed(Race race = Races::None) const = 0;
    // int allUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
    // int visibleUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
    // int completedUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
    // int incompleteUnitCount(UnitType unit = UnitTypes::AllUnits) const;
    // virtual int deadUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
    // virtual int killedUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
    // virtual int getUpgradeLevel(UpgradeType upgrade) const = 0;
    // virtual bool hasResearched(TechType tech) const = 0;
    // virtual bool isResearching(TechType tech) const = 0;
    // virtual bool isUpgrading(UpgradeType upgrade) const = 0;
    // virtual BWAPI::Color getColor() const = 0;
    // char getTextColor() const;
    // int maxEnergy(UnitType unit) const;
    // double topSpeed(UnitType unit) const;
    // int weaponMaxRange(WeaponType weapon) const;
    // int sightRange(UnitType unit) const;
    // int weaponDamageCooldown(UnitType unit) const;
    // int armor(UnitType unit) const;
    // int damage(WeaponType wpn) const;
    int getUnitScore(){ return obj->getUnitScore(); };
    int getKillScore(){ return obj->getKillScore(); };
    int getBuildingScore(){ return obj->getBuildingScore(); };
    int getRazingScore(){ return obj->getRazingScore(); };
    int getCustomScore(){ return obj->getCustomScore(); };
    bool isObserver(){ return obj->isObserver(); };
    // virtual int getMaxUpgradeLevel(UpgradeType upgrade) const = 0;
    // virtual bool isResearchAvailable(TechType tech) const = 0;
    // virtual bool isUnitAvailable(UnitType unit) const = 0;
    // bool hasUnitTypeRequirement(UnitType unit, int amount = 1) const;
};

#else

py::class_<PyBinding::PlayerWeakref> player(m, "Player");
player.def("__init__", [](PyBinding::PlayerWeakref){
    throw std::runtime_error("Player objects can't be instantiated from python side");
});
player.def_property_readonly("id", &PyBinding::PlayerWeakref::getID);
player.def_property_readonly("name", &PyBinding::PlayerWeakref::getName);
// virtual const Unitset &getUnits() const = 0;
// virtual Race getRace() const = 0;
// virtual PlayerType getType() const = 0;
player.def_property_readonly("force", &PyBinding::PlayerWeakref::getForce);
player.def("is_ally", &PyBinding::PlayerWeakref::isAlly);
player.def("is_enemy", &PyBinding::PlayerWeakref::isAlly);
player.def_property_readonly("neutral", &PyBinding::PlayerWeakref::isNeutral);
// virtual TilePosition getStartLocation() const = 0;
player.def_property_readonly("victorious", &PyBinding::PlayerWeakref::isVictorious);
player.def_property_readonly("defeated", &PyBinding::PlayerWeakref::isDefeated);
player.def_property_readonly("left_game", &PyBinding::PlayerWeakref::leftGame);
player.def_property_readonly("minerals", &PyBinding::PlayerWeakref::minerals);
player.def_property_readonly("gas", &PyBinding::PlayerWeakref::gas);
player.def_property_readonly("gathered_minerals", &PyBinding::PlayerWeakref::gatheredMinerals);
player.def_property_readonly("gathered_gas", &PyBinding::PlayerWeakref::gatheredGas);
player.def_property_readonly("repaired_minerals", &PyBinding::PlayerWeakref::repairedMinerals);
player.def_property_readonly("repaired_gas", &PyBinding::PlayerWeakref::repairedGas);
player.def_property_readonly("refunded_minerals", &PyBinding::PlayerWeakref::refundedMinerals);
player.def_property_readonly("refunded_gas", &PyBinding::PlayerWeakref::refundedGas);
player.def_property_readonly("spent_minerals", &PyBinding::PlayerWeakref::spentMinerals);
player.def_property_readonly("spent_gas", &PyBinding::PlayerWeakref::spentGas);
// int supplyTotal(Race race = Races::None) const = 0;
// int supplyUsed(Race race = Races::None) const = 0;
// int allUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
// int visibleUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
// int completedUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
// int incompleteUnitCount(UnitType unit = UnitTypes::AllUnits) const;
// virtual int deadUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
// virtual int killedUnitCount(UnitType unit = UnitTypes::AllUnits) const = 0;
// virtual int getUpgradeLevel(UpgradeType upgrade) const = 0;
// virtual bool hasResearched(TechType tech) const = 0;
// virtual bool isResearching(TechType tech) const = 0;
// virtual bool isUpgrading(UpgradeType upgrade) const = 0;
// virtual BWAPI::Color getColor() const = 0;
// char getTextColor() const;
// int maxEnergy(UnitType unit) const;
// double topSpeed(UnitType unit) const;
// int weaponMaxRange(WeaponType weapon) const;
// int sightRange(UnitType unit) const;
// int weaponDamageCooldown(UnitType unit) const;
// int armor(UnitType unit) const;
// int damage(WeaponType wpn) const;
player.def_property_readonly("unit_score", &PyBinding::PlayerWeakref::getUnitScore);
player.def_property_readonly("kill_score", &PyBinding::PlayerWeakref::getKillScore);
player.def_property_readonly("building_score", &PyBinding::PlayerWeakref::getBuildingScore);
player.def_property_readonly("razing_score", &PyBinding::PlayerWeakref::getRazingScore);
player.def_property_readonly("custom_score", &PyBinding::PlayerWeakref::getCustomScore);
player.def_property_readonly("observer", &PyBinding::PlayerWeakref::isObserver);
// virtual int getMaxUpgradeLevel(UpgradeType upgrade) const = 0;
// virtual bool isResearchAvailable(TechType tech) const = 0;
// virtual bool isUnitAvailable(UnitType unit) const = 0;
// bool hasUnitTypeRequirement(UnitType unit, int amount = 1) const;

#endif
