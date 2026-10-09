# Preserve offline GTA IV gameplay while riding with Skate

The owner selected offline GTA IV as the host game, preserving its city, traffic, pedestrians, vehicles and missions while reusing the existing Skate simulation for riding. Mounting while on foot transfers movement to Skate; dismounting returns ordinary GTA movement, camera and vehicle use. Reconstructing the city in the MW2 host would also require rebuilding the GTA gameplay the owner wants to retain.

A separate Skate worker is approved for evaluation, not selected as the permanent runtime architecture. Compare it with the preserved in-process candidate through collision, input, pose and failure recovery before replacing that candidate. Process separation may simplify iteration and isolate simulation failures; it does not supply GTA collision or skater presentation.

On 2026-10-09 the owner reaffirmed this host choice and selected a bounded real-street demonstration before full-city work. Traffic and pedestrians remain active, while the first riding proof covers static streets, pavements and walls; physical riding interaction with moving objects is deferred. The demonstration needs a visible board and recognisable skating animation, followed by dismount and ordinary GTA driving. Collision preparation alone is not that milestone.

[Issue #20](https://github.com/Jpatching/combine/issues/20) remains the current mount/move/dismount experiment. This decision records the broader desired behavior; it does not mark its acceptance complete or expand that ticket into full-city integration.
