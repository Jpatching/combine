# Combine

Combine connects an existing game's world and normal gameplay with Skate physics and mechanics.

## Language

**Host game**:
The game that supplies the world and its ordinary gameplay. For the GTA experiment, this is offline GTA IV, including its traffic, pedestrians, vehicles and missions.

**Riding**:
The mode in which Skate controls the mounted skater's movement.

**Dismounted**:
The mode in which normal host-game movement, camera and vehicle use are available again.

**Skate Session**:
An active instance of the existing Skate simulation, with its collision, controls and skater pose.

## Riding surfaces

**Sampled surface**:
Host-game floor found by querying the running game around the rider, as opposed to floor decoded from collision files.
_Avoid_: live ground, probe surface

**Resident collision**:
The host game's collision currently held in memory around the player, as opposed to collision files on disk.
_Avoid_: loaded bounds, nearby collision, streamed bounds

**Coverage window**:
The area of sampled surface currently given to the Skate Session around the rider. It follows the rider in fixed world cells: crossing out of its centre cell resamples it, and the new window replaces the old one without a remount.
_Avoid_: flat patch, patch, grid

**Coverage gap**:
A place the coverage window cannot honestly cover, such as a wall-sized height jump, unloaded ground or a vehicle. Mounting there is refused, or riding into it dismounts, with a stated reason. The window's edge is not a gap: the window moves with the rider.
_Avoid_: hole, unsupported area

**Floor agreement**:
The host-game ground under the rider belongs to the floor the coverage window describes, allowing for the error that sampling introduces. It is about which floor the rider is on, not how closely the skater appears planted on it. It is checked only while Skate reports ground contact; leaving the ground does not lose it. Losing it ends the ride with a stated reason.
_Avoid_: ground check, height match
