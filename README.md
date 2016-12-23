Binding made as from-scratch code generator, outputting msvc project.
Although starcraft runs perfectly under wine, I couldn't run it with BWAPI injector.
So I decided to run SC in VirtualBox.

## building

`python3.5 -m generator`

Then run `build.bat` inside `output` folder.

## TODO:

- Make sets (Unitset, etc) iterable.
- Default argument value handling.
- Default argument value handling: nullptr value cases.

## Internals

`generator.parser` contains everything related to parsing of BWAPI include files.
It returns data structure sufficient to generate binding module.

There're several kinds of things to be passed between python and C++ sides:

1. Usual C++ enums.
2. Classes.
3. Primitive types and STL containers automatically handled by pybind11.

### C++ enums

Most straightforward part. Just using them exactly as pybind11 documentation says:

```
enum BWAPI::Text::Size::Enum
{
  Small,
  Default,
  Large,
  Huge
};
→
py::enum_<BWAPI::Text::Size::Enum>(m, "TextSize")
    .value("Small", BWAPI::Text::Size::Enum::Small)
    .value("Default", BWAPI::Text::Size::Enum::Default)
    .value("Large", BWAPI::Text::Size::Enum::Large)
    .value("Huge", BWAPI::Text::Size::Enum::Huge);
```

We need only set (by hand) pythonic name here: `"TextSize"`.

### Classes

Depending on:

1. Availability of class destructor in public space (
    This is required just for describing a class using `py::class_`.
    It doesn't matter even if you're going to use objects only via weakrefs
    ).
2. Whether the type is actually a pointer to a class.
3. Intended for construction from python side as usual object.
4. Class resembles set (may be with some extra methods, marked with +).
5. Class is BWAPI::Type with numeric ID and string Name (may be with some extra methods, marked with +).
    This class works like numeric enum constant, but has some attached functionality.

Possible decisions:

1. Building proxy class (for available destructor) holding pointer to actual object, behaving like weakref.
2. Possibility to construct typed set on py side and call its methods.
    ```
    # possible to create C++ side set from pure pythonic
    pset = Playerset({player1, player2})
    pset.getRaces()

    # passing sets to methods require constructed object
    # for simplicity, due to rareness of such situations
    some_bwapi_method(pset)
    # impossible: some_bwapi_method({player1, player2})

    # returned values are also C++ side objects with ability to iterate
    pset2 = another_bwapi_method()
    pset2.getRaces()
    for player in pset2:
        pass
    pythonic_set = set(pset2)

    # for simplicity other set operations are NOT implemented:
    # impossible: pset2.add(player2)
    pset2 = Playerset(set(pset2) | {player2})
    # Yes, this is slightly suboptimal, but doesn't complicate things.
    ```
3. Straightforward description of class using pybind11.
    1. Without ability to construct, enumeration of singletons available in advance.
    2. With free ability to construct.
    3. Without ability to construct, one singleton available in advance.

class | 1 | 2 | 3 | 4 | 5 | decision
--- | --- | --- | --- | --- | --- | ---
Bullet          | |Y| |  |  | 1
Bulletset       | | | |Y |  | 2
Client          | | | |  |  | 3.3
Color           | | |Y|  |Y+| 3.2
DamageType      | | | |  |Y | 3.1
Error           | | | |  |Y | 3.1
ExplosionType   | | | |  |Y | 3.1
Force           | |Y| |  |  | 1
Forceset        | | | |Y+|  | 2
Game            |N| | |  |  | 1
GameType        | | | |  |Y | 3.1
Order           | | | |  |Y | 3.1
Player          | |Y| |  |  | 1
Playerset       | | | |Y+|  | 2
PlayerType      | | | |  |Y+| 3.1
Race            | | | |  |Y+| 3.1
Region          | |Y| |  |  | 1
Regionset       | | | |Y+|  | 2
TechType        | | | |  |Y+| 3.1
Unit            | |Y| |  |  | 1
UnitCommandType | | | |  |Y | 3.1
Unitset         | | | |Y+|  | 2
UnitSizeType    | | | |  |Y | 3.1
UnitType        | | | |  |Y+| 3.1
UpgradeType     | | | |  |Y+| 3.1
WeaponType      | | | |  |Y+| 3.1

Note that handling of all type cases must also be done in return values and function/method parameters.

#### Building proxy class

There's no need to worry about lifetime of object. BWAPI returns pointers and we can freely transform them into weak references.

```
namespace Pybrood {
class Bullet
{
public:
    BWAPI::Bullet obj;  // be sure this type is pointer to object
    Bullet(BWAPI::Bullet);
    ...  // dummy methods following here
};
}
```

```
py::class_<Pybrood::Bullet>(m, "Bullet")  // note how original class replaced with proxy
    .def("getPlayer", ...)
    .def("getType", ...)
    .def("getSource", ...);
```

Dummy methods must not handle any specific type conversions. Instead, use pybind11 definitions
for this. That is the way to place special conversions uniformly: they can happen even in straightforwardly binded classes.

#### Straightforward description

Simply as pybind11 manual says:

```
py::class_<BWAPI::Race>(m, "Race")
    .def("getWorker", ...)
    .def("getCenter", ...)
    .def("getRefinery", ...)
    .def("getTransport", ...)
    .def("getSupplyProvider", ...);
```

Yet again, we need to choose pythonic name: `"Race"`.

#### Enums consisting of objects

Straightforward pybind11 classes used in conjunction with returning as weakref.

```
namespace Races
{
  extern const Race Zerg;
  extern const Race Terran;
  extern const Race Protoss;
  extern const Race Random;
  extern const Race None;
  extern const Race Unknown;
}
→
{
    auto o = py::dict();
    o["Zerg"] = py::cast(BWAPI::Races::Zerg, py::return_value_policy::reference);
    o["Terran"] = py::cast(BWAPI::Races::Terran, py::return_value_policy::reference);
    o["Protoss"] = py::cast(BWAPI::Races::Protoss, py::return_value_policy::reference);
    o["Random"] = py::cast(BWAPI::Races::Random, py::return_value_policy::reference);
    o["None"] = py::cast(BWAPI::Races::None, py::return_value_policy::reference);
    o["Unknown"] = py::cast(BWAPI::Races::Unknown, py::return_value_policy::reference);
    m.attr("Races") = o;
}
```

Python side then can build dummy object converting this dict keys into properties:

```
Races.Terran.getRefinery()
some_bwapi_method(Races.Terran)
```

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

Solution: create proxy classes. It is possible to return objects
as weak references from function, but impossible to describe a class without accessble destructor.

Third problem, `BWAPI::Game` class has protected destructor.

Solution: create proxy class for Game. Same as previous.

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
BWAPI::Bullet
    virtual Unit getSource() const = 0;
→
output/include/bullet.h
    BWAPI::Unit getSource();
output/pybind/bullet.cpp
    class_bullet.def_property_readonly("source", [](BWAPI::Bullet& obj) -> PyBinding::Wrapper::Unit {
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

обёртки нужны, так как pybind требует деструктор класса, описать класс иначе нельзя.

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
