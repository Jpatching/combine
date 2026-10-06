# Core / CL-3917250 qualification — 2026-10-06

## Outcome

**Blocked: no exact permitted local-trial route is established.** Core is a source-inspected candidate for Fortnite server behavior, but its client mode does not establish gameplay, its listen mode assumes an already authoritative world, and it does not implement the collision/rendering connection required by the existing Rust Skate simulation. The existing client's acquisition and normal startup remain unresolved. Core's default server hooks also alter session validation; they cannot be adopted as a route around the project's protection-bypass restriction.

This is read-only research. Public source was downloaded into temporary directories and inspected; no dependencies were installed, source compiled, DLL loaded, game launched, client downloaded, bypass implemented, or gameplay accepted. Source inspection establishes possible integration points, not their validity against the private executable.

## Pins and reproduction

Observed 2026-10-06. Public `PongooDev/Core` main HEAD was pinned to **`6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0`** (commit timestamp `2026-09-05T16:48:26+01:00`). Limited backend inspection pinned `Lawin0129/LawinServer` main to **`7f0f26d7a772c6122c42b1783fd75f497e86d3a9`**. Neither changes Combine's existing upstream pin. Fresh Skate source reads used **`f608f85e407ff1b7689d54a9aafdd16e95711ac4`**.

Read-only commands actually used: `git clone --depth 1` for the two public repositories; `git rev-parse HEAD`; `git show -s --format='%H %cI %s'`; `rg`, `rg --files`, `nl -ba`, and `sha256sum`. The initial sandbox clone failed with DNS resolution; the approved escalated source download succeeded. The clones were never executed.

| Inspected source | SHA256 |
| --- | --- |
| Core `README.md` | `30d1e00b3d32dbe24105ddd2afcab995b8ae5d9f538adc5f381a9fb9d96b27c6` |
| Core `Core/Core/dllmain.cpp` | `5ae75611ff9f2d313ece65932f65ceedf269f4a417309e9070502b2a31158f83` |
| Core `Core/Core.vcxproj` | `4cf78456028e1ce381e78b150a29da0f8eaa8e3b950187f9015c7d39bd7a6273` |
| Skate `skate/crates/skate-host/src/physics/bridge.rs` | `7b47702ca1dd3067ff17fb1bb170c289cc692d8892a7a4d4ca410254a47a4b57` |
| Skate `skate/crates/skate-host/Cargo.toml` | `12cb8bcb47ccdc9b8d7b8b800318a8dbe574a3597084be507167008e86a51320` |

The immutable links below cite the exact inspected revisions. Negative findings refer to the inspected tree and searches, not every possible external plugin or fork.

## Exact client compatibility and acquisition

**Documented:** Core claims active support for versions 1.7.2–8.00. Its own definition allows missing functionality; the range is not evidence that every CL was tested. Its repository excludes the Fortnite files, launcher and backend. [Core scope/support][core-readme]

**Source-inspected:** Core obtains the executable's engine-version string and parses release number and CL. Its fallback lookup for older Live/Cert/Next strings enumerates earlier CLs through 3870737; no exact `3917250` or `5046157` literal was found in the inspected Core tree. Release-form parsing could still recognize CL-3917250, so absence from the table is not proof of incompatibility. Signature finders and version-dependent offsets remain executable-specific runtime uncertainties. [Version parser][version]

**Inherited local evidence, not rehashed this session:** the [input diagnosis](2026-10-06-fortnite-input-diagnosis.md) records shipping executable SHA1 `b017f433b1238c0eed9f43fdb80df3ea1d90361e` and manifest SHA256 `4dd1ab60ef742b6bc56f2565be29b60896b3ce57f5e31bf7a2ba07fffe2a6ff0`. The [adapter qualification](2026-10-06-fortnite-adapter-qualification.md) records the 83,333,008-byte executable and version-name ambiguity around catalogue 3.1.1; use the exact CL and executable identity rather than a shorthand version label. Previous extraction CRC/signature checks establish integrity observations, not acquisition rights or play. The stock protected launch stalled during installation; a direct unmodified executable exited within twenty seconds, cause unresolved. No fresh private-asset inspection occurred here.

**Decision:** retain the existing client as a candidate only. Source evidence supplies no concrete 7.40 advantage that removes these blockers; no speculative 7.40 download is warranted.

## Loading, client mode and listen mode

**Source-inspected:** Core is a Windows DLL. Its attach entry starts initialization inside the host process; no launcher or supported loading mechanism is delivered by that entry point. Initialization finds engine/world objects, resolves version and core offsets, then selects exactly one client/server branch. [DLL entry and branches][dll]

Client initialization checks `GEngine`, creates a development console and polls to create a CheatManager for the local player. It never calls `Utils::Hook`, `SetupDedicatedServer` or `LoadWorld`. Moreover, `Finder::SetupOffsets` immediately returns in client mode. Thus the presence of `bIsClient` demonstrates a development client path, not a ready Skate host, fully resolved server interfaces, or autonomous local gameplay. [Client initialization][client] [Offset setup][finder]

The server branch installs engine/Fortnite hooks. Listen mode preserves the local player and reports listen-server net mode; however, `SetupDedicatedServer` returns false immediately for listen mode. Main then waits without timeout for a non-Frontend world with an authoritative game mode in `InProgress` before invoking `LoadWorld`. This is a concrete bootstrap dependency: an earlier route must already create that authoritative world. Source inspection cannot establish that the existing client satisfies it. The false return produces a setup-failed message even for the intentional listen early return. [Server sequencing][dll] [Setup and travel][travel] [Net mode][world]

Once reached, `LoadWorld` selects a map and requests travel with one required player and a playlist. The default for the candidate's older release range is `Athena_Terrain`; this establishes a source default, not a verified Creative island or sandbox. Map/playlist availability and successful player spawn remain unverified. [Map selection][utils] [World travel][travel]

**Documented/source-inspected build prerequisites:** Windows 10/11, Visual Studio, C++ workload, Windows SDK; Release x64 selects MSVC v143 and latest C++ language mode. Other configurations select v145, so the documented Release x64 selection matters. The project links bundled fmt/spdlog/curl/zlib/MinHook/Detours libraries and Windows libraries, and delay-loads D3D11/D3DCompiler/IMM32. Bundled binary-library provenance, hashes, licenses and an exact successful compiler/toolchain build would need review before execution; this report does not claim a reproducible build. [Build documentation][core-readme] [Project configuration][vcx]

## Protection/backend boundary

**Source-inspected:** Core's game-session hook substitutes successful player validation when its normal-validation condition is not enabled. Its network challenge hook can similarly change an unsuccessful response to success. These behaviors are substantive server session/challenge validation changes. This does not establish that Core disables or bypasses operating-system anti-cheat; that separate claim is not made. This report identifies them to enforce the existing boundary; it supplies no activation, loading or workaround procedure. A permitted trial must retain relevant protections and establish normal validated startup. The presence of a branch calling the original functions does not prove a working backend/session route. [Session validation][session] [Challenge handling][challenge]

**Limited backend assessment:** LawinServer's documented role covers profiles, settings and matchmaking services; its documented use depends on client traffic redirection and mentions SSL bypass. That does not provide a reviewed permissible connection for this client, nor a Skate bridge. No backend was installed or run. Core's documentation proves a missing backend component but does not prove which backend is mandatory for every local listen scenario. [Lawin scope and use][lawin-readme] [Backend route registration][lawin-index]

## Required Skate connection

```text
normal validated client startup + permitted Core loading
  -> authoritative local Fortnite world [not established]
  -> client tick/input + live world collision [adapter absent]
  -> existing Rust Session -> pose/camera/bones [existing seam]
  -> Fortnite player + skater rendering [adapter absent]
       build/edit/destroy -> replace/remove collision [adapter absent]
failure at startup or unavailable collision -> stop trial
```

The existing simulation supplies the guest side of this flow. Core supplies candidate Fortnite object access and server behavior. The pieces between them require new, independently verified code.

| Need | Inspected source evidence | Remaining qualification |
| --- | --- | --- |
| Controller input and client tick | Core client path only polls every 30 ms for CheatManager; inspected Core classes do not provide a Skate controller sampler or simulation tick driver. Existing Rust `ControllerTransport::poll` and `InputFrame::from_pad` already accept raw controller state. | Reuse or adapt that input path; prove focus, reconnect, neutral handoff and game-thread scheduling without Fortnite/Skate double movement. Raw controls need not originate in Core. |
| Live collision | Core exposes `LineTraceSingle`, but its `UStaticMesh` and `UBodySetup` wrappers contain type identity only. No triangle/convex export or Skate collision replacement was found. | A ray result is insufficient for the existing triangle/rail collision builder. Prove terrain and dynamic geometry extraction, transforms, units, ownership and replacement before skating. |
| Building | Server creation checks placement/cost, removes conflicting actors, spawns and initializes the building. | These are server actions; no callback publishes resulting collision to Skate. |
| Editing | Server edit validates actor/team/editor and replaces the building actor with a new class. | Detect removal/replacement at the rendering client's live-world state; prevent stale ramp geometry/rails. |
| Destruction | Damage handling delegates to original engine behavior and updates resources; actor destruction exists elsewhere. | Prove authoritative destruction reaches the local collision adapter and removes geometry before the next relevant simulation step. |
| Player/camera | Controller exposes pawn possession/control rotation; actor location and camera-manager bounds/FOV are accessible. | Prove safe takeover/restore, matching scale/axes, camera ownership and no native movement correction conflict. |
| Skater rendering | Skeletal mesh/animation wrappers expose existing Fortnite objects. Core's D3D11 GUI creates a separate window/device. | No importer, bone mapping, board/skater animation or game viewport render adapter exists in inspected Core. A GUI window is not in-world skater rendering. |

Sources: [client loop][client], [trace implementation][trace], [mesh wrapper][staticmesh], [body wrapper][body], [build/edit handlers][building], [damage handler][damage], [controller][controller], [actor][actor], [camera][camera], [skeletal wrapper][skeletal], [GUI][gui]. These are Core's wrappers around upstream runtime behavior; they do not establish actual behavior in CL-3917250.

**Fresh existing Rust source inspection:** `Session::new` needs private Skate assets, collision triangles/rails, spawn and heading. `collect`/`advance` drive genuine simulation; suspend-input and period methods already exist. Pose output includes root/bone transforms, names, camera, velocity and tick/state. Collision builder/install methods support replacement. However, the crate is a default Rust library (edition 2024), without a declared `cdylib`/`staticlib` or exported C ABI. Its interfaces use Rust `Vec`, `Path`, `Result` and Bevy matrices, so C++ Core cannot directly call them through a stable foreign-function interface. A narrowly designed same-process wrapper is plausible, **an inference**, and no public API or transport is selected. [Session implementation][skate-bridge] [Crate configuration][skate-cargo]

## Precise blocker and next action

Qualification ends blocked at **normal validated client startup and permitted in-process loading**: no source-backed route combines CL-3917250 provenance, successful ordinary startup, an authoritative local world and Core loading while retaining the project's protection boundary. Independent technical blockers remain the C++/Rust callable boundary and live collision/rendering adapter. Another client version or backend service does not by itself resolve them.

The owner corrected the next step to compare several client/host combinations before selecting one for startup diagnosis or a prototype. The bounded comparison below supersedes a Core-only next action. A selected candidate must establish a documented permitted loading/startup route for its exact executable and identify how it creates an authoritative world. Acceptance evidence must include executable identity, loader/backend revisions and reviewed behavior, protection-preserving startup, local movement/build/edit/destroy and clean relaunch. If that route cannot be established, retain this blocked result and select a host with a supported extension route before writing the skating adapter. Only after qualification should a thin same-process experiment advance actual `Session` ticks and demonstrate live collision replacement plus rendered pose; coordinate logging alone is insufficient.

No trial-ready claim, gameplay claim, legal clearance, owner acceptance, merge or release follows from this report. The lead records repository gate, board read-back and source publication separately at handoff.

[core-readme]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/README.md#L6-L88
[version]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Version.cpp#L17-L123
[dll]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/dllmain.cpp#L48-L195
[client]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Client.cpp#L23-L81
[finder]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Finder.cpp#L11543-L11570
[utils]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Utils.cpp#L296-L312
[world]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Private/World.cpp#L28-L43
[vcx]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core.vcxproj#L42-L143
[session]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/FortniteGame/Private/FortGameSession.cpp#L4-L24
[challenge]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Private/NetConnection.cpp#L84-L106
[trace]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Private/KismetSystemLibrary.cpp#L52-L68
[staticmesh]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/Engine/StaticMesh.h#L1-L10
[body]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/PhysicsEngine/BodySetup.h#L1-L10
[building]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/FortniteGame/Private/Player/FortPlayerController.cpp#L704-L893
[damage]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/FortniteGame/Private/Building/BuildingActor.cpp#L52-L144
[controller]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/GameFramework/Controller.h#L17-L63
[actor]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h#L170-L192
[camera]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/Camera/PlayerCameraManager.h#L1-L23
[skeletal]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Classes/Components/SkeletalMeshComponent.h#L1-L21
[gui]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Gui/Private/Gui.cpp#L186-L300
[travel]: https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Utils.cpp#L445-L519
[lawin-readme]: https://github.com/Lawin0129/LawinServer/blob/7f0f26d7a772c6122c42b1783fd75f497e86d3a9/README.md#L75-L83
[lawin-index]: https://github.com/Lawin0129/LawinServer/blob/7f0f26d7a772c6122c42b1783fd75f497e86d3a9/index.js#L1-L36
[skate-bridge]: https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs#L32-L304
[skate-cargo]: https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/Cargo.toml


## Multiple client and host comparison — owner correction

The owner requested several candidates so qualification does not depend on one client/host bet. This authorizes broader research, not game downloads or execution. Four bounded combinations were compared using the evidence available on 2026-10-06. Two Core rows separate existing-client reuse from a version change; they are not independent loading solutions. FortExternalServer tests a distinct external-process design. UEFN supplies an official acquisition/extension comparator. None is a verified host for the actual Rust Skate simulation.

| Client + host combination | Exact client access | Protection-preserving launch/load | Live collision, rendering and actual Skate bridge | Evidence confidence / disposition |
| --- | --- | --- | --- | --- |
| Existing CL-3917250 + Core `6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0` | Existing executable identity is inherited evidence above; provenance and ordinary startup unresolved. No new game download needed. | Missing documented permitted DLL loading and authoritative-world bootstrap; source-inspected session/challenge overrides require exclusion/review. | Server building/editing exist, collision triangles/rails export and replacement lifecycle absent; Rust callable boundary and in-world skater rendering absent. | Fresh source inspection plus inherited client observations. Candidate retained; blocked, not trial-ready. |
| 7.40 / CL-5046157 + same Core pin | Exact client acquisition and identity unknown here. Broad Core support range does not verify this CL. | Same DLL/backend/bootstrap gap as existing Core. Changing version supplies no independent permitted loading route. | No inspected exact-CL advantage for input, geometry or real Skate rendering. Existing wrapper gaps persist. | Range documented; exact CL behavior unverified. Deprioritize unless concrete compatibility advantage and suitable acquisition route are evidenced. No speculative download. |
| 3.6 / CL-4019403 + FortExternalServer `season-3` design | Main documentation names this exact CL and UE4.19. No reviewed game acquisition route. | Standalone host is documented, but it writes machine-code stubs into the game and replaces engine functions including `KickPlayer`. This does not qualify protection-preserving launch and is not an automatic safe alternative to a DLL. | External-process control is a genuinely different design, with no documented existing Rust Skate connection or live geometry export. It departs from the preferred same-process route; no transport selected. | Fresh primary documentation at main pin `b39f9b7a78a82b75621a4829f55d6cfafbbbb83f`; main contains README/LICENSE only. Implementation branch download was interrupted: no inspected implementation pin, build or gameplay claim. Negative qualification for current trial readiness. |
| Official current Fortnite + UEFN/Verse | Epic documents current acquisition through its launcher; exact installed CL not observed. This is not historical-client acquisition evidence. | Official creator/playtesting route documented; no custom loading procedure needed for documented Verse tools. No local trial executed. | Epic documents Verse/custom behavior and physics props. No supported callable path into our existing Rust `Session`, full mutable-world triangle/rail export, or original Skate pose/render integration was established from reviewed docs. Built-in physics does not prove preservation of actual Skate mechanics. | Fresh official documentation. Strongest documented access route; bridge evidence absent. Comparator only, not an owner-approved replacement or a claimed impossible platform. |

Primary alternative-host evidence: [FortExternalServer pinned main README](https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b39f9b7a78a82b75621a4829f55d6cfafbbbb83f/README.md#L13-L87). Its exact version table is documentation, not tested executable compatibility. The external-process mechanism avoids a DLL artifact but still changes game memory and executes stubs at engine call sites; this does not establish an OS anti-cheat bypass, and no such universal claim is made.

Official comparison evidence: [Epic acquisition and UEFN playtesting requirements](https://dev.epicgames.com/documentation/en-us/fortnite/install-and-launch-fortnite-creative-and-unreal-editor-for-fortnite), [Verse programming](https://dev.epicgames.com/documentation/en-us/fortnite/programming-with-verse-in-unreal-editor-for-fortnite), and [UEFN physics](https://dev.epicgames.com/documentation/en-us/fortnite/getting-started-with-physics). Reviewed documentation describes Epic's physics/Verse tools; it does not demonstrate the required existing Rust integration. This is an evidence gap, not a claim that every possible sanctioned future route is impossible.

Inherited exclusions remain useful: the [earlier adapter qualification](2026-10-06-fortnite-adapter-qualification.md) pinned Project Reboot3.0 `3f6417ee6b07063bb6f83902ad3971f998888bab` and launcher `64dc971da499f1856f40af992d0068c5801e344b`; the [guidance qualification](2026-10-06-fortnite-guidance-qualification.md) compared Rift/Era and recorded loading/prerequisite gaps. Those inspected launcher routes and absent Skate seams remain inherited negative evidence, not fresh latest-HEAD results. Reopening their broad version lists would not establish a different permitted route. LawinServer supplies backend services, not a fifth native Skate host.

**Recommendation:** keep existing Core and official UEFN as the two useful comparison anchors: one preserves direct native-bridge potential and existing-client reuse, the other supplies documented official access. Neither qualifies the full outcome yet. Keep Core7.40 conditional and FortExternalServer as a researched negative, rather than downloading either client. The next decision should use actual evidence of a permitted exact-client loading/extension route capable of calling the existing simulation. Stop a candidate if it needs protection bypass, lacks suitable client access, or cannot establish mutable collision and rendered actual Skate state. Only then select one bounded startup qualification/prototype; acceptance requires genuine simulation advancement, visible pose and ramp edit/destruction collision replacement. This comparison does not select a new transport, port Skate into Verse, install a host, or weaken the interactive Fortnite-world requirement.
