# Supplied collision coverage

Isolated runtime preparation injects strict JSON data into the single `SURFACES`
declaration in `combine_skate.js`. Keep actual geometry and qualification records
private. This interface consumes qualification; it does not establish it or load
map resources automatically.

Each record requires `qualified: true`, a nonempty `evidence` string, an integer
`layer` from 1 through 4294967295, and 1–4096 `triangles`. Each triangle is three
finite GTA-coordinate `[x, y, z]` vertices. Preserve nearby obstacle triangles as
well as the supporting floor. Do not flatten, extrapolate, or discard unsupported
resource shapes to create apparent coverage.

There are two explicit coverage forms:

- A bounded region omits `coverage` and supplies finite `center: [x, y]` and a
  positive `radius`. Both the circle and the supplied triangles limit its coverage.
  Existing prepared 3 m regions retain that qualification boundary.
- A complete mesh supplies `coverage: "mesh"` and omits `center` and `radius`.
  Qualification must cover the complete supplied mesh at its established world
  placement. Its triangles define coverage, including holes and the actual edge;
  there is no fixed outer radius. Unknown modes and mixed mesh/radius records
  refuse. Complete meshes also receive the native coordinate and triangle-area
  validation before local selection, including geometry far from the rider.

Large regions and complete meshes supply local 4 m collision windows centered
at the player and refreshed during riding through the existing asynchronous
Session replacement interface. This is a streaming size, not the mesh's outer
ride boundary. Selection retains whole triangles whose horizontal bounds
intersect the local square, including walls. Every accepted pose still needs
support in the original qualified geometry. Failed replacement restores GTA
control through the existing recovery path.

This source capability does not expand the installed prepared data. A broader
live ride needs broader independently qualified collision supplied through the
same interface. Merely adding `coverage: "mesh"` to old checkpoint data does not
supply that evidence. Arbitrary resource placement, automatic map acquisition,
stacked-floor disambiguation, floor transitions, and state-appropriate airborne
validation remain separate requirements in issues #65 and #66. Existing host
agreement, layer, freshness, and floor-relative pose checks remain in force.

Authored behavior checks: `node tools/gtaiv-skate/tests/coverage.cjs` and
`node tools/gtaiv-skate/tests/script.cjs`. These exercise the script-to-Session
boundary; they do not establish physical GTA contact or live map coverage.
