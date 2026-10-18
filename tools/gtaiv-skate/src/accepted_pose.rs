//! Last accepted bridge output keeps its original deadline across reads.
use crate::connection::{Rider, Surface};
use std::time::{Duration, Instant};
#[derive(Clone, Copy)]
pub struct AcceptedPose {
    ride: u64,
    revision: u64,
    epoch: u64,
    pose: [f32; 4],
    grounded: bool,
    updated: Instant,
}
impl AcceptedPose {
    pub fn new(
        ride: u64,
        revision: u64,
        epoch: u64,
        pose: [f32; 4],
        grounded: bool,
        updated: Instant,
    ) -> Option<Self> {
        if ride == 0 || revision == 0 || epoch == 0 || !pose.iter().all(|v| v.is_finite()) {
            return None;
        }
        Some(Self {
            ride,
            revision,
            epoch,
            pose,
            grounded,
            updated,
        })
    }
    pub fn grounded(&self) -> bool {
        self.grounded
    }
    /// The pose, while fresh, if the host observation at `query` is on its floor.
    #[allow(clippy::too_many_arguments)]
    pub fn fresh(
        &self,
        ride: u64,
        revision: u64,
        epoch: u64,
        now: Instant,
        surface: &Surface,
        query: [f32; 2],
        ground: f32,
        layer: u32,
        valid: u32,
    ) -> Option<[f32; 4]> {
        let pose = [self.pose[0], self.pose[1], self.pose[2]];
        let seen = Rider { pose, grounded: self.grounded, query, ground, layer, valid };
        if self.ride != ride
            || self.revision != revision
            || self.epoch != epoch
            || now.checked_duration_since(self.updated)? > Duration::from_millis(250)
            || !surface.observation(&seen)
            || !surface.contains_pose(pose)
        {
            return None;
        }
        Some(self.pose)
    }
}
