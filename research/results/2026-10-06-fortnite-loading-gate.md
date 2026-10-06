# Fortnite startup/loading gate — 2026-10-06

## Current decision and scope

The owner narrowed the prerequisite: establish a reviewed startup/native-loading
route, then build the missing adapter through a small experiment. Existing SDKs,
official plugin support, ready-made loaders and completed collision/rendering
adapters are not mandatory. Reverse engineering remains an available method.
The existing no-DRM/anti-cheat-bypass restriction remains in force; hooking or
local server emulation alone is not evidence that such a bypass occurs. This
clarification prevents absence of implementation from becoming a circular gate.

**Result:** no runnable route selected in this pass. The fallback's actual source
is now pinned; Core still has no demonstrated startup/loading sequence for the
existing client. A new bounded run of that unchanged client exited in 2.812 seconds
with code 0 and no original configuration changes. This is an observed startup
result, not proof of an anti-cheat failure or a reason to abandon reverse engineering.
The one-surface Skate experiment remains conditional on obtaining a live host;
its missing adapter code is subsequent engineering work.

## Fallback findings: FortExternalServer

**Gate unpassed for this fallback.** The actual `season-3` implementation has now been inspected, replacing the previous documentation-only evidence. It provides a concrete external-process startup/loading design for CL-4019403, but does not establish ordinary validated local startup while preserving relevant protections. This result concerns startup/loading only. Missing Rust callable interfaces, collision adapters and skater rendering are **subsequent build work**, not prerequisite rejection criteria.

### Pin, scope and observation

Public repository: `OGFN-Open-sourceing/FortExternalServer`, branch `season-3`, exact commit **`b45f939b612ba75ff41f38b0952410336b6b0b19`**, commit date `2026-09-16T15:17:24+02:00`; observed 2026-10-06. The formerly interrupted branch fetch succeeded in this pass. Public source was fetched, archived into a temporary directory and read using `rg`/`nl`. During this fallback source inspection, no source build, game download, private asset access, game launch, injection, authentication change or protection manipulation occurred. The separate unchanged-client probe is recorded below.

| Source | SHA256 |
| --- | --- |
| `Source/Server/Private/GameServerHost.cpp` | `ed1723c231b09893ab39462988449798985fac15b7b839fcfd26797821251567` |
| `Source/Runtime/Engine/Private/Engine/NetworkHooks.cpp` | `a4e53b6d2fea90cba3848d10b244acd230879055c9f7104e50a9e7ca88b6481b` |
| `Source/Server/Private/ServerSettings.cpp` | `882b7d2c2051fcd668f849d7ff4341068f6250f374aec895b323f9c017575f31` |

### Startup and loading dependencies

**Source-inspected:** the build profile explicitly targets Fortnite3.6/CL-4019403. It does not target the existing CL-3917250. The source profile sets engine version4.20, while the earlier pinned main README table says UE4.19; this contradiction needs resolution before using engine-specific assumptions. No client acquisition route was established. [Build profile][profile] [Earlier main documentation][main-readme]

The host finds a build folder containing `FortniteGame` and `Engine`, locates the shipping executable and either attaches to a matching running process or creates that process directly. Default configuration selects direct startup. The launch arguments contain placeholder authentication fields; that is source evidence of a launch attempt, not evidence that ordinary account/session validation succeeds. This report intentionally omits a launch command or credential procedure. [Host attach/start][host-start] [Executable/settings][settings] [Default configuration][config] [Process creation][process]

After obtaining the executable image and resolving engine objects, startup installs hooks, checks version, waits for a local player controller, travels to Athena and waits for an authoritative world. Those steps contain explicit failure returns/timeouts. Crucially, the hooks are installed **before** final version verification and before the frontend wait; there is no source-demonstrated run that first proves an untouched client can reach ordinary local gameplay. [Startup ordering][host-order] [Frontend/travel][host-travel]

The load mechanism is not a DLL: it writes generated machine-code stubs into the running game, redirects engine call sites and services them through a remote game-thread bridge. That is a concrete implementation, not merely README wording. It changes host execution despite being packaged as a separate executable. [Bridge implementation][bridge] [Network hooks][hooks]

Build dependencies are narrow: C++20, CMake3.21 or the Visual Studio project, Windows x64 and Windows system libraries (`psapi`, `ole32`, `shlwapi` in the CMake target). This inspected branch is Windows-only in CMake. No dependency installation/build was attempted, and source metadata does not prove toolchain or gameplay success. [CMake target][cmake]

### Protection-preserving gate evidence

**Source-inspected negative evidence:** startup hook installation always invokes constant overrides. When the online-session kick function is located, the source replaces it with a constant return rather than its original behavior; no configuration guard preserving it appears in that installation path. The hook set also forces listen net mode and alters control-message handling. The Beacon login handler receives a payload and directly welcomes the player while skipping the original handler. These changes require classification against the protection boundary before execution. They do not, by themselves, prove a DRM or operating-system anti-cheat bypass, nor establish that every local session-emulation change is prohibited. The concrete present gaps are a reviewed compatible client (this branch targets a different CL) and an observed working startup/loading path; no such trial was made. [Installation/overrides][hooks] [Beacon login handling][login]

An attach-to-running-process option exists, but it still proceeds through the same override installation. Its existence therefore does not, on its own, qualify a protection-preserving alternative. Removing or changing those overrides would be new code requiring its own review and successful ordinary-startup evidence; it was not done or silently assumed here. [Attach/default][config] [Startup order][host-order]

**Inference, bounded:** this source supplies a real startup/loading mechanism worth understanding, but cannot pass the selected gate on available evidence. The precise blocker is an evidenced ordinary-startup/load route for the exact client that retains relevant protections; the missing Skate adapters are not the reason for this decision. No universal impossibility, legal-clearance verdict or ban on all process extension techniques follows.

### Fallback decision

Do not start the conditional actual-Skate prototype through this fallback yet. Proceed only after the lead combines this finding with the Core review and identifies a startup/loading route that meets the owner-selected boundary. The gate needs exact-client identity/access, an inspected loading mechanism, resolved protection behavior and evidence that ordinary local startup reaches the required host state. It does **not** require the future collision/rendering/Rust adapter already to exist.

## Core primary-path review

Core remains pinned at `6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0`.
Its [README](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/README.md#L6-L9)
excludes a launcher/backend; this is missing implementation/integration work,
not a universal ban on building one. The [initialization](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/dllmain.cpp#L91-L139)
client branch does not start a world, and the server branch waits for an
already-authoritative world before its map load. [SetupDedicatedServer](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Utils.cpp#L445-L519)
early-returns in listen mode. These source facts leave bootstrap work; they
are not measured proof of incompatibility with CL-3917250.

Fresh public issue/API check: [Core issue 112](https://github.com/PongooDev/Core/issues/112)
reports a crash after landing on **CL-3915963**, not our CL-3917250. It is open,
created/updated 2026-08-16, with zero comments on the checked API response.
No launcher/backend/source revision is supplied. It is a reporter's observation,
not our gameplay evidence or a reproducible setup. The public launcher issue
search returned zero matches; that limited search does not prove no route exists.
The web issue/wiki fetch failed; GitHub's issue API succeeded. No issue comment
or outreach was sent.

## Existing-client startup experiment

**Actually executed:** ignored `probe-startup-v2.py` through native Windows Python.
It hashes the isolated shipping executable against the inherited known SHA1,
refuses an already running Fortnite process, preserves existing configuration,
starts the unchanged executable with only the five prior profile/window options,
and observes for at most twenty seconds. A surviving process would be closed by
the probe; no loader, injection, alternate account arguments or protection
modification is supplied. Source, original installation and configuration are
not edited. The script and raw diagnostic files stay private.

Result: `exited_before_20_seconds=true`, client exit `0 / 0x00000000`,
2.812 seconds; 143 stdout bytes and zero stderr bytes; executable unchanged;
zero changed original config files and zero new config files. Probe exits 1
because the client closed before the observation completed. Exit 0 from the
client does not establish gameplay success. Only a local whitelist classifier
read the output: launcher/exit terms were present; the specific condition and
cause remain unestablished. No raw log or game bytes were uploaded.

This replaces the earlier null-exit-code gap with a definite observation. It is
one fresh run consistent with the inherited early-exit observation, not a full
repeatability study or a fixed bug. No protected launcher service or third-party
host was run. No live Skate simulation, local island, collision or pose test
occurred. The prior stock BattlEye installation stall remains inherited.

## Next concrete experiment and stop condition

Investigate the existing client's launcher/startup contract through redacted
local diagnostics and reviewed source/reverse engineering. A published native
extension API is not a prerequisite. Establish which prerequisites are ordinary
startup/backend work and which, if any, actually require altering DRM/anti-cheat.
Keep the different-CL external host as a fallback; do not acquire it speculatively.
If startup/loading is established without those prohibited changes, implement
only the Rust call and real-surface collision/pose adapter needed to advance
actual Skate. Ramp edits/destruction come after that first result. If the
identified required change crosses the boundary, record that specific mechanism
and switch candidates rather than declaring all reverse engineering impossible.

The current retained-client exit is the runtime blocker. The protection effect
of the alternative's session changes is an open review question, not a proven
OS anti-cheat bypass. Complete adapter code is expressly not an entry gate.

[profile]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/FortniteGame/Private/Versioning/Season3BuildProfile.cpp#L5-L12
[main-readme]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b39f9b7a78a82b75621a4829f55d6cfafbbbb83f/README.md#L18-L22
[host-start]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Private/GameServerHost.cpp#L23-L67
[settings]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Private/ServerSettings.cpp#L6-L12
[config]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Public/Configuration.h#L3-L23
[process]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Runtime/RemoteProcess/Private/ProcessAttachment.cpp#L10-L85
[host-order]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Private/GameServerHost.cpp#L343-L381
[host-travel]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Private/GameServerHost.cpp#L241-L295
[bridge]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Runtime/RemoteProcess/Private/GameThreadBridge.cpp#L264-L281
[hooks]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Runtime/Engine/Private/Engine/NetworkHooks.cpp#L10-L150
[login]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Runtime/Engine/Private/Engine/NetworkHooks.cpp#L206-L234
[cmake]: https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/CMakeLists.txt#L1-L36
