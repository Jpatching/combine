// Read-only native queries. No player, camera, input, asset or protection changes.
while (true) {
    wait(250);
    let scene=0, control=false, onFoot=false;
    const ready=Boolean(native("COMBINE_SKATE_READY"));
    try {
        if (ready) {
            const paused=Boolean(native("IS_PAUSE_MENU_ACTIVE"));
            const cutscene=Boolean(native("HAS_CUTSCENE_LOADED")) && !native("HAS_CUTSCENE_FINISHED");
            const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
            const ped=native("GET_PLAYER_CHAR",player);
            const playing=Boolean(native("IS_PLAYER_PLAYING",player));
            control=playing && Boolean(native("IS_PLAYER_CONTROL_ON",player));
            onFoot=playing && Boolean(native("DOES_CHAR_EXIST",ped)) && Boolean(native("IS_CHAR_ON_FOOT",ped));
            scene=paused?3:cutscene?2:playing?1:4;
        }
    } catch (_) {scene=0;control=false;onFoot=false;}
    native("COMBINE_GAME_STATUS",scene,control?1:0,onFoot?1:0);
}
