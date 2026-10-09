# Pinned viewer qualification fixture

This authored fixture checks one approved boundary: resource bytes through the
existing GTA4Unity `CollisionDebugRenderer.RenderAll` to observable scene geometry.
It is a local qualification check for issues #39/#40, not measurement tooling or
a supported collision parser. It contains no game assets or private identities.

## Prerequisites and staging

Use an isolated checkout of GTA4Unity at
`c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`, Unity Editor
`6000.4.0f1 (8cf496087c8f)`, an eligible activated licence, a graphics-capable
session and its unchanged pinned package manifest/lock. Package resolution and
compilation must succeed before a fixture result can exist. Missing editor,
licence, packages or shader support is an unavailable qualification, not a
behavioral red result. Do not open the owned-game scene or enter Play first.

Copy [CollisionOverlayQualification.cs](Editor/CollisionOverlayQualification.cs)
and [CollisionOverlayVisibility.cs](Editor/CollisionOverlayVisibility.cs)
to the isolated upstream checkout's `Assets/CombineQualification/Editor/` folder.
The `Editor` folder lets the existing predefined editor assembly reference the
upstream runtime assembly without moving upstream code into new assemblies.
This is an executable fixture check, not an NUnit test-runner invocation.

With locally supplied absolute paths in PowerShell:

```powershell
& $unityEditor -batchmode -projectPath $viewerLab `
  -accept-apiupdate `
  -executeMethod CombineQualification.CollisionOverlayQualification.Run `
  -logFile $privateFixtureLog
$LASTEXITCODE
```

The method exits with 0 on success and 1 on failure. Do not supply `-nographics`:
the output checks require a supported material. Do not supply `-quit`: the method
owns exit. Preserve the private log and distinguish compilation/licensing errors
from a fixture assertion failure. Confirm the explicit
`COMBINE_OVERLAY_QUALIFICATION` verdict; an editor process exiting alone is not a
pass. For local visual inspection, use the menu
**Combine Qualification → Check authored collision overlay**. It leaves an
unsaved authored scene with camera/light. The interactive route prompts to save
modified scenes before replacing them; cancelling preserves the current scenes
and reports qualification unavailable. Keep any screenshot private and open
it through the existing workbench evidence command before owner acceptance.

`-accept-apiupdate` enables Unity's API migration during batch compilation; it
does not accept licence terms. The pinned Editor moved `GUID` from `UnityEditor`
to `UnityEngine`. Fresh package compilation can otherwise fail before the fixture
executes. Retain the private migration log and verify that package manifest/lock
identities remain unchanged. See [Unity's release notes](https://unity.com/releases/editor/alpha/6000.4.0a4)
and [command-line reference](https://docs.unity.com/en-us/engine/6000.7/manual/unity-editor/command-line-arguments/editor).

## Inspect the map with and without the overlay

Select the collision-only parent in the Hierarchy, then use **Combine Qualification
→ Hide selected collision overlay** for the map alone and **Show selected collision
overlay** to restore it. In the private lab use the dedicated Selected collision overlay parent;
in the authored fixture it is Authored overlay qualification. Keep the camera
fixed for both views. These commands change only `MeshRenderer.enabled`; they do
not move geometry, query ground, load resources or write game files.

Both commands refuse an absent, inactive, empty or mixed selection. Every selected
mesh renderer must follow the pinned renderer's `col_` naming contract and contain
a mesh. Select the complete parent to compare the complete resource; selecting
one child changes that child only. The commands do not independently verify a
resource's digest, completeness or active GTA collision. Use the earlier lab
coverage checks and retain private evidence. Map-only visibility is not proof
that the selected mesh covers a visible road.

The retained live trial emitted HIDDEN and SHOWN markers and produced a fixed-
camera game-view pair, opened locally. Independent visual review confirmed green
surfaces disappear and return while map landmarks stay aligned. Some foreground
approach/yard/roadside surfaces are covered; farther bridge spans are not. This
does not identify a named street or qualify ground checkpoints. See the
[location verdict](../../research/results/2026-10-10-gtaiv-viewer-location-verdict.md).

## What the fixture covers

The input is an authored Deflate RSC5 composite with two geometry children,
explicit identity child matrices, seven asymmetric vertices at several heights,
nonuniform quantization, one triangle and one quad. Expected Unity world positions
and triangle indices are literal hand-worked values. Neither expectations nor
input bytes depend on Combine's decoder or owned game data.

The check requires both active overlay renderers, supported materials, every
expected vertex at its world coordinate (absolute tolerance 0.0001 in the
authored scene) and complete face topology/winding. Empty, missing or partly
rendered fixture output fails. The fixture tolerance applies only to this
authored coordinate check; it does not choose the later GTA measurement tolerance.

The same menu-command boundary also checks hiding/restoring both children at
their literal coordinates while an unrelated renderer stays visible, and refusal
of mixed or absent selections. The visibility roundtrip failed on the missing
Hide command before implementation and passed after adding the commands.
Selection-refusal checks qualify the guard separately; no extra red/green cycle
is claimed for those checks.

A passing check establishes those scene-output behaviors only. It does not
establish visible pixels, startup overlay enablement, arbitrary child transforms,
malformed-input rejection, complete loading of a different resource, an
identifiable street or active GTA collision. Visible pixels require a separate
local camera/Scene view inspection. A later malformed-sibling case must be its
own observed red → implementation → green cycle if a change is necessary.

## Execution review

The pinned script scan found no custom `InitializeOnLoad`, `AssetPostprocessor`,
`ExecuteAlways`, explicit HTTP client or process-launch path in `Assets` scripts.
The editor build preprocess changes included shaders only when building; this
route does not build. Unity itself resolves packages from `packages.unity.com`
and manages licensing, IDE/collaboration/analytics packages and local caches;
the script scan does not independently audit those packages or Unity binaries.

The sole bundled managed plugin is SharpZipLib, SHA-256
`cfc2a838569a48d16a15269bb701de87b81b3d2bc303bb7c4c3724cc3bba0c50`.
That digest identifies the inspected bytes, not an independent security audit.
Native imports for `ragezip.dll` and `libsquish.dll` exist elsewhere; the authored
Deflate collision path does not call those imports. The fixture constructs the
loader without calling `LoadGameFiles`, uses no filesystem writes and never
enters Play. Unity still writes project caches and the supplied private log.

For a later real-map trial, bootstrap reads the owned executable for a key,
reads archives recursively and can cache a key offset in the process working
directory. Filesystem store methods can write if explicitly invoked. Keep
original installs isolated, retain keys/settings/logs outside Git and uploads,
and keep parent/bootstrap transform identity. This fixture does not authorize
that later trial before qualification or bypass the street-location gate.

## Result status

The actual CLI run verified Unity Editor `6000.4.0f1`; the pinned package
manifest and lock remained unchanged. The initial compilation attempt was
unavailable: the fixture's ambiguous `CompressionLevel` name was corrected in
`bed92c1`, and separate package GUID compilation errors were resolved during
local setup. That attempt was not a behavioral red result.

The second run emitted
`COMBINE_OVERLAY_QUALIFICATION: PASS (scene geometry; pixels unverified)`, exited
with code 0 and reported no compiler errors. This is a baseline pass of the
existing renderer through the authored fixture; no behavioral red → green
implementation cycle or existing upstream source change is claimed for that
fixture baseline.

Subsequent interactive capture confirmed both authored shapes visibly rendered.
The isolated live viewer also displayed the surrounding map and the exact
digest-verified selected collision overlay at unchanged placement, with expected
aggregate child/vertex/triangle coverage. The owner accepted the viewer appearance;
the bounded viewer qualification under #40 is complete and that ticket is closed.
These observations extend beyond the authored fixture's limited coverage and
do not qualify arbitrary resources or active GTA collision.

The [street-location investigation](../../research/results/2026-10-10-gtaiv-viewer-location-verdict.md)
ended at a precise **inconclusive** stop: the observed building/railway landmarks
do not yet establish a named junction or selected-mesh coverage of suitable road,
pavement and height-change checkpoints. Viewer appearance acceptance does not
establish street placement. No ground-measurement tooling or GTA comparison was
produced. Keep private execution logs, assets and setup details outside Git and
uploads.
