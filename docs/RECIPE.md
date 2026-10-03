# Research recipe v1

A recipe describes a candidate combination for the selected upstream runtime. It is
portable configuration, not code, a game bundle, proof of ownership, or a native
upstream file format. The offline checker accepts the two catalogue combinations
below; their gameplay remains unverified.

| Field | Contract |
| --- | --- |
| schema_version | Integer 1 |
| id | Lowercase letters/digits separated by hyphens; 1–64 characters |
| title | Nonempty display string, up to 120 characters; no control characters |
| runtime | Exactly id and commit, matching research/upstream.lock.json |
| world | iw4:mp_rust or minecraft:overworld |
| movement | Exactly ["on-foot", "skate"] |
| combat | mw2-default |
| required_content | Exact ordered identifiers specified for the selected world |

MW2 Rust requires `mw2-2009-steam-multiplayer` and `skate3-xbox360-extracted`.
Minecraft overworld additionally requires `minecraft-26.3-runtime-data`. This last
identifier describes the upstream runtime's content requirement; it is not a token,
download authorization or instruction to obtain files.

Examples: [MW2/Skate](../recipes/mw2-skate.json) and
[Minecraft/MW2/Skate](../recipes/minecraft-skate.json). Settings not expressible here
remain runtime defaults. No seed, physics tuning, arbitrary mods or new game support
is promised. On-foot and skating are available modes, not simultaneous controllers;
enter skating manually during the pilot.

## Inputs, outputs and failures

`python3 scripts/check_recipe.py <recipe.json>` reads a UTF-8 JSON file of at most
64 KiB with at most 16 nesting levels and the trusted repository lock. It rejects unknown/missing keys, duplicate
JSON keys, non-finite numbers, malformed input, mismatched pins and unsupported
settings. Exit 0 means metadata accepted; exit 1 means validation/read failure;
exit 2 is command-line usage error. It does not emit input contents in diagnostics.

Recipes have no paths, URLs, executable hooks, shell fragments, assets or secrets.
Runtime paths will belong in a separate local-only configuration when a companion
is justified. A checksum identifies content; it is not an execution-safety guarantee.

## Future adapter boundary (not implemented)

1. Check: recipe + local installation references -> readiness or actionable reasons.
2. Prepare: compatible inputs -> isolated profile or recoverable failure.
3. Launch: prepared profile -> explicit local process start and session result.

For this milestone, a tester applies world selection and skating activation manually
using the Windows runbook. An accepted recipe does not invoke these stages. Before
implementing them, C-003 and C-005 must establish working behaviour and a useful
improvement; C-006 governs public distribution. Treat any new recipe format or
supported runtime pin as a reviewed catalogue change with fresh compatibility evidence.
