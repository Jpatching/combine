// Private opt-in checkpoint template. Coordinates are strict private data.
// Reaching a checkpoint leaves loading/layer remain unqualified.
const CONFIG = __CONFIG__;
let held = false;
function emit(event, reason) {log('COMBINE_CHECKPOINT ' + CONFIG.token + ' PRIVATE ' + JSON.stringify({event,reason}));}
function player() {
    const id = native('CONVERT_INT_TO_PLAYERINDEX', native('GET_PLAYER_ID'));
    const ped = native('GET_PLAYER_CHAR', id);
    if (native('COMBINE_SKATE_EVAL_OWNER').player >= 0 || !native('COMBINE_SKATE_READY') || !native('IS_PLAYER_PLAYING', id)
        || !native('DOES_CHAR_EXIST', ped) || !native('IS_CHAR_ON_FOOT', ped)
        || !native('IS_PLAYER_CONTROL_ON', id) || native('IS_PAUSE_MENU_ACTIVE')
        || (native('HAS_CUTSCENE_LOADED') && !native('HAS_CUTSCENE_FINISHED'))) throw new Error('state');
    return ped;
}
while (true) {
    wait(50);
    let pressed = false;
    try {pressed = native('COMBINE_SKATE_EVAL_KEY', 2) === 1;} catch (_) {continue;}
    if (pressed && !held) {
        let ped = null, original = null, moved = false;
        try {
            ped = player(); original = native('GET_CHAR_COORDINATES', ped);
            if (![original.x,original.y,original.z].every(Number.isFinite)) throw new Error('position');
            const [x,y,z] = CONFIG.position;
            native('REQUEST_COLLISION_AT_POSN', x,y,z);
            native('SET_CHAR_COORDINATES_NO_OFFSET', ped,x,y,z); moved = true;
            const deadline = Date.now() + 10000;
            let reached = false;
            while (Date.now() < deadline) {
                wait(100);
                if (player() !== ped) throw new Error('player-changed');
                const position = native('GET_CHAR_COORDINATES', ped);
                if (Math.hypot(position.x-x,position.y-y,position.z-z) <= 1
                    && !native('IS_CHAR_IN_AIR',ped) && !native('IS_CHAR_DEAD',ped)
                    && !native('IS_CHAR_WAITING_FOR_WORLD_COLLISION',ped)) {reached=true;break;}
            }
            if (!reached) throw new Error('checkpoint-unavailable');
            emit('reached','position-observed-loading-layer-unqualified');
        } catch (_) {
            if (moved) {
                try {
                    if (player() !== ped) throw new Error('player-changed');
                    native('SET_CHAR_COORDINATES_NO_OFFSET',ped,original.x,original.y,original.z);
                    wait(100);
                    const position = native('GET_CHAR_COORDINATES',ped);
                    if (Math.hypot(position.x-original.x,position.y-original.y,position.z-original.z)>1) throw new Error('rollback-position');
                    emit('restored','checkpoint-unavailable');
                } catch (_) {emit('recovery-unverified','checkpoint-unavailable');}
            } else emit('refused','prerequisites');
        }
    }
    held = pressed;
}
