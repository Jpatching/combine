pub const MAX_TRIANGLES: usize = 4096;
/// One bounded, approximately flat GTA ground patch, sampled on a 5x5 grid.
/// GTA coordinates are Z-up; Skate is Y-up, in metres.
pub struct Surface {
    points: Vec<[f32; 3]>,
    origin: [f32; 3],
    scale: f32,
    geometry: Option<(u32, Vec<[[f32; 3]; 3]>)>,
}
impl Surface {
    pub fn new(points: Vec<[f32; 3]>, origin: [f32; 3], scale: f32) -> Result<Self, &'static str> {
        if points.len() != 25
            || !scale.is_finite()
            || !(0.1..=10.).contains(&scale)
            || !origin
                .iter()
                .chain(points.iter().flatten())
                .all(|v| v.is_finite())
        {
            return Err("invalid surface");
        }
        for (i, p) in points.iter().enumerate() {
            let expected = [
                origin[0] - 4. / scale + (i % 5) as f32 * 2. / scale,
                origin[1] - 4. / scale + (i / 5) as f32 * 2. / scale,
            ];
            if (p[0] - expected[0]).abs() > 0.001 / scale
                || (p[1] - expected[1]).abs() > 0.001 / scale
                || (p[2] - origin[2]).abs() > 0.05 / scale
            {
                return Err("surface is not a flat grid");
            }
        }
        Ok(Self {
            points,
            origin,
            scale,
            geometry: None,
        })
    }
    pub fn from_triangles(
        mut triangles: Vec<[[f32; 3]; 3]>,
        origin: [f32; 3],
        scale: f32,
        layer: u32,
    ) -> Result<Self, &'static str> {
        if layer == 0
            || triangles.is_empty()
            || triangles.len() > MAX_TRIANGLES
            || !scale.is_finite()
            || !(0.1..=10.).contains(&scale)
            || !origin
                .iter()
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
                || magnitude * scale * scale < 0.000001
                || t.iter().flatten().any(|v| v.abs() > 1_000_000.)
                || t.iter().any(|p| {
                    p.iter()
                        .zip(origin)
                        .any(|(v, o)| (v - o).abs() * scale > 1000.)
                })
            {
                return Err("degenerate or oversized geometry");
            }
            if area < 0. {
                t.swap(1, 2);
            }
        }
        let surface = Self {
            points: vec![],
            origin,
            scale,
            geometry: Some((layer, triangles)),
        };
        if !surface.observation([origin[0], origin[1]], origin[2], layer, 1) {
            return Err("unsupported mount ground");
        }
        Ok(surface)
    }
    fn support(&self, xy: [f32; 2]) -> Option<f32> {
        let (_, triangles) = self.geometry.as_ref()?;
        let mut found: Option<f32> = None;
        for t in triangles {
            let d = (t[1][1] - t[2][1]) * (t[0][0] - t[2][0])
                + (t[2][0] - t[1][0]) * (t[0][1] - t[2][1]);
            // Vertical faces still participate in Session collision, not floor support.
            if d.abs() * self.scale * self.scale < 0.000001 {
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
                if found.is_some_and(|old| (old - z).abs() * self.scale > 0.001) {
                    return None;
                }
                found = Some(z);
            }
        }
        found
    }
    pub fn is_geometry(&self) -> bool {
        self.geometry.is_some()
    }
    pub fn query_matches_pose(&self, xy: [f32; 2], pose: [f32; 3]) -> bool {
        xy.iter()
            .zip(pose)
            .all(|(v, p)| v.is_finite() && p.is_finite() && (v - p).abs() * self.scale <= 0.001)
    }
    pub fn observation(&self, xy: [f32; 2], ground: f32, layer: u32, valid: u32) -> bool {
        if valid != 1 || !xy.iter().chain([ground].iter()).all(|v| v.is_finite()) {
            return false;
        }
        match self.geometry.as_ref() {
            Some((selected, _)) => {
                *selected == layer
                    && self
                        .support(xy)
                        .is_some_and(|z| (z - ground).abs() * self.scale <= 0.05)
            }
            None => layer == 0 && self.contains([xy[0], xy[1], ground], ground),
        }
    }
    pub fn contains_pose(&self, p: [f32; 3]) -> bool {
        p.iter().all(|v| v.is_finite())
            && self
                .support([p[0], p[1]])
                .is_some_and(|z| (p[2] - z).abs() * self.scale < 3.)
    }
    pub fn to_skate(&self, p: [f32; 3]) -> [f32; 3] {
        [
            (p[0] - self.origin[0]) * self.scale,
            (p[2] - self.origin[2]) * self.scale,
            -(p[1] - self.origin[1]) * self.scale,
        ]
    }
    pub fn to_gta(&self, p: [f32; 3]) -> [f32; 3] {
        [
            p[0] / self.scale + self.origin[0],
            -p[2] / self.scale + self.origin[1],
            p[1] / self.scale + self.origin[2],
        ]
    }
    pub fn contains(&self, p: [f32; 3], ground: f32) -> bool {
        p.iter().all(|v| v.is_finite())
            && ground.is_finite()
            && (p[0] - self.origin[0]).abs() * self.scale < 3.5
            && (p[1] - self.origin[1]).abs() * self.scale < 3.5
            && (ground - self.origin[2]).abs() * self.scale <= 0.05
            && (p[2] - self.origin[2]).abs() * self.scale < 3.
    }
    pub fn triangles(&self) -> Vec<[[f32; 3]; 3]> {
        if let Some((_, triangles)) = &self.geometry {
            return triangles
                .iter()
                .map(|t| t.map(|p| self.to_skate(p)))
                .collect();
        }
        let mut out = Vec::new();
        for y in 0..4 {
            for x in 0..4 {
                let a = y * 5 + x;
                let b = a + 1;
                let c = a + 5;
                let d = c + 1;
                // Y-up winding after the right-handed Z-up -> Y-up rotation.
                out.push([a, b, c].map(|i| self.to_skate(self.points[i])));
                out.push([b, d, c].map(|i| self.to_skate(self.points[i])));
            }
        }
        out
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
/// Bounded preparation; failed uploads cannot leave a reusable partial surface.
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
    pub fn finish(
        &mut self,
        origin: [f32; 3],
        scale: f32,
        layer: u32,
        valid: u32,
    ) -> Result<(Surface, Vec<[[f32; 3]; 3]>), &'static str> {
        let staged = std::mem::take(self);
        if valid != 1
            || layer != staged.layer
            || staged.vertices.len() != staged.count
            || staged.count == 0
        {
            return Err("incomplete or unqualified surface");
        }
        let triangles: Vec<_> = staged
            .vertices
            .chunks_exact(3)
            .map(|c| [c[0], c[1], c[2]])
            .collect();
        let surface = Surface::from_triangles(triangles.clone(), origin, scale, layer)?;
        Ok((surface, triangles))
    }
}
