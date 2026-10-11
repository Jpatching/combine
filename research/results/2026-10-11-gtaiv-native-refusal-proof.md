# Native surface preparation and refusal proof

Reviewed: 2026-10-11

The owner resumed [spec #52](https://github.com/Jpatching/combine/issues/52)
through `implement-spec` and `implement`. The ready source follow-up belongs to
[#53](https://github.com/Jpatching/combine/issues/53), retaining
[draft #57](https://github.com/Jpatching/combine/pull/57). Its fixed starting
revision is `4677e1616b8d41e218f08bdbf13139b73f3ab45d`.
Executed source candidate: `ff1ae268df8dc5a7013ab5824d5a087d2741bc04`.

The existing related local harness changes were preserved and completed through
verification. They extend the approved public Session ABI checks; no adapter
implementation changed and no new red/green implementation claim is made.
Before this follow-up, the native harness covered unavailable and wrong-layer
observations. It now also checks missing/incomplete geometry without pose exposure
or partial-preparation reuse, ground disagreement above 5 cm, query-position
mismatch and stale time. Every riding refusal is followed by stop, pose clearing
and a successful remount. Both backends still exercise 90 push ticks across
distinct authored ramp heights and height following.

Spec review found that repeating an incomplete mount could not distinguish
consumed upload state from retained incomplete state. The corrected harness
also requires another vertex to refuse without a fresh preparation start, then
checks fresh-upload recovery. This closes a test-evidence gap; the existing
implementation already consumed failed preparation. Standards review also
corrected the handoff's source branch before publication to the retained PR.

## Executed checks

Both x86 Windows harnesses were freshly linked with C++17, static runtime linking
and `-Wall -Wextra -Werror`. The in-process harness used the retained optimized
library with all eight adapter Rust source files matching the candidate. The
worker library and executable were rebuilt together from the current copied
adapter and retained pinned upstream source using:

```sh
cargo build --locked --offline --manifest-path <isolated>/adapter/Cargo.toml \
  --target i686-pc-windows-gnu --features worker --release
```

The fresh harness source SHA-256 is
`006b13ddffc4edc7dd90ce79673e7b8fda092b6beee614c8433c3a1374d3f86f`.
After the review correction, both harnesses were freshly relinked against the
unchanged source-matched libraries and rerun in new isolated directories.
Compiler packages were restored from Ubuntu's package metadata into temporary
storage, without a system installation. All builds, asset pointers and logs
remain private. A reviewed bounded PowerShell runner retained the exact owned
process handle, refused log overwrite and supplied timeout cleanup. Its initial
unsigned-script refusal occurred before native launch; process-scoped execution
policy permitted the reviewed runner without persistent policy changes.

| Explicit backend | Native exit | Harness duration | Maximum measured mount/poll/tick call |
| --- | --- | --- | --- |
| `--worker` | 0 | 49.445 s | 1.027 ms |
| `--in-process` | 0 | 198.778 s | 19,751.443 ms |

Both passed the complete preparation, movement, five fault cases and recovery
checks, including the corrected consumed-upload assertion. Wrapper durations
were 49.773 s and 199.134 s respectively. Configuration,
geometry upload and stop are excluded from the maximum-call metric. Synchronous
in-process preparation remains unsuitable to assume safe on a GTA thread; this
trial does not qualify that thread's latency or stack.

`python3 tools/gtaiv-skate/check.py` passed all seven authored suites.
The repository gate passed 79 tests and links/context checks in 70 documents.
Fixed-revision review results belong to the final publication on #53.
Focused Rust builds retain existing dead-code warnings.
Full upstream tests remain unavailable because the pinned map-startup test
source is missing.

## Remaining gameplay boundary

These are standalone authored Session proofs. No GTA file, plugin, input, launch
or installed runtime changed. They do not qualify a real street, show a board
or establish solved rider animation or owner acceptance.

[Collector #58](https://github.com/Jpatching/combine/pull/58) is already published;
its latest head passed all three CI jobs when checked. Its live ground result
remains inconclusive under
[#39's current verdict](https://github.com/Jpatching/combine/issues/39#issuecomment-6110986624).
The four exact intended surfaces/layers and an independently validated per-point
loading witness remain missing. The owner needs the labelled local inspection
views before being asked to identify marker bases; labels alone are insufficient.
A private explanatory gallery was prepared from all 16 retained PNGs and its
local browser opening was requested successfully. No pixels were inspected or
uploaded to AI; owner viewing and interpretation remain unverified.
Character state or successful height queries do not establish loading/layer.
[#54](https://github.com/Jpatching/combine/issues/54) still waits for #39 and #53;
board #55 and rider #56 remain downstream. Preserve existing drafts and recovery.
