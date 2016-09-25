Binding made as from-scratch code generator, outputting msvc project.
Although starcraft runs perfectly under wine, I couldn't run it with BWAPI injector.
So I decided to run SC in VirtualBox.

## building

`python3.5 -m generator`

Then run `build.bat` inside `output` folder.

## developer notes

Standard pybind11 method handling:

```
.def("isResourceDepot", &BWAPI::UnitType::isResourceDepot)
```

First problem, overloaded methods:

```
.def("canUseTechPosition", &BWAPI::Unit::canUseTechPosition)
.def("canUseTechPosition", &BWAPI::Unit::canUseTechPosition)
```

Solution:

```
.def("canUseTechPosition", (bool (BWAPI::Unit::*)(BWAPI::TechType, bool, bool)) &BWAPI::Unit::canUseTechPosition)
.def("canUseTechPosition", (bool (BWAPI::Unit::*)(BWAPI::TechType, Position, bool, bool, bool)) &BWAPI::Unit::canUseTechPosition)
```

Second problem, some types are actually pointers to classes:

```
typedef RegionInterface *Region;
```

Solution: create proxy classes


Some classes require wrapping, because pybind11 requires possibility to destruct object.
This is impossible for entities like `Force`, `Player`, `Bullet`, etc.
E.g. `BWAPI::Force` is getting wrapped into `PyBinding::Wrapper::Force`.
This requires type replacement in any function using `Force` type.
To solve this there's a `typereplacer.py`.

Some classes require no transformation though.

Without wrapping the usage is trivial for pybind11:
```
BWAPI::PlayerType
    bool isLobbyType() const;
→
output/pybind/playertype.cpp
    class_playertype.def_property_readonly("is_lobby_type",  &BWAPI::PlayerType::isLobbyType);
```

With wrapping here's the intermediate class:
```
BWAPI::Bullet
    virtual Unit getSource() const = 0;
→
output/include/bullet.h
    BWAPI::Unit getSource();
output/pybind/bullet.cpp
    class_bullet.def_property_readonly("source", [](PyBinding::Wrapper::Bullet& obj) -> PyBinding::Wrapper::Unit {
        return PyBinding::Wrapper::Unit(obj.getSource());
    });
output/src/bullet.cpp
    BWAPI::Unit Bullet::getSource(){
        return obj->getSource();
    }
```

```
BWAPI::Unitset
    bool gather(Unit target, bool shiftQueueCommand = false) const;
→
output/pybind/unitset.cpp
    class_unitset.def("gather", [](BWAPI::Unitset& obj, PyBinding::Wrapper::Unit target, bool shiftQueueCommand = false) -> bool {
        return obj.gather(target.obj, shiftQueueCommand);
    });
```

Wrapper class just keeps reference to an object `obj` and allows free destruction
by pybind11 without affecting internals of BWAPI. `output/include/` and `output/src/` are folders
for these "as is" wrappers. All type transformations, including instantiation of wrappers happens
in lambda functions in `output/pybind/`. You can see how `BWAPI::Unit` becomes `PyBinding::Wrapper::Unit`
and how methods of wrapper are getting called.

## todo

Unitset не стоит сразу конвертировать в py::set, у него есть родные методы (в том числе конструкторы)
Forceset ..
Playerset ..
Regionset ..

обёртки нужны, так как pybind требует деструктор класса

добавляются ли динамически создаваемые классы в __subclasses__?

нужно передавать как reference не врапаные константные типы (UnitType например, наследники Type), чтобы
pybind не пытался их удалить.
хотя.. по идее пайбинд их скопирует. с другой стороны внутри тайпа нет никакого стейта кроме int id.

TODO: implement __all__ for:
BulletType
DamageType
Error
ExplosionType
GameType
Order
PlayerType
Race
TechType
UnitCommandType
UnitSizeType
UnitType
UpgradeType
WeaponType

```
+ AIModule.h
+ ArithmaticFilter.h
BestFilter.h
+ Bullet.h
Bulletset.h
  set methods ? (empty)
+ BulletType.h
Client.h
+ Color.h
  Color is the one of few types open for construction from python side.
ComparisonFilter.h
+ Constants.h
  only TILE_SIZE constant, она нигде не используется
+ CoordinateType.h
+ DamageType.h
+ Error.h
Event.h
+ EventType.h
+ ExplosionType.h
Filters.h
+ Flag.h
+ Force.h
Forceset.h
  set methods
Game.h
+ GameType.h
+ Input.h
+ Interface.h
  есть возможность вешать эвенты на сущности, но это по сути уже частичная
  имплементация самого AI алгоритма. и работает оно тупо проверяя указанный
  колбэк с определённой периодичностью.
  явно не то, ради чего стоит усложнять биндинг
+ InterfaceEvent.h
+ Latency.h
+ Order.h
+ Player.h
Playerset.h
  set methods
+ PlayerType.h
+ Position.h
  условно выполнено. отброшена вся векторная логика, позиции выдаются без
  различия в скейле. предполагается считать на стороне питона, так как
  транслировать простейшие операции через барьер биндинга очень медленно.
PositionUnit.h
+ Race.h
+ Region.h
Regionset.h
  set methods
+ SetContainer.h
+ TechType.h
+ TournamentAction.h
+ Type.h
UnaryFilter.h
+ Unit.h
UnitCommand.h
+ UnitCommandType.h
Unitset.h
  set methods
+ UnitSizeType.h
UnitType.h
  constants from line 905
  static methods from line 926 (including __all__)
+ UpgradeType.h
WeaponType.h
  static methods from line 311 (including __all__)
+ WindowsTypes.h
```
