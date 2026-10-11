// Private opt-in diagnostic template. prepare-probe embeds strict point data.
// Reuses the reviewed plugin-owned float buffer and conditional ground native.
// No movement, camera, teleport, freezing or loading/layer inference.
const CONFIG = __CONFIG__;
const SENTINEL = -1234567;
function emit(value) {
    log('COMBINE_GROUND_COLLECT ' + CONFIG.token + ' PRIVATE ' + JSON.stringify(value));
}
function current() {
    const player = native('CONVERT_INT_TO_PLAYERINDEX', native('GET_PLAYER_ID'));
    if (!native('IS_PLAYER_PLAYING', player) || !native('IS_PLAYER_CONTROL_ON', player)
        || native('IS_PAUSE_MENU_ACTIVE')
        || (native('HAS_CUTSCENE_LOADED') && !native('HAS_CUTSCENE_FINISHED'))) throw new Error();
    const ped = native('GET_PLAYER_CHAR', player);
    if (!native('DOES_CHAR_EXIST', ped) || !native('IS_CHAR_ON_FOOT', ped)) throw new Error();
    return {player, ped};
}
function physical(ped) {
    // Retain candidate witness data; these natives are not a contact oracle.
    return {position: native('GET_CHAR_COORDINATES', ped),
        velocity: native('GET_CHAR_VELOCITY', ped), speed: native('GET_CHAR_SPEED', ped),
        height_above_ground: native('GET_CHAR_HEIGHT_ABOVE_GROUND', ped),
        air: native('IS_CHAR_IN_AIR', ped), stopped: native('IS_CHAR_STOPPED', ped),
        waiting: native('IS_CHAR_WAITING_FOR_WORLD_COLLISION', ped),
        dead: native('IS_CHAR_DEAD', ped), water: native('IS_CHAR_IN_WATER', ped),
        injured: native('IS_CHAR_INJURED', ped)};
}
let held = false, attempt = 0;
while (true) {
    wait(50);
    let key = false;
    try { key = native('COMBINE_SKATE_EVAL_KEY', 0) === 1; } catch (_) { continue; }
    if (key && !held) {
        let armed = false;
        try {
            const owner = current(), started = native('COMBINE_SKATE_EVAL_TIME');
            emit({kind: 'start', attempt: ++attempt});
            for (const point of CONFIG.checkpoints) {
                for (let batch = 0; batch < 3; batch++) {
                    const now = current();
                    if (now.player !== owner.player || now.ped !== owner.ped
                        || ((native('COMBINE_SKATE_EVAL_TIME') - started) >>> 0) > 30000) throw new Error();
                    const before = physical(owner.ped);
                    const address = native('COMBINE_GROUND_SEED', SENTINEL);
                    if (!Number.isInteger(address) || address === 0) throw new Error();
                    armed = true;
                    let reading;
                    try {
                        const success = native('GET_GROUND_Z_FOR_3D_COORD',
                            point.position[0], point.position[1], point.query_z_m, address);
                        const intact = native('COMBINE_GROUND_INTACT') === 1;
                        const height = native('COMBINE_GROUND_VALUE');
                        reading = {position: point.position,
                            query_z_m: point.query_z_m,
                            query_success: typeof success === 'boolean' ? success : null,
                            height_m: Number.isFinite(height) && height !== SENTINEL ? height : null,
                            buffer_intact: intact, physical_before: before,
                            physical_after: physical(owner.ped)};
                    } finally { native('COMBINE_GROUND_CLEAR'); armed = false; }
                    emit({kind: 'reading', attempt, label: point.label, batch, reading});
                    if (batch < 2) wait(100);
                }
            }
            emit({kind: 'complete', attempt});
        } catch (_) { emit({kind: 'refused', attempt}); }
        finally {
            if (armed) {
                try { native('COMBINE_GROUND_CLEAR'); }
                catch (_) { emit({kind: 'clear-failed', attempt}); }
            }
        }
    }
    held = key;
}
