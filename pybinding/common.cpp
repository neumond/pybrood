template <class Weakref, class BWSetContainer>
inline py::set set_converter(BWSetContainer src){
    py::set out;
    for (auto it = src.cbegin(); it != src.cend(); ++it )
        out.add(py::cast(Weakref(*it)));
    return out;
}


class UnitWeakref;
class UnitTypeWeakref;
class ForceWeakref;
class PlayerWeakref;
class BulletTypeWeakref;
class DamageTypeWeakref;
class UpgradeTypeWeakref;
class WeaponTypeWeakref;
class PlayerTypeWeakref;
