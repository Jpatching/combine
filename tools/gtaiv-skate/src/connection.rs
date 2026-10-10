/// One bounded, approximately flat GTA ground patch, sampled on a 5x5 grid.
/// GTA coordinates are Z-up; Skate is Y-up, in metres.
pub struct Surface {
    points: Vec<[f32; 3]>,
    origin: [f32; 3],
    scale: f32,
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
        })
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
