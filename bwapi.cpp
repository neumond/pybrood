#include <pybind11/pybind11.h>
#include <BWAPI.h>
#include <BWAPI/Client.h>

namespace py = pybind11;

namespace PyBinding {
    #include "pybinding/common.cpp"
    #include "pybinding/force.cpp"
    #include "pybinding/player.cpp"
}

PYBIND11_PLUGIN(pybrood) {
    py::module m("pybrood", "BWAPI python module");

    #define MODCODE

    #include "pybinding/force.cpp"
    #include "pybinding/player.cpp"
    #include "pybinding/client.cpp"
    #include "pybinding/game.cpp"

    return m.ptr();
}
