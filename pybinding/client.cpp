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
