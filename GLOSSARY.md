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

**Collision resource**:
A retained host-game asset describing physical surfaces. Decoded geometry alone does not establish its street placement or use by the host game.

**Viewer qualification**:
Evidence that an inspection viewer displays the complete selected collision resource and surrounding map with the required coordinate behavior. It supports inspection of street placement; active host-game collision remains a separate claim.

**Street placement**:
The established relationship between a retained collision resource and an identifiable street location, supported by distinctive landmarks at unchanged coordinates.
