# Preserve the interactive Fortnite world with Skate riding

The owner selected Fortnite building, editing and destruction with actual Skate
movement, tricks and grinds. A static exported island would lose the world
behavior being requested. The earlier static-world direction is superseded;
its source remains available in Git history.

Keep Fortnite world behavior in its host and reuse the existing Skate Session.
Prefer in-process reuse until an observed host constraint justifies separation.
No universal bridge interface is selected. The first proof and startup
prerequisites belong to [#4](https://github.com/Jpatching/combine/issues/4) and
[#5](https://github.com/Jpatching/combine/issues/5); the
[interactive-world contract](../FORTNITE_SKATE.md) owns final requirements.
This choice does not establish a working host adapter or authorize protection bypass.
