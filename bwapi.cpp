#include <pybind11/pybind11.h>
#include <BWAPI.h>
#include <BWAPI/Client.h>


namespace py = pybind11;


namespace PyBinding {
    namespace Client {
        #include "pybinding/client.cpp"
    }

    class ForceWeakref
    {
    protected:
        BWAPI::Force obj;
    public:
        ForceWeakref(BWAPI::Force iobj) : obj(iobj){};
        int getID(){
            return obj->getID();
        }
        std::string getName(){
            return obj->getName();
        }
        // virtual Playerset getPlayers() const = 0;
    };

    namespace Game {
        #include "pybinding/game.cpp"
    }
}

PYBIND11_PLUGIN(pybrood) {
    py::module m("pybrood", "BWAPI python module");

    py::class_<PyBinding::ForceWeakref> force(m, "Force");
    force.def("__init__", [](PyBinding::ForceWeakref){
        throw std::runtime_error("Force objects can't be instantiated from python side");
    });
    force.def_property_readonly("id", &PyBinding::ForceWeakref::getID);
    force.def_property_readonly("name", &PyBinding::ForceWeakref::getName);

    py::module m_Client = m.def_submodule("client");
    m_Client.def("is_connected", &PyBinding::Client::isConnected);
    m_Client.def("connect", &PyBinding::Client::connect);
    m_Client.def("disconnect", &PyBinding::Client::disconnect);
    m_Client.def("update", &PyBinding::Client::update);

    // py::class_<BWAPI::TilePosition>(m, "TilePosition")
    //     .def(py::init<int, int>())
    //     .def("getLength", &BWAPI::TilePosition::getLength);

    py::module m_Game = m.def_submodule("game");
    //
    m_Game.def("countdown_timer", &PyBinding::Game::countdownTimer);
    m_Game.def("elapsed_time", &PyBinding::Game::elapsedTime);
    m_Game.def("enable_flag", &PyBinding::Game::enableFlag);
    //
    m_Game.def("get_average_FPS", &PyBinding::Game::getAverageFPS);
    //
    m_Game.def("get_force", &PyBinding::Game::getForce);
    m_Game.def("get_forces", &PyBinding::Game::getForces);
    m_Game.def("get_FPS", &PyBinding::Game::getFPS);
    m_Game.def("get_frame_count", &PyBinding::Game::getFrameCount);
    //
    m_Game.def("get_last_event_time", &PyBinding::Game::getLastEventTime);
    m_Game.def("get_latency", &PyBinding::Game::getLatency);
    m_Game.def("get_latency_frames", &PyBinding::Game::getLatencyFrames);
    m_Game.def("get_latency_time", &PyBinding::Game::getLatencyTime);
    //
    m_Game.def("get_remaining_latency_frames", &PyBinding::Game::getRemainingLatencyFrames);
    m_Game.def("get_remaining_latency_time", &PyBinding::Game::getRemainingLatencyTime);
    m_Game.def("get_replay_frame_count", &PyBinding::Game::getReplayFrameCount);
    m_Game.def("get_revision", &PyBinding::Game::getRevision);
    //
    m_Game.def("has_creep", &PyBinding::Game::hasCreep);
    //
    m_Game.def("is_battle_net", &PyBinding::Game::isBattleNet);
    //
    m_Game.def("is_debug", &PyBinding::Game::isDebug);
    m_Game.def("is_explored", &PyBinding::Game::isExplored);
    //
    m_Game.def("is_flag_enabled", &PyBinding::Game::isFlagEnabled);
    m_Game.def("is_GUI_enabled", &PyBinding::Game::isGUIEnabled);
    m_Game.def("is_in_game", &PyBinding::Game::isInGame);
    m_Game.def("is_lat_com_enabled", &PyBinding::Game::isLatComEnabled);
    m_Game.def("is_multiplayer", &PyBinding::Game::isMultiplayer);
    m_Game.def("is_paused", &PyBinding::Game::isPaused);
    m_Game.def("is_replay", &PyBinding::Game::isReplay);
    //
    m_Game.def("is_visible", &PyBinding::Game::isVisible);
    //
    m_Game.def("is_walkable", &PyBinding::Game::isWalkable);
    //
    m_Game.def("leave_game", &PyBinding::Game::leaveGame);
    m_Game.def("map_file_name", &PyBinding::Game::mapFileName);
    m_Game.def("map_hash", &PyBinding::Game::mapHash);
    m_Game.def("map_height", &PyBinding::Game::mapHeight);
    m_Game.def("map_name", &PyBinding::Game::mapName);
    m_Game.def("map_path_name", &PyBinding::Game::mapPathName);
    m_Game.def("map_width", &PyBinding::Game::mapWidth);
    //
    m_Game.def("pause_game", &PyBinding::Game::pauseGame);
    m_Game.def("ping_minimap", &PyBinding::Game::pingMinimap);
    //
    m_Game.def("restart_game", &PyBinding::Game::restartGame);
    m_Game.def("resume_game", &PyBinding::Game::resumeGame);
    //
    m_Game.def("set_frame_skip", &PyBinding::Game::setFrameSkip);
    m_Game.def("set_GUI", &PyBinding::Game::setGUI);
    //
    m_Game.def("set_lat_com", &PyBinding::Game::setLatCom);
    m_Game.def("set_local_speed", &PyBinding::Game::setLocalSpeed);

    return m.ptr();
}
