#ifndef MODCODE

class ForceWeakref
{
protected:
    BWAPI::Force obj;
public:
    ForceWeakref(BWAPI::Force iobj) : obj(iobj){};
    int getID(){ return obj->getID(); };
    std::string getName(){ return obj->getName(); };
    py::set getPlayers(){
        return set_converter<PlayerWeakref, BWAPI::Playerset>(obj->getPlayers());
    }
};

#else

py::class_<PyBinding::ForceWeakref> force(m, "Force");
force.def("__init__", [](PyBinding::ForceWeakref){
    throw std::runtime_error("Force objects can't be instantiated from python side");
});
force.def_property_readonly("id", &PyBinding::ForceWeakref::getID);
force.def_property_readonly("name", &PyBinding::ForceWeakref::getName);
force.def("get_players", &PyBinding::ForceWeakref::getPlayers);

#endif
