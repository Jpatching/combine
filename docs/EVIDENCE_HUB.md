# Private candidate evidence

[Workflow #61](https://github.com/Jpatching/combine/issues/61) groups the retained
riding, non-flat ground and collector work into one candidate. The hub shows
criteria, blockers, attempts and registered private clips. Approval stays in chat
and names the candidate revision.

## Start

The local game commands share a reviewed private configuration:

```sh
python3 scripts/workbench.py gta open
python3 scripts/workbench.py gta status
python3 scripts/workbench.py gta recover
python3 scripts/workbench.py gta test --scenario mount-diagnostic
python3 scripts/workbench.py gta test --scenario ride-proof
```

`.private/evidence-hub/gta.json` holds `state`, `inspection`, `window_mode`,
`manifest` and `runtime_config` paths; relative paths resolve beside that file.
Opening uses the pinned isolated runtime and requests foreground once. Recovery
tries normal close first. A successful launch creates a fresh immutable session
and updates the private runtime pointer; it does not establish gameplay readiness.
Missing session configuration permits opening but refuses testing. Test requests
default to one attempt; `--request-id <UUID>` makes reconnect/retry idempotent.
An active or unresolved diagnostic blocks launch/recovery.
Launch/recovery and diagnostic claims share an atomic runtime-operation lease;
interrupted helpers retain private process records and block reuse until reconciled.

If normal close fails, the default preserves the process. Only explicit owner
approval permits `gta recover --allow-hung-termination`: it verifies the exact
unresponsive process/start/executable, retains its process handle, records the
action privately and confirms exit before relaunch. Unsaved progress may be lost.
This option is local only; the hub cannot request termination or launch.

Manifest preparation verifies reviewed staged `Items.SourceHash` for replaced
files and the retained `Hashes` for baseline files. Rollback hashes do not describe
the active staged bytes. Independent changes, contradictory retained overrides
and unsafe relative paths refuse. `prepare-session.ps1 -InventoryOnly` verifies
files without claiming process loading or gameplay.

Agent staging uses `tools/workbench/stage.ps1 -Plan <reviewed-private-bundle>
-Output <new-private-manifest>` only with GTA closed. It accepts the eight fixed
adapter/helper roles, verifies source digests and the signed pinned baseline,
backs up existing files, atomically replaces owned targets and records rollback.
It cannot launch GTA, alter saves/assets or accept an unrelated runtime target.
The private manifest pins the exact source revision and checkpoint token; the
next launch creates a fresh process-bound session. Preserve failed transactions.

```sh
python3 scripts/evidence_hub.py serve
python3 scripts/evidence_hub.py work --config .private/evidence-hub/runtime.json
```

Run these in separate retained terminals. Storage defaults to
`.private/evidence-hub/`; `--state <private-directory>` before the subcommand
selects another store. Missing runtime configuration records a refusal without input.
Requests persist before execution. One batch runs at a time; a claimed batch is
never replayed after interruption. Stop prevents the next attempt while the active
attempt completes owned-input release/recovery. Unverified recovery blocks all work.
Reconcile the retained child/game transaction before continuing; the page has no
recovery override. Two unchanged failures stop the scenario; the agent records a
new experimental variable before requesting another diagnostic.

## Runtime configuration

Use `tools/workbench/prepare-session.ps1 -Manifest <reviewed-manifest> -Output
<new-private-session>` with the retained staging manifest. It checks current
process and retained hashes without changing the game or sending input. Existing
session files are preserved. Inventory matching does not establish loaded-memory
provenance, ground availability or an intended collision layer.

Private `runtime.json` fields:

| Field | Meaning |
| --- | --- |
| `source_checkout` | Absolute path to the clean reviewed retained source |
| `source_revision` | Full revision verified before the trial |
| `session` | Absolute private session JSON path |
| `session_sha256` | Exact session digest |
| `changed_variable` | Diagnostic variable changed for this experiment |
| `checkpoints` | Qualified private checkpoint JSON; required only for ground collection |

This is reviewed local execution configuration, separate from catalogue recipes.
The page accepts scenario IDs and counts, never commands, paths, installation,
downloads, restarts or merges. Keep configuration, coordinates, identities, logs
and media outside Git and AI uploads.

- `preflight`: inventory, process/start identity, captioned window, foreground,
  fresh gameplay, unmounted adapter, selected input and ordinary player control.
- `offline-menus`: selected-window local capture/OCR; one owned Enter pulse only
  for the existing offline title/start menus. Stale, unknown, online, login and
  loading screens refuse input. Input delivery does not prove gameplay readiness.
- `mount-diagnostic`: selected-window recording and guarded F6, first mount/query
  boundary, ordinary GTA recovery. Non-finite querying and the flat route's 5 cm
  refusal remain distinct. A pending preparation timeout blocks further input.
- `ground-query`: existing collector with its complete independent qualification
  and recovery requirements; unavailable loading/layer witnesses stay unknown.

Input checks foreground/process/start identity immediately before key-down,
refuses held keys and releases only accepted owned presses. Pending native
children are retained rather than killed between key-down and key-up. The hub
cannot steal focus or launch/restart a game. Capture requires the pinned local
Universal Modder checkout and existing Windows ffmpeg. MP4 remux verifies unchanged
frame counts before registering evidence.

Preparation failure, timeout, cancellation and changed-floor notifications are
terminal diagnostic results. If cleanup cannot be verified, the attempt remains
blocked on recovery and retains the preceding verdict/boundary/reason in
`diagnostic`; the page shows that original diagnostic separately. Neither a
timeout nor a prior owner-observed mount clears a recovery block.

## Tailscale

```sh
python3 scripts/evidence_hub.py serve --origin https://machine.tailnet.ts.net --owner owner@example.com
tailscale serve --bg --https=443 http://127.0.0.1:8765
```

Use the machine's actual private DNS name and owner login. The app binds only to
loopback. Tailscale Serve supplies identity headers; the hub checks exact host/login,
same-origin writes and a per-server request token. Only registered media IDs are
served, with seeking support; changed media is refused. There is no file browser
or upload route. Restrict tailnet access to the owner and use Serve, never Funnel.

## Evidence and verification

`candidate <private-json>` updates displayed source checks, criteria, blockers and
next experiment; it cannot approve a merge. `import <private-json>` registers a
reviewed attempt and its media locally. Imported records declare `scenario`,
`verdict`, `boundary`, `reason`, `changed_variable`, `cleanup`, `source_revision`,
`runtime_identity`, `limitations` and a `media` array of private paths. They never
execute game actions. `status` reads persistent records locally.

Run `python3 scripts/verify.py` and `python3 tools/gtaiv-skate/check.py`.
HTTP/command tests use authored media. `work --once --authored-results <fixture-json>`
exercises batching without a game and labels every result authored. These fixtures
cannot establish runtime/gameplay acceptance. Windows syntax, compiled key refusal,
menu categories, actual capture/cleanup and phone access need their own checks.

## One ride proof and retained recovery

`gta test --scenario ride-proof` uses the installed opt-in evaluation script,
definitions and plugin. It observes the actual mounted Session, sends F8 for
bounded push/both-steering/camera observations, dismounts with F6, then observes
owned-camera destruction and normal GTA walking with F9 and a fixed guarded W
hold. Every key binds to the verified windowed foreground process. Results do
not establish physical-controller delivery, visual scale/orientation acceptance,
all-floor coverage or owner acceptance. Capture remains private.

After independently restored ordinary GTA control, use the local-only command
`gta reconcile --request-id <blocked-batch-uuid>` with the reviewed local config.
The named batch remains locked while its original immutable session digest is
matched to the recorded attempts and every owned key is independently released.
If that exact original PID/start is absent or its PID was reused, recovery is
recorded as `original-session-exited`; this makes no claim about any current GTA process
and does not require the obsolete inventory to remain installed. A live original
process still requires exact runtime inventory and fresh foreground normal control. Any
retained pending helper marker refuses reconciliation. A successful observation
records reconciliation separately; original attempts and failure reasons remain.
There is no HTTP recovery override or game input during reconciliation. Missing original-session binding or interrupted verification preserves the block.
Reconciliation never makes an independently changed installed script valid for a
new trial; installed-source matching and new session preparation remain required.

When the owner is present and explicitly opts out of recording, the private runtime
configuration may set `record_video` to `false`. Native trial identity, foreground,
input and recovery checks still apply. The result identifies owner observation
and omitted video; acceptance remains an explicit owner decision. Recording stays
enabled by default. Offline-menu classification still requires a private screenshot.
