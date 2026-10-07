// Synthetic interface checks only; this does not run CLEO or GTA.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
let frame = -1;
const stop = new Error("end of test frames");
const samples = [];
const reads = [];
const context = {
    wait(delay) {
        assert.equal(delay, 0);
        if (++frame === 5) throw stop;
    },
    native(name, ...args) {
        reads.push([frame, name]);
        switch (name) {
            case "COMBINE_IV_READY": return frame !== 0;
            case "GET_PLAYER_ID": return 0;
            case "CONVERT_INT_TO_PLAYERINDEX": assert.deepEqual(args, [0]); return 41;
            case "GET_PLAYER_CHAR": assert.deepEqual(args, [41]); return 42;
            case "DOES_CHAR_EXIST": assert.deepEqual(args, [42]); return frame !== 1;
            case "GET_CHAR_COORDINATES": return {x: frame, y: 2, z: 3};
            case "GET_GAME_CAM": return 43;
            case "DOES_CAM_EXIST": assert.deepEqual(args, [43]); return frame !== 2;
            case "GET_CAM_POS": assert.deepEqual(args, [43]); return {x: 4, y: frame, z: 6};
            case "GET_CAM_ROT": return {angleX: 7, angleY: 8, angleZ: frame};
            case "GET_POSITION_OF_ANALOGUE_STICKS":
                assert.deepEqual(args, [0]);
                return {pLeftX: -frame, pLeftY: frame, pRightX: 127, pRightY: -128};
            case "GET_GAME_TIMER": return frame * 16;
            case "GET_FRAME_TIME": return 0.016;
            case "IS_CHAR_ON_FOOT": return frame === 3;
            case "COMBINE_IV_SAMPLE": samples.push(args); return;
            default: throw new Error(`Unexpected native query or write: ${name}`);
        }
    },
};
try {
    vm.runInNewContext(fs.readFileSync(`${__dirname}/combine_iv_diagnostic.js`, "utf8"), context);
} catch (error) {
    if (error !== stop) throw error;
}
assert.deepEqual(samples, [
    [48, 0.016, 42, 1, 3, 2, 3, 4, 3, 6, 7, 8, 3, -3, 3, 127, -128],
    [64, 0.016, 42, 0, 4, 2, 3, 4, 4, 6, 7, 8, 4, -4, 4, 127, -128],
]);
assert.equal(reads.some(([f, name]) => f === 0 && name !== "COMBINE_IV_READY"), false);
assert.equal(reads.some(([f, name]) => f === 1 && name === "GET_CHAR_COORDINATES"), false);
assert.equal(reads.some(([f, name]) => f === 2 && name === "GET_CAM_POS"), false);
console.log("PASS: readiness/player/camera guards; changing telemetry; 17-argument ABI; read-only queries");
