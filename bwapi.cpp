#include <pybind11/pybind11.h>
#include <BWAPI.h>
#include <BWAPI/Client.h>

namespace py = pybind11;

namespace PyBinding {
    #include "pybinding/common.cpp"
    #include "pybinding/force_auto.cpp"
    #include "pybinding/player_auto.cpp"
    #include "pybinding/unit_auto.cpp"
    #include "pybinding/unittype_auto.cpp"
}

PYBIND11_PLUGIN(pybrood) {
    py::module m("pybrood", "BWAPI python module");

    #define MODCODE

    #include "pybinding/client_auto.cpp"
    #include "pybinding/game_auto.cpp"
    #include "pybinding/force_auto.cpp"
    #include "pybinding/player_auto.cpp"
    #include "pybinding/unit_auto.cpp"
    #include "pybinding/unittype_auto.cpp"

    return m.ptr();
}
