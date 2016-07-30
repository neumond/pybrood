py::module m_Client = m.def_submodule("client");
m_Client.def("is_connected", []() -> bool {
    return BWAPI::BWAPIClient.isConnected();
});
m_Client.def("connect", []() -> bool {
    return BWAPI::BWAPIClient.connect();
});
m_Client.def("disconnect", [](){
    BWAPI::BWAPIClient.disconnect();
});
m_Client.def("update", [](){
    BWAPI::BWAPIClient.update();
});
