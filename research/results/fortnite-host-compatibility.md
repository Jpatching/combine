# Fortnite host compatibility references

These are source findings and retained observations from October 2026, not a
selected working setup. [Startup qualification #6](https://github.com/Jpatching/combine/issues/6)
owns candidate selection; [#5](https://github.com/Jpatching/combine/issues/5)
owns usable startup and [#4](https://github.com/Jpatching/combine/issues/4)
owns the Skate first proof. The [interactive-world contract](../../docs/FORTNITE_SKATE.md)
and ADR own the desired behavior. Historical candidate ordering does not select work.

The original [input diagnosis](https://github.com/Jpatching/combine/blob/04aadeb84c16770c49cb95a9a2cd246c9800af4e/research/results/2026-10-06-fortnite-input-diagnosis.md)
and [startup qualification](https://github.com/Jpatching/combine/blob/04aadeb84c16770c49cb95a9a2cd246c9800af4e/research/results/2026-10-07-local-fortnite-host-qualification.md)
retain the observation context in Git history.

## Retained client observations

- **3.1 CL3917250:** inherited shipping SHA-1
  `b017f433b1238c0eed9f43fdb80df3ea1d90361e`. The unmodified stock protected
  launcher stopped at BattlEye installation. A later unchanged shipping-client
  probe exited after 2.812 seconds with exit code 0; gameplay did not start and
  the initiating cause remains unknown. `LauncherCheck` in shutdown output is
  not a diagnosed launcher-check failure. Neither observation proves the other
  route is required or the client universally incompatible.
- **3.1 inventory:** ten freshly hash-matched game containers had valid
  version-4 footers with encrypted-index flags. CUE4Parse at
  `e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc` skipped them without a supplied
  key/custom handler: 0/10 mounted, no world or collision export. This establishes
  the header flag and parser policy, not the payload encryption algorithm or
  a general corruption finding. Changing UE4_19/UE4_20 did not alter that result.
- **12.41 CL12905909:** rejected before execution. The shipping executable
  matched manifest size but failed SHA-1 comparison and Windows Authenticode
  returned `HashMismatch`. Expected SHA-1
  `88e69fa47c475d76b6963a470b0b5bb21d1c3cb2`; observed
  `3b390bf9d1e72b4b0ab7cfd1bc5c807d47a10c91`. The exact-build comparison
  [manifest](https://github.com/VastBlast/FortniteManifestArchive/blob/b228ac917383377dec99f29e88c7f1394b141d16/Fortnite/Windows/jTfg_xZZ2H4T9L__PEmzI2Y90hr9Aw.manifest)
  is community archived, not independently authenticated publisher provenance.
  Remaining archive contents were not fully verified; no malware cause is claimed.

Private logs, paths, profiles and game bytes remain local. These observations are
historical evidence, not a fresh integrity or startup check.

## Inspected host dependencies

**Core**, `6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0`, is an in-process gameserver
DLL; its [README](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/README.md)
excludes Fortnite files, launcher and backend. The
[client branch](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Client.cpp#L23-L81)
creates console/CheatManager behavior, not a world. The
[server branch](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/dllmain.cpp#L92-L139)
waits for an already authoritative non-Frontend world before `LoadWorld`;
[listen mode](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Core/Private/Utils.cpp#L445-L519)
skips dedicated bootstrap. Flags or compilation therefore do not demonstrate
self-starting local gameplay. Whole-DLL loading is unselected: its inspected
[player validation](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/FortniteGame/Private/FortGameSession.cpp#L4-L24),
[challenge handling](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/Engine/Source/Runtime/Engine/Private/NetConnection.cpp#L84-L106)
and [MCP credentials](https://github.com/PongooDev/Core/blob/6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0/Core/FortniteGame/Private/Mcp/McpProfileGroup.cpp#L4-L14)
change normal validation/credential behavior. These are concrete source findings,
not proof of an operating-system anti-cheat bypass.

**Reboot**, server `3f6417ee6b07063bb6f83902ad3971f998888bab`, has
[server building/edit handlers](https://github.com/Milxnor/Project-Reboot-3.0/blob/3f6417ee6b07063bb6f83902ad3971f998888bab/Project%20Reboot%203.0/FortPlayerController.cpp).
Its inspected [launcher](https://github.com/Milxnor/Reboot-Launcher/blob/64dc971da499f1856f40af992d0068c5801e344b/gui/lib/src/widget/game/game_start_button.dart#L211)
starts/suspends EAC. That route is rejected under the project boundary; server
handlers do not supply a Skate rendering-client adapter. Historical
[Era launch source](https://github.com/EraFNOrg/Era-Launcher/blob/e7d48de4ba652df3efef50c25698ef43549d5d10/EraLauncher/Home.xaml.cs#L292-L310)
likewise requests protection-disabling behavior and substitute authentication;
this does not qualify or condemn unrelated current Era distributions.

**FortExternalServer**, season-3 `b45f939b612ba75ff41f38b0952410336b6b0b19`,
[targets CL4019403](https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/FortniteGame/Private/Versioning/Season3BuildProfile.cpp#L5-L12),
not CL3917250. Its profile says UE4.20 while the earlier main README says UE4.19.
Its [startup](https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Server/Private/GameServerHost.cpp#L343-L381)
installs remote game-thread hooks before final version verification. The
[hook set](https://github.com/OGFN-Open-sourceing/FortExternalServer/blob/b45f939b612ba75ff41f38b0952410336b6b0b19/Source/Runtime/Engine/Private/Engine/NetworkHooks.cpp#L10-L150)
changes session/control-message behavior. Compatible-client startup and the
protection effect of those changes remain unqualified; no trial ran.

## Existing Skate and official-tool boundary

The pinned [Skate Session](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs)
provides controls/ticks, solved pose/camera and triangle/rail collision replacement.
Its [crate](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/Cargo.toml)
does not declare a stable C ABI; C++ hosts cannot directly call its Rust types.
A narrow same-process wrapper remains implementation work, not a selected generic
bridge. Ray contacts or server building handlers alone do not supply current
Skate collision, client movement ownership or rendered solved bones.

The October 6 inspected [UEFN/UE comparison](https://dev.epicgames.com/documentation/en-us/fortnite/uefn-vs-ue-in-unreal-editor-for-fortnite),
[Verse WebAPI](https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/unrealenginedotcom/webapi)
and [UEFN MCP](https://dev.epicgames.com/documentation/fortnite/uefn-mcp)
did not establish a creator native-library call path or a connection to the
player's local Skate Session. Editor automation is a different execution context.
These pages move: recheck them against an actual selected build before relying on
them. The finding is bounded missing evidence, not universal impossibility.

Usable exact-client startup and reviewed native execution are the entry gate.
Missing collision/rendering/FFI adapter code is subsequent prototype work;
a complete finished adapter is not required before beginning an authorized experiment.
