# Combine

Combine explores a controller-friendly trickshot menu in the existing
MW2 / Skate 3 / Minecraft mashup. The destination is the **proper Synergy menu
plus trickshot hit radius**, without Combine-specific practice additions.
The owner confirmed on October 4 that this means **Synergy itself**, running its
GSC menu source, rather than our custom native panel. The actual GSC menu
is integrated, with Intervention/input checks passing and a versioned local
trial ready. The earlier native Intervention build is preserved and unaccepted;
it is not the requested replacement. Other option effects remain unverified. This is experimental,
not a complete menu or production launcher.
See the [menu requirements and coverage](docs/TRICKSHOT_MENU.md).
To resume, say **Continue Combine**; the [workflow](docs/WORKFLOW.md) follows current
evidence through the menu work, then Fortnite map qualification.

The agreed destination includes sniper near-pass assistance (Off by default,
0.25–5 metres, Normal/One-shot damage with ordinary cover rules), Frag No Clip
and host-controlled private-player options. These requirements are recorded;
the Intervention build does not yet implement them.

The owner reports that Minecraft and skating work in the upstream Windows trial.
Recovery, replay and a possible freeze still need investigation. A successful
build or synthetic test does not establish gameplay.

## Current trial status

The October 5 desktop review folder **Combine Synergy - 2026-10-05 - c591086**
contains **Test Synergy**, **Open trial files** and **Read checklist** shortcuts.
The actual menu and all its original sections are present; Intervention/input
is the verified scope. God Mode, ammo/perks and subsequent batches still need
effect/reversal checks. The agreed hit radius is not implemented.
The owner can launch this exact local trial; it is prepared and unaccepted. See the [current handoff](docs/HANDOFF.md).

Developers can reproduce the source patches using the [menu guide](docs/TRICKSHOT_MENU.md).
This source repository contains no game files, ready-to-play download or installer.
The private planning board is owner-only; public technical evidence lives here.

## Earlier practice build (preserved trial)

The controls below also apply to the Intervention menu. The Positions, Targets
and Aim actions described here belong only to the earlier preserved build.


The menu starts hidden and leaves no banner or aim-lock overlay when closed.
It uses the game's proportional font, cyan selection, seven row slots and
Positions, Targets and Aim submenus.

| Control | DualSense | Keyboard |
| --- | --- | --- |
| Open / close | Hold L2, press R3 | F6 |
| Move | D-pad up/down or L2/R2 | Up/down arrows |
| Select | Cross or Square | Enter or right arrow |
| Back | Circle or R3 | Backspace or left arrow |
| Close immediately | Hold L2, press R3 | Escape |

Release buttons after opening or closing. While captured, inputs cannot shoot,
jump, melee or toggle skating. Escape closes the menu without opening pause.

- **Positions:** save your starting spot, then return to it. Return leaves skating
  first. Saved positions are cleared on map change.
- **Targets:** request a stationary bot, place the latest living bot at your
  position, or freeze bots. Bots remain damageable.
- **Aim:** optionally enable bot aim lock, apply a smooth controller preset, or
  restore the settings captured before applying that preset in the current run.
Settings persist only in the isolated trial's profile.

A separate development audio patch adds board pop/landing cues from skating
events and an optional short music cue when entering skating or doing Christ Air.
Sound files stay local. A ten-second **Even Flow** cue from the owner's supplied
MP3 is installed in the audio trial, and startup decoding is confirmed. The
comedy video also has a new music-backed export. Original Skate collision samples
still need a listening check; their exact pop/landing assignment is provisional.
See the [audio and highlights record](research/results/2026-10-03-skate-audio-highlights.md).

Actions report feedback inside the menu and leave it open, including on failure.
Aim lock starts off. It requires the local host's debug-enabled world with no
other humans, and only aims while on foot and holding aim at a visible, living
enemy bot within 30 degrees. It does not fire for you.

## Setup and checks

Players need a separately prepared, lawful local Windows runtime and game data.
Follow the [Windows baseline runbook](docs/WINDOWS_BASELINE.md). The menu patch
includes source, attribution and tests; it includes no games or IW4x binaries.
Use the [menu build and trial guide](docs/TRICKSHOT_MENU.md) to reproduce the
pinned development build and prepare a fresh trial without replacing originals.

For the offline research catalogue (Python 3.10+, no extra packages):

```sh
python3 scripts/verify.py
python3 scripts/check_recipe.py recipes/mw2-skate.json
```

On Windows use `py -3`. These commands check metadata and recipes; they do not
install or launch games. See the [private phase board](https://github.com/users/Jpatching/projects/5/views/4)
for status, [BACKLOG.md](BACKLOG.md) for history,
[HANDOFF.md](docs/HANDOFF.md) for current evidence, and
[RESEARCH.md](docs/RESEARCH.md) for upstream limitations.

## Source and limits

The menu presentation/navigation adapts
[Synergy MW2 by SyndiShanX](https://github.com/SyndiShanX/Synergy-GSC-Menu/tree/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2),
including its M203 / Xeirh and Apparition Structure Team credits.
The adapted code is [GPLv3](licenses/Synergy-GPL-3.0.md); the
[patch guide](patches/README.md) describes its scope and attribution.

No generic GSC loader, public-match assistance, firing while skating, new game
integration, launcher product or marketplace is implemented. The stunt launcher
is a [separate proposal](docs/STUNT_LAUNCHER_PROPOSAL.md). Publication to
Jpatching/combine is authorized for reviewed source branches; owner acceptance,
merge and release remain separate (D-016/D-017).
Game assets, OBS/recordings, private logs and local settings stay outside Git.
Source licensing does not settle asset rights or publisher terms.
