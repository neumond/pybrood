template <class Weakref, class BWSetContainer>
inline py::set set_converter(BWSetContainer src){
    py::set out;
    for (auto it = src.cbegin(); it != src.cend(); ++it )
        out.add(py::cast(Weakref(*it)));
    return out;
}


class PlayerWeakref;
class ForceWeakref;
class UnitWeakref;
class UnitTypeWeakref;
