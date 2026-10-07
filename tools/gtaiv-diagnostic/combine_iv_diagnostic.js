// Read-only queries, pinned gta_iv.json API 0.108. No player/camera/input writes.
while (true) {
    wait(0);
    if (!native("COMBINE_IV_READY")) continue;
    const player = native("CONVERT_INT_TO_PLAYERINDEX", native("GET_PLAYER_ID"));
    const ped = native("GET_PLAYER_CHAR", player);
    if (!native("DOES_CHAR_EXIST", ped)) continue;
    const position = native("GET_CHAR_COORDINATES", ped);
    const camera = native("GET_GAME_CAM");
    if (!native("DOES_CAM_EXIST", camera)) continue;
    const cameraPosition = native("GET_CAM_POS", camera);
    const rotation = native("GET_CAM_ROT", camera);
    const sticks = native("GET_POSITION_OF_ANALOGUE_STICKS", 0);
    native("COMBINE_IV_SAMPLE",
        native("GET_GAME_TIMER"), native("GET_FRAME_TIME"), ped,
        native("IS_CHAR_ON_FOOT", ped) ? 1 : 0,
        position.x, position.y, position.z,
        cameraPosition.x, cameraPosition.y, cameraPosition.z,
        rotation.angleX, rotation.angleY, rotation.angleZ,
        sticks.pLeftX, sticks.pLeftY, sticks.pRightX, sticks.pRightY);
}
