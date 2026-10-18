//! The floor contract: the only way GTA ground reaches a Skate Session.
//! GTA coordinates are Z-up; Skate is Y-up, in metres.
pub type Triangle = [[f32; 3]; 3];
pub const MAX_TRIANGLES: usize = 4096;
/// Floor agreement: host ground at a grounded rider is within the coverage
/// window's wall threshold of the floor (ADR 0004).
pub const FLOOR_AGREEMENT: f32 = 0.3;
/// A host query belongs to the displayed pose when it is this close to it.
pub const QUERY_AGREEMENT: f32 = 0.001;
/// Supports closer than this are one floor; farther apart, stacked floors.
pub const SAME_FLOOR: f32 = 0.001;
/// The rider stays within this height of the floor under it.
pub const POSE_HEIGHT: f32 = 3.;
/// Smallest triangle area (and vertical-face projection) the floor accepts, m^2.
pub const MIN_AREA: f32 = 0.000001;
/// GTA coordinate bound for any vertex.
pub const MAX_COORDINATE: f32 = 1_000_000.;
/// One upload reaches no farther than this from the rider.
pub const MAX_REACH: f32 = 1000.;
/// The Skate frame stays at the mount origin for the whole ride; within this
/// extent f32 resolves positions to under a millimetre (2^13 m).
pub const MAX_RIDE: f32 = 8192.;
/// Accepted GTA-to-Skate scales.
pub const SCALES: std::ops::RangeInclusive<f32> = 0.1..=10.;
/// Skate reports ground contact in every physical state but the air states.
pub fn grounded(state: &str) -> bool {
    !state.contains("Air")
}
/// The Skate frame and selected floor: fixed at mount for the whole ride.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Basis {
    pub origin: [f32; 3],
    pub scale: f32,
    pub layer: u32,
}
/// The displayed rider, the host ground queried under it, and Skate ground contact.
#[derive(Clone, Copy, Debug)]
pub struct Rider {
    pub pose: [f32; 3],
    pub grounded: bool,
    pub query: [f32; 2],
    pub ground: f32,
    pub layer: u32,
    pub valid: u32,
}
/// An installed floor: triangles on one selected layer, in a fixed Skate frame.
pub struct Surface {
    basis: Basis,
    triangles: Vec<Triangle>,
    revision: u64,
}
impl Surface {
    /// The one way a floor reaches a Session: install these triangles for this
    /// rider, or refuse with a reason. `current` is None at mount.
    pub fn install<E>(
        current: Option<&Surface>,
        triangles: Vec<Triangle>,
        basis: Basis,
        rider: &Rider,
        install: impl FnOnce(&Surface) -> Result<(), E>,
    ) -> Result<Surface, &'static str> {
        let revision = match current {
            None => 1,
            Some(old) => {
                if old.basis != basis {
                    return Err("floor basis changed");
                }
                if !old.agrees(rider) {
                    return Err("rider left the current floor");
                }
                old.revision.checked_add(1).ok_or("floor revisions exhausted")?
            }
        };
        let next = Self::qualify(triangles, basis, rider.query, revision)?;
        if !next.agrees(rider) {
            return Err("floor does not support the rider");
        }
        install(&next).map_err(|_| "Session refused the floor")?;
        Ok(next)
    }
    fn qualify(
        mut triangles: Vec<Triangle>,
        basis: Basis,
        near: [f32; 2],
        revision: u64,
    ) -> Result<Self, &'static str> {
        let Basis { origin, scale, layer } = basis;
        if layer == 0
            || triangles.is_empty()
            || triangles.len() > MAX_TRIANGLES
            || !scale.is_finite()
            || !SCALES.contains(&scale)
            || !origin
                .iter()
                .chain(&near)
                .chain(triangles.iter().flatten().flatten())
                .all(|v| v.is_finite())
        {
            return Err("invalid geometry");
        }
        for t in &mut triangles {
            let area = (t[1][0] - t[0][0]) * (t[2][1] - t[0][1])
                - (t[1][1] - t[0][1]) * (t[2][0] - t[0][0]);
            let u = std::array::from_fn::<_, 3, _>(|i| t[1][i] - t[0][i]);
            let v = std::array::from_fn::<_, 3, _>(|i| t[2][i] - t[0][i]);
            let cross = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], area];
            let magnitude = cross.iter().map(|c| c * c).sum::<f32>().sqrt();
            if !magnitude.is_finite()
                || magnitude * scale * scale < MIN_AREA
                || t.iter().flatten().any(|v| v.abs() > MAX_COORDINATE)
                || t.iter().any(|p| {
                    (0..2).any(|i| (p[i] - near[i]).abs() * scale > MAX_REACH)
                        || (0..3).any(|i| (p[i] - origin[i]).abs() * scale > MAX_RIDE)
                })
            {
                return Err("degenerate or oversized geometry");
            }
            if area < 0. {
                t.swap(1, 2);
            }
        }
        Ok(Self { basis, triangles, revision })
    }
    fn support(&self, xy: [f32; 2]) -> Option<f32> {
        let scale = self.basis.scale;
        let mut found: Option<f32> = None;
        for t in &self.triangles {
            let d = (t[1][1] - t[2][1]) * (t[0][0] - t[2][0])
                + (t[2][0] - t[1][0]) * (t[0][1] - t[2][1]);
            // Vertical faces still participate in Session collision, not floor support.
            if d.abs() * scale * scale < MIN_AREA {
                continue;
            }
            let a = ((t[1][1] - t[2][1]) * (xy[0] - t[2][0])
                + (t[2][0] - t[1][0]) * (xy[1] - t[2][1]))
                / d;
            let b = ((t[2][1] - t[0][1]) * (xy[0] - t[2][0])
                + (t[0][0] - t[2][0]) * (xy[1] - t[2][1]))
                / d;
            let c = 1. - a - b;
            if a >= -0.000001 && b >= -0.000001 && c >= -0.000001 {
                let z = a * t[0][2] + b * t[1][2] + c * t[2][2];
                if found.is_some_and(|old| (old - z).abs() * scale > SAME_FLOOR) {
                    return None;
                }
                found = Some(z);
            }
        }
        found
    }
    pub fn basis(&self) -> Basis {
        self.basis
    }
    pub fn revision(&self) -> u64 {
        self.revision
    }
    /// Query at the displayed pose, on this floor, with the pose supported by it.
    pub fn agrees(&self, rider: &Rider) -> bool {
        self.query_matches_pose(rider.query, rider.pose)
            && self.observation(rider)
            && self.contains_pose(rider.pose)
    }
    pub fn query_matches_pose(&self, xy: [f32; 2], pose: [f32; 3]) -> bool {
        xy.iter().zip(pose).all(|(v, p)| {
            v.is_finite() && p.is_finite() && (v - p).abs() * self.basis.scale <= QUERY_AGREEMENT
        })
    }
    /// The host observation is on this floor's coverage and layer, and, while
    /// Skate reports ground contact, in floor agreement with it.
    pub fn observation(&self, rider: &Rider) -> bool {
        rider.valid == 1
            && rider.layer == self.basis.layer
            && rider.query.iter().chain([rider.ground].iter()).all(|v| v.is_finite())
            && self.support(rider.query).is_some_and(|z| {
                !rider.grounded || (z - rider.ground).abs() * self.basis.scale <= FLOOR_AGREEMENT
            })
    }
    pub fn contains_pose(&self, p: [f32; 3]) -> bool {
        p.iter().all(|v| v.is_finite())
            && self
                .support([p[0], p[1]])
                .is_some_and(|z| (p[2] - z).abs() * self.basis.scale < POSE_HEIGHT)
    }
    pub fn to_skate(&self, p: [f32; 3]) -> [f32; 3] {
        let Basis { origin, scale, .. } = self.basis;
        [
            (p[0] - origin[0]) * scale,
            (p[2] - origin[2]) * scale,
            -(p[1] - origin[1]) * scale,
        ]
    }
    pub fn to_gta(&self, p: [f32; 3]) -> [f32; 3] {
        let Basis { origin, scale, .. } = self.basis;
        [
            p[0] / scale + origin[0],
            -p[2] / scale + origin[1],
            p[1] / scale + origin[2],
        ]
    }
    /// GTA-space triangles, wound upward, as qualified.
    pub fn host_triangles(&self) -> &[Triangle] {
        &self.triangles
    }
    /// Skate-space triangles for Session collision.
    pub fn triangles(&self) -> Vec<Triangle> {
        self.triangles.iter().map(|t| t.map(|p| self.to_skate(p))).collect()
    }
}
/// Use the documented GET_GAME_TIMER milliseconds, never raw CLEO time_step.
pub struct Clock {
    last: u32,
    remaining: f64,
    period: f64,
}
impl Clock {
    pub fn new(now: u32, period: f32) -> Result<Self, &'static str> {
        if !period.is_finite() || !(0.001..=0.1).contains(&period) {
            return Err("invalid period");
        }
        Ok(Self {
            last: now,
            remaining: 0.,
            period: f64::from(period),
        })
    }
    pub fn steps(&mut self, now: u32) -> Result<usize, &'static str> {
        let elapsed = now.wrapping_sub(self.last);
        self.last = now;
        if elapsed > 250 {
            return Err("time discontinuity");
        }
        self.remaining += f64::from(elapsed) / 1000.;
        let steps = ((self.remaining + 1e-8) / self.period).floor() as usize;
        if steps > 32 {
            return Err("simulation backlog");
        }
        self.remaining -= steps as f64 * self.period;
        Ok(steps)
    }
}
pub fn skate_heading(gta_degrees: f32) -> f32 {
    std::f32::consts::PI + gta_degrees.to_radians()
}
pub fn gta_heading(skate_forward: [f32; 3]) -> f32 {
    (-skate_forward[0])
        .atan2(-skate_forward[2])
        .to_degrees()
        .rem_euclid(360.)
}
/// Bounded preparation; failed uploads cannot leave a reusable partial floor.
#[derive(Default)]
pub struct GeometryBuilder {
    layer: u32,
    count: usize,
    vertices: Vec<[f32; 3]>,
}
impl GeometryBuilder {
    pub fn begin(&mut self, layer: u32, triangles: u32) -> i32 {
        *self = Self::default();
        if layer == 0 || triangles == 0 || triangles as usize > MAX_TRIANGLES {
            return 0;
        }
        self.layer = layer;
        self.count = triangles as usize * 3;
        1
    }
    pub fn vertex(&mut self, p: [f32; 3]) -> i32 {
        if self.layer == 0 || self.vertices.len() >= self.count || !p.iter().all(|v| v.is_finite())
        {
            *self = Self::default();
            return 0;
        }
        self.vertices.push(p);
        1
    }
    /// The complete staged upload for `layer`, consumed whether or not it qualifies.
    pub fn finish(&mut self, layer: u32, valid: u32) -> Result<Vec<Triangle>, &'static str> {
        let staged = std::mem::take(self);
        if valid != 1
            || layer != staged.layer
            || staged.vertices.len() != staged.count
            || staged.count == 0
        {
            return Err("incomplete or unqualified surface");
        }
        Ok(staged.vertices.chunks_exact(3).map(|c| [c[0], c[1], c[2]]).collect())
    }
}
