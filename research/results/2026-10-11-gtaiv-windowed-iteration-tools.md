# GTA IV windowed testing and iteration tools

Research date: 2026-10-11. Question: which existing tools can shorten the live
GTA–Skate feedback loop, and improve agent understanding without replacing the
current integration? This is public-source research and a bounded local source
review. Windows-MCP and Airtest upstream documentation/source were refreshed on
the research date; their moving main/master links are not adoption pins.
No tool installation, runtime modification or gameplay trial was performed for
this report.

## Finding

**The useful capabilities already exist. Reuse the retained collector and native
status observer first; qualify script reload and process-window recording only
where they remove measured friction.** No evidence currently justifies a new
general bridge, API or testing framework. Broader desktop control and local visual
scenarios are credible additions if menu/recovery work becomes the measured
bottleneck. This is a recommendation, not a measured speed improvement or proof
of physical support.

The owner requires GTA IV to stay windowed during testing. A predictable client
size and a visible, unminimized window help repeatable capture and menu handling.
Windowed mode alone does not establish foreground focus, gameplay readiness or
loaded collision. Universal Modder's reviewed guide recommends fixed windowed
dimensions and says its GPU window capture cannot capture minimized windows.
[Reviewed game-automation guide](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/game-automation/SKILL.md).

## Existing capabilities and limits

| Capability | Verified source support | Local qualification and decision |
| --- | --- | --- |
| CLEO Redux script reload | Official docs describe automatic restart when an active script changes; adding/deleting scripts starts/stops them. GTA IV Complete Edition 1.2.0.59 is supported. [Features](https://re.cleo.li/docs/en/other-features.html), [lifecycle](https://re.cleo.li/docs/en/script-lifecycle.html), [supported releases](https://re.cleo.li/docs/en/introduction.html) | Not tested here against the retained runtime. Qualify only a harmless dismounted diagnostic edit, including cleanup and unchanged native plugin identity. Script restart is not native plugin reload. |
| Tracing and editor definitions | CLEO offers generated command typings and `CLEO.debug.trace(true/false)`. Opcode logging can impair performance. [Features](https://re.cleo.li/docs/en/other-features.html) | Use short targeted traces when a command boundary is unknown; disable before comparing timing. Keep raw traces private. |
| Native custom commands | CLEO's C++/Rust SDK supports custom commands. `.cleo` DLLs are scanned and loaded at startup. [SDK](https://re.cleo.li/docs/en/using-sdk.html) | Our retained plugin already supplies the integration boundary. Preserve normal shutdown/restart for native replacement; documented script reload provides no promise of safe DLL hot replacement. |
| Automated collection | The retained collector checks run/readiness/artifact identity, sends a guarded F8 pulse, retains every attempt, compares readings, checks restoration and records timing. [Collector at a1e456c](https://github.com/Jpatching/combine/blob/a1e456cebcebdbc2b3a59033edfbc4629db0f0ab/tools/gtaiv-collision/README.md) | Reuse its existing checkout. It is absent from this synchronized-main research base; do not recreate or merge it through this report. It cannot independently qualify loading or layer witnesses. |
| Structured game observation | Retained native status publishes compact readiness/control/mount labels, refuses stale or mismatched-process evidence, and supports read-only wait/watch commands. [Adapter at 45d409a](https://github.com/Jpatching/combine/blob/45d409a1b6e8bb72d6f5361355c44c58228892c4/tools/gtaiv-skate/README.md) | Best existing agent-facing observation route. Readiness is separate from surface correctness and visible board/rider behavior. |
| Window recording and input | Universal Modder supplies process/window selection, GPU `gfxcapture`, process-only audio and Windows input helpers. [Reviewed win.py](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/um/win.py) | Not runtime-qualified in this research. Its Python `Drive.cmd` automatically refocuses/retries after foreground errors: do not substitute this for the collector's focus-loss refusal. Recording requires a drawing, unminimized window and compatible local setup. |
| Windows-MCP desktop bridge | CursorTouch's existing MCP server offers UI Automation snapshots, window move/resize/switch, mouse/keyboard actions, screenshots and tool allowlists. It must execute on Windows, including when invoked from WSL. Its README explicitly excludes playing video games. [Current author README](https://github.com/CursorTouch/Windows-MCP) | No callable connection or GTA qualification here. Useful candidate for ordinary Windows dialogs and surrounding desktop recovery; GTA menu effectiveness remains unproven. Retain the game runner's exact-process, foreground, bounded-input and key-release guards. |
| Airtest local visual scenarios | Existing game/app framework supports Windows application selection, image matching/assertions and CLI/Python runs. Its Windows backend provides scan-code press/release and MSS capture with fallback. [Author README](https://github.com/AirtestProject/Airtest), [Windows source](https://raw.githubusercontent.com/AirtestProject/Airtest/master/airtest/core/win/win.py) | No callable MCP connection or GTA qualification here; Airtest is a local scenario framework, not a supplied desktop MCP. Candidate for repeated menu/visible-transition tests with private local templates, screenshots and reports. Add the existing process/focus/freshness guards and cleanup; successful input calls or image matches do not establish contact state. |
| REA investigation | Reviewed REA supports artifact analysis with provider prerequisites; its process-capture documentation excludes new native Windows PTY captures. [Windows provider](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/docs/windows-ghidra-p0.md), [process capture](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/docs/process-capture.md) | Installed CLI and authored JavaScript-fixture analysis are recorded in the workbench. They do not prove Windows native-provider readiness or an active MCP connection. Use source inspection first. |
| IV-SDK .NET | The author's README restricts support to GTA IV 1.0.7.0 and 1.0.8.0. [Author repository](https://github.com/ClonkAndre/IV-SDK-DotNet) | Exclude from the pinned 1.2.0.59 experiment. No downgrade or migration is proposed. |

The active tool inventory inspected in this research exposed no callable REA,
Windows desktop-control or Airtest MCP tool. That is an availability observation
for this session, not proof that these integrations do not exist. The
[earlier helper comparison](2026-10-08-gtaiv-runtime-helper-alternatives.md)
already examines Windows-MCP, Airtest and debugger candidates. The refreshed
sources above establish that the desktop and visual bridges exist today; they
could reduce navigation and repeated visual-check friction, while authoritative
GTA contact/layer evidence still requires the game-specific diagnostic.

If navigation is the observed bottleneck, qualify a narrowly selected
Windows-MCP tool set against ordinary Windows window/dialog handling first.
Use local transport, disable its documented default anonymous telemetry, and
exclude screenshots and vision-enabled snapshots of private game content from
model-facing calls. UI snapshots can also expose private text, so review what is
returned. Its best-effort user-takeover mechanism does not replace game-specific
input guards. [Current author controls and limitations](https://github.com/CursorTouch/Windows-MCP).

If maintaining repeated visual scenarios is the bottleneck, qualify one Airtest
case locally against the existing runner: identical starting state, accepted
actions, expected visual transition, foreground-loss cleanup and native verdict.
MSS desktop-region capture is not Universal Modder's process-window GPU capture;
test occlusion and rendering compatibility rather than assuming equivalent
frames. Export only approved fixed classifications to the agent. Keep recording
with the already reviewed process-window route until a replacement proves useful.
[Current Windows implementation](https://raw.githubusercontent.com/AirtestProject/Airtest/master/airtest/core/win/win.py).

Local OCR may help classify menus, but the retained adapter explicitly treats it
as supplemental. Keep classifications separate from native state, and review
their exact local implementation before use. No new OCR accuracy or capture
success was established here.

## Efficient next experiment

1. Keep the isolated GTA runtime windowed, visible and unminimized. Confirm the
   exact process, fresh on-foot status, focus and matching prepared artifacts.
2. At one already-confirmed checkpoint, use the prepared physical-state
   diagnostic without transferring ownership to Skate. Establish whether the
   observations independently identify loaded support on the intended layer.
   Standing, flags or height agreement alone remain insufficient.
3. If the method qualifies, resolve it explicitly under
   [ground qualification #39](https://github.com/Jpatching/combine/issues/39), then
   reuse collector #58 for all four checkpoints. Require three valid readings
   each, at most 2 cm spread and 5 cm mesh error. Keep ambiguous witnesses unknown.
4. Repeat compatible collections in the same run. If native plugin bytes must
   change, perform the existing backed-up normal restart procedure. Qualify any
   script-only reload separately before relying on it to shorten repeats.
5. Record the first failed boundary and retain the attempt. Compare the same
   scenario's preflight, observation, restoration, total duration and restart
   count against a separately timed previous procedure. Only then claim savings.

The approach follows a concrete upstream modding pattern: repeatable scene,
bounded actions, real-game observations and a thin structured observer. Universal
Modder demonstrates that pattern; it does not establish how quickly modders
generally iterate, or that AI has independently verified our gameplay.
[Automation guide](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/game-automation/SKILL.md).

Send the agent approved fixed labels and source-safe outcomes. Keep exact
coordinates, assets, private settings/logs, screenshots and recordings local;
open actual media for owner review with the existing
[workbench](../../docs/WORKBENCH.md). A model-facing screenshot tool would upload
the image to the client and does not satisfy the existing local-media boundary.

## Evidence and unresolved questions

The coordinating session supplied prior retained-branch results: 12 authored
collector tests, 79 root tests and 70 document checks passed; candidate/recovery
artifact hashes matched. Its latest read-only Windows process check found one
responding GTA process, minimized and not foreground. These are reported prior
checks, not tests rerun by this researcher or confirmation of current gameplay.

Still unknown: independent contact/loading/layer validity, live script-reload
cleanup, process-window recording quality, OCR accuracy, end-to-end time savings,
and owner gameplay acceptance. The next skating boundary remains #39, then the
qualified riding trial #54; board/rider work remains separate. The user's
windowed preference does not change those verdicts.

Source verification on `research/gtaiv-windowed-iteration`: `python3
scripts/verify.py` passed 62 tests and 60 document/context checks; `git diff
--check` passed. Independent Standards and Spec reviews reported zero actionable
findings. Spec review did not independently refresh the REA URLs after they failed
to open; those claims rely on the researcher's reviewed pinned public sources.
These checks do not establish runtime window mode, hot reload or gameplay.
