# Windows game testing: repositories and practical improvements

Researched 2026-10-12 for the owner-approved GTA IV evidence workflow. This
refreshes [the previous comparison](2026-10-11-gtaiv-windowed-iteration-tools.md).
Primary public repositories/docs were reopened; local source inspection used
`integration/gtaiv-evidence-loop` at starting revision
`844fcdad69be245c4a8df9c36a6c1f1019599d5f`, with existing candidate changes preserved.
No installation, game control, private media inspection or runtime qualification
was performed by this researcher. Recommendations below are engineering judgments.

## Finding

**The strongest improvement is a shorter, state-driven native mount loop using
the existing runner, retained checkpoint and private capture.** A general desktop
MCP does not supply GTA collision facts. Add a local visual assertion only if
menu navigation is the measured bottleneck; add frame telemetry only if a freeze
is the measured bottleneck. No evidence supports replacing the integration with
a broad automation framework.

The candidate already contains exact-process/session checks, bounded owned input,
native status, retained attempts, selected-window capture, local Windows OCR and
ground collection. Its live evaluation script also measures movement, heading,
camera and post-dismount restoration with expiring input playback. These are
verified source capabilities, separate from live qualification and owner acceptance.
[Evidence hub](../../docs/EVIDENCE_HUB.md),
[adapter evaluation](../../tools/gtaiv-skate/README.md),
[local OCR implementation](../../tools/workbench/menu.ps1).

## Ranked fit

Rank reflects this project's next experiment, not a universal popularity list.
Setup estimates are judgments. Public rounded stars observed on the research date:
AutoHotkey 13.3k, Airtest 9.6k, Windows-MCP 8.7k, pywinauto 6.2k and PresentMon
2.6k, on their linked repository pages below. Popularity does not establish GTA
compatibility or maintenance quality.

| Priority / repository | What it contributes | Friction, licence and project decision |
| --- | --- | --- |
| 1. Existing adapter + [Universal Modder](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/game-automation/SKILL.md) | Fixed window, repeatable scene, process-window GPU capture, relative mouse and scan-code input. | Reviewed pin already used by capture. [MIT](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/LICENSE). Reuse capture; preserve our runner for input. Its [Python Drive](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/um/win.py) refocuses/retries foreground errors, conflicting with our test refusal policy. |
| 2. [Airtest](https://github.com/AirtestProject/Airtest) | Windows image-template assertions, Python/CLI scenarios and local reports without game-engine injection. | Medium: separate Python dependencies and private templates. Apache-2.0. Best optional menu-test candidate. Existing OCR may make it unnecessary. No local GTA qualification. |
| 3. [PresentMon](https://github.com/GameTechDev/PresentMon) | Process-targeted presented-frame timing/CSV; useful for separating rendering stalls from input/state failures. | Low–medium: Windows binary and ETW permissions. MIT. Optional freeze observer; frames do not prove gameplay or collision. No local qualification. |
| 4. [pywinauto](https://github.com/pywinauto/pywinauto) | Win32/UI Automation controls and waits for ordinary launcher/dialog automation. | Low–medium Python setup, BSD-3-Clause. Inspect actual controls first. No demonstrated GTA rendered-menu hierarchy; not a collision observer. Airtest already uses it in its Windows backend. |
| 5. [Windows-MCP](https://github.com/CursorTouch/Windows-MCP) | Agent-facing desktop/window tools, UI Automation snapshots and tool allowlists. | Medium Windows-side MCP/client setup, MIT. Author explicitly excludes playing video games. Candidate for surrounding dialogs only. No callable Windows-MCP tool exposed in this research session. |
| 6. [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey) | Small opt-in keyboard/mouse macros. | Low runtime setup, GPL-2.0. Duplicates the guarded runner and provides no native pass/fail signal. Consider only a missing operator shortcut; use v2, since v1 is unmaintained. |
| Reference. [CLEO Redux](https://re.cleo.li/docs/en/introduction.html) | Supported GTA IV Complete Edition 1.2.0.59 script runtime. [Script restart on edits](https://re.cleo.li/docs/en/other-features.html) can shorten diagnostic iteration. | Already selected; [EULA](https://re.cleo.li/docs/en/introduction.html#license), not assumed MIT. Qualify harmless dismounted script restart/cleanup separately. [Native plugins load at startup](https://re.cleo.li/docs/en/using-sdk.html); script reload does not authorize DLL replacement in a running game. |
| Defer. [REA](https://github.com/morluto/rea) | Structured read-only binary investigation when a source/native contract cannot otherwise be resolved. | High provider setup; MIT repository. [Pinned Windows provider](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/docs/windows-ghidra-p0.md) requires Ghidra/JDK and distinguishes main's x86 support from published packages through 5.0.0. No callable REA MCP or Windows provider qualification established here. |
| Exclude. [Poco](https://github.com/AirtestProject/Poco) | Engine UI hierarchy through an integrated SDK. | Apache-2.0; high custom-engine integration cost. Listed engines include Unity/cocos, with no documented GTA IV/RAGE driver. It is not a drop-in hierarchy inspector for this game. |
| Exclude. [IV-SDK .NET](https://github.com/ClonkAndre/IV-SDK-DotNet) | GTA IV .NET scripting. | GPL-3.0; author limits support to 1.0.7.0/1.0.8.0. Incompatible with selected 1.2.0.59; no downgrade proposed. |

Maintenance signals: reopened release lists label Airtest v1.4.3, pywinauto 0.6.9,
Windows-MCP v0.8.8 and AutoHotkey v2.0.30 as latest. These are observations,
not adoption pins or proof of ongoing support; date rendering omitted years on
several pages, so no inferred release dates are recorded.
[Airtest releases](https://github.com/AirtestProject/Airtest/releases),
[pywinauto releases](https://github.com/pywinauto/pywinauto/releases),
[Windows-MCP releases](https://github.com/CursorTouch/Windows-MCP/releases),
[AutoHotkey releases](https://github.com/AutoHotkey/AutoHotkey/releases).

## Tricks with a sharper signal

- **Wait on state instead of sleeping.** Bound waits on fresh native status and
  process identity. Assert the exact mount refusal/success boundary and verified
  recovery, rather than successful F6 delivery or a responsive window. Existing
  readiness/watch commands are the starting point.
  [Adapter](../../tools/gtaiv-skate/README.md).
- **Restore a repeatable starting point.** Use the retained isolated save and
  approved checkpoint helper; preserve originals. A checkpoint is scene setup,
  not a full process-memory snapshot, deterministic traffic simulation or proof
  that collision is loaded. Record setup time separately from mount time.
  [Existing checkpoint tooling](2026-10-10-gtaiv-checkpoint-tooling.md).
- **Shrink before broadening.** Start with one checkpoint, one mount request and
  the first failed native boundary. Do not run all-point collection or a long
  riding sequence until this signal is usable. Stop after two unchanged failures;
  the next trial changes one declared variable.
  [Current workflow](../../docs/EVIDENCE_HUB.md).
- **Replay at the real boundary.** Capture private native observations locally,
  then build source-safe authored fixtures for decoding/return contracts and
  recovery transitions. Compare old/new handling with the same fixture and a
  matched live probe. A fixture can prove adapter behavior; it cannot reproduce
  proprietary CLEO return handling or qualify street support.
  [Existing definition qualification](../../tools/gtaiv-skate/README.md).
- **Pair visual and native assertions.** For menus, use a fixed client size and
  local OCR/template classification with explicit unknown/refusal. For riding,
  combine native displacement/heading/camera-restoration verdicts with private
  owner-viewed video. A screenshot match alone cannot establish mounting/contact.
  [Airtest assertion API](https://airtest.readthedocs.io/en/latest/all_module/airtest.core.api.html),
  [existing live observer](../../tools/gtaiv-skate/tests/live-evaluation.js).
- **Do not confuse recorded frames with progress.** Airtest's Windows recorder
  caps capture at 10 fps and documents repeating the last frame after a crash;
  its MSS desktop-region capture also needs occlusion/DPI qualification. Keep
  the current selected-window GPU capture for riding evidence.
  [Windows source](https://github.com/AirtestProject/Airtest/blob/master/airtest/core/win/win.py).
- **Observe frame events for a freeze.** PresentMon supports exact PID, bounded
  timed capture and process-exit termination. Align its private timing with
  native status; ongoing presents can coexist with stalled gameplay. Use only
  after capture overhead and no-input baseline are measured.
  [Console options](https://github.com/GameTechDev/PresentMon/blob/main/README-ConsoleApplication.md).

For better agent context, return approved fixed classifications, first failed
boundary, recovery verdict, source identity, elapsed duration and declared changed
variable. Keep raw coordinates, private identities/settings/logs and all game
media local. Windows-MCP screenshots or vision snapshots would expose media to
the client; they are outside this project's AI-upload boundary. If desktop-only
use is later selected, restrict its tools and disable default anonymous telemetry.
[Author controls](https://github.com/CursorTouch/Windows-MCP),
[project evidence boundary](../../docs/EVIDENCE_HUB.md).

## Smallest next experiment and limits

Run the existing `mount-diagnostic` once from the retained checkpoint in a
verified visible windowed session. Record preparation, native verdict,
restoration and total duration separately; retain its private clip. Repeat only
to establish the same exact failure, stopping at two unchanged failures. This
provides the timing and boundary needed to choose the next diagnostic variable.

Only if menu preparation dominates, qualify one local visual menu case against
the existing OCR classifications: known offline menu, unknown/loading screen,
wrong process, obscured window, focus loss and interrupted owned-key cleanup.
Keep runner input and native verdicts authoritative. Only if freezes dominate,
qualify a bounded PresentMon observation before the next input trial. No installs
or broader framework are necessary to run the first experiment.

Still unknown: exact current runtime failure, collision loading/layer validity,
new tools' local capture/input behavior and measured time savings. This report
does not establish a mount root cause, live red-capable loop, gameplay acceptance,
runtime launch or release. Source licences grant no game-asset/publisher rights;
no protection bypass, asset upload or downgrade is proposed.
