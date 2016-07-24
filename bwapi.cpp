#include <pybind11/pybind11.h>
#include <BWAPI.h>
#include <BWAPI/Client.h>

int add(int i, int j) {
    return i + j;
}

namespace PyBinding {
    namespace Client {
        bool isConnected(){
            return BWAPI::BWAPIClient.isConnected();
        }
        bool connect(){
            return BWAPI::BWAPIClient.connect();
        }
        void disconnect(){
            BWAPI::BWAPIClient.disconnect();
        }
        void update(){
            BWAPI::BWAPIClient.update();
        }
    }
}


namespace py = pybind11;

PYBIND11_PLUGIN(pybrood) {
    py::module m("pybrood", "BWAPI python module");

    m.def("add", &add, "A function which adds two numbers");
    m.def("Client_isConnected", &PyBinding::Client::isConnected, "");
    m.def("Client_connect", &PyBinding::Client::connect, "");
    m.def("Client_disconnect", &PyBinding::Client::disconnect, "");
    m.def("Client_update", &PyBinding::Client::update, "");

    return m.ptr();
}
