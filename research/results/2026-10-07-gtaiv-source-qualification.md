# GTA IV 1.2.0.59 loader and diagnostic source research

Observed 2026-10-07. Public documentation/source and GitHub metadata only. No game files accessed by this research agent, no bundle downloaded, no plugin built or loaded, no launch or gameplay test. A source-documented route is a candidate, not qualification.

## Candidate pins

| Component | Selected identity | Evidence |
| --- | --- | --- |
| CLEO Redux | release 1.5.1, source commit `bbf6773fe8cc1bfa95c73509a25928f97b0d8d13` | [release](https://github.com/cleolibrary/CLEO-Redux/releases/tag/1.5.1), GitHub ref API returned a commit directly |
| CLEO x86 portable asset | `cleo_redux_1.5.1.x86.zip`, 3,928,451 bytes, metadata SHA256 `8dcc0e83e25ab8c57a52d4ca65470b8ec6fc4e94121e5905b826079d75c2807b` | [release metadata](https://api.github.com/repos/cleolibrary/CLEO-Redux/releases/tags/1.5.1); not independently byte-verified |
| C++ SDK header | `SDK/cleo_redux_sdk.h` at the above CLEO commit; locally fetched source SHA256 `c7b1e01f415c0fb59c00e630278a68c2e87a05739d247e284b01a73a038204a7` | [header](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h) |
| Ultimate ASI Loader | release v9.7.4, commit `6b440669144c4a0bef5718ab155df160d231cd42` | [release](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases/tag/v9.7.4), GitHub ref API returned a commit directly |
| ASI Loader asset | `Ultimate-ASI-Loader.zip`, 3,910,913 bytes; metadata SHA256 `952cebfc30d525afc2bdbaca954329d405ded3aa688a83027354dae14dfd5c5f` | [release metadata](https://api.github.com/repos/ThirteenAG/Ultimate-ASI-Loader/releases/tags/v9.7.4); not independently byte-verified |
| GTA IV native definitions | sannybuilder/library commit `34bedee0be2f57047ed8f0705c81f137ede3d3ce`, `gta_iv/gta_iv.json`, API version 0.108; fetched source SHA256 `ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b` | [definitions](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json) |
| Universal Modder guidance | commit `76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70` | [engine guidance](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/skills/mod-any-game/references/engines/big-frameworks.md) |

CLEO's pinned introduction explicitly includes GTA IV Complete Edition 1.2.0.43 and 1.2.0.59 and Windows 10/11. Its portable archive excludes the ASI loader; pinned installation guidance chooses `dinput8.dll` for GTA IV. Native plugins are DLLs renamed `.cleo`, scanned from `CLEO/CLEO_PLUGINS` at startup via LoadLibrary. [Supported versions](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md), [installation](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/installation.md), [SDK](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-sdk.md).

Original IV-SDK documents only 1.0.7.0 and 1.0.8.0 EFIGS and states no plans for additional versions because classes/functions differ. IV-SDK .NET likewise documents 1.0.7.0/1.0.8.0. Neither supplies evidence for 1.2.0.59. [Original SDK](https://github.com/Zolika1351/iv-sdk/blob/master/README.md), [NET FAQ](https://github.com/ClonkAndre/IV-SDK-DotNet/blob/main/Documentation/FAQ.md).

Universal Modder's pinned RAGE guidance concerns GTA V and RDR2: story mode, version matching, community loader APIs, originals preserved through mod copies, and camera/script timing pitfalls. Its GTA V ScriptHookV and BattlEye instructions are not GTA IV compatibility evidence and must not be applied to IV. The example passthrough helper is prior architectural art, not proof that this Skate host needs a helper.

## Verified SDK signatures

From the pinned header:

```cpp
typedef void* Context;
typedef HandlerResult (*CommandHandler)(Context);
typedef void (*OnTickCallback)(unsigned int current_time, int time_step);
long GetSDKVersion();
HostId GetHostId(); // IV = 9
void Log(const char* text);
void RegisterCommand(const char* name, CommandHandler handler,
                     const char* permission = nullptr);
intptr_t GetIntParam(Context ctx);
float GetFloatParam(Context ctx);
void GetStringParam(Context ctx, char* dest, unsigned char maxlen);
void OnBeforeScripts(OnTickCallback callback);
void OnAfterScripts(OnTickCallback callback);
void OnRuntimeInit(OnRuntimeInitCallback callback);
void GetCLEOVersion(char* dest);
void* GetSymbolAddress(const char* symbol);
```

OnBeforeScripts and OnAfterScripts run on each main-loop iteration before/after scripts; OnRuntimeInit runs on new game, save load, or explicit SDK RuntimeInit. `current_time` and `time_step` units are not defined by this header; record raw values until runtime or further authoritative evidence establishes meaning. Avoid calling RuntimeInit/RuntimeNextTick from a diagnostic because those drive the runtime. `HandlerResult::CONTINUE = 0`, BREAK = 1, TERMINATE = 2, ERR = -1.

The docs say SDK version 6, but this pinned header includes `TriggerEvent` marked since v7. Do not silently assume an installed binary's SDK number; log GetSDKVersion and use only required methods (the tick callbacks require v4). The SDK provides no named direct GTA native-invocation function, and GetSymbolAddress supplies no documented GTA IV symbols here. Thus direct C++ native calls are unproven.

## Supported read-only diagnostic route

Inference from two documented interfaces: read game data in a CLEO JS script using native(commandName, ...inputs), pass numbers to a custom C++ diagnostic command registered via RegisterCommand, and correlate them with the native OnAfterScripts callback. This proves the script/native-plugin path if it works in gameplay. It does not prove direct C++ access to GTA natives. [JS API](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/api.md), [C++ guide](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/cpp-sdk.md).

Exact JS native inputs/outputs from pinned GTA IV definitions (single output returns its value; multiple outputs return an object with these exact field names):

| Query | Inputs | Returned value |
| --- | --- | --- |
| GET_PLAYER_ID | none | id integer |
| CONVERT_INT_TO_PLAYERINDEX | playerId integer | Player handle |
| GET_PLAYER_CHAR | Player handle | Char handle |
| GET_CHAR_COORDINATES | Char handle | `{x,y,z}` floats |
| GET_GAME_CAM | none | Camera handle |
| GET_CAM_POS | Camera handle | `{x,y,z}` floats |
| GET_CAM_ROT | Camera handle | `{angleX,angleY,angleZ}` floats |
| GET_POSITION_OF_ANALOGUE_STICKS | pad integer | `{pLeftX,pLeftY,pRightX,pRightY}` integers |
| GET_GAME_TIMER | none | integer milliseconds since game start |
| GET_FRAME_TIME | none | float; units not documented in definition |
| IS_CHAR_ON_FOOT | Char handle | boolean |
| DOES_CHAR_EXIST | Char handle | boolean |

Do not label analogue input ranges, the pad index, frame time units, or angle units verified: these signatures do not establish them. Pad 0 is a candidate to test, with physical controller movements proving it supplies the real input. `GET_PAD_STATE` parameters are `_p1,_p2` and `IS_BUTTON_PRESSED(pad,button)` gives no button mapping in this inspected definition; omit mappings until separately supported. A script can use wait(0) to yield and resume in the main loop and must guard absent/loading player handles.

Custom commands need JSON definitions matching registered name and parameter order. GTA IV uses `CLEO/.config/gta_iv.json`, minimum API 0.108. The pinned definitions documentation says runtime downloads missing/invalid definitions, and combines game and unknown-host definitions. Preserve a baseline pinned file and add a local command definition deliberately; do not imply arbitrary SDK commands become visible without a definition. The inspected config docs provide no setting to turn off definition updates. [Definitions](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/definitions.md), [config](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/config.md).

## Separate qualifications

- Geometry: GET_GROUND_Z_FOR_3D_COORD(x,y,z)->float ground Z and GET_CHAR_HEIGHT_ABOVE_GROUND(char)->height exist in definitions. They do not prove collision mesh access, contact normals, continuous sweeps, or Skate-compatible surface collision.
- Grind: no inspected source proves traversable edge extraction or grind detection. Remains unqualified.
- Bones: GET_PED_BONE_POSITION(char,boneId,x,y,z)->Vector3 position exists, but binding, offsets, coordinate convention and real runtime result need qualification. Position reads do not prove writable bone transforms or Skate animation integration.

All loader compatibility, changing gameplay values, repeated loading, disabled normal walking/driving/camera controls, collision, grind and bone-animation behavior remain runtime checks. Do not issue a skating proof spec as an accepted route merely from these sources.
