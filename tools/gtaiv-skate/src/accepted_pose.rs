//! Last accepted bridge output keeps its original deadline across reads.
use crate::connection::Surface;
use std::time::{Duration, Instant};
#[derive(Clone, Copy)]
pub struct AcceptedPose {
    ride: u64,
    revision: u64,
    epoch: u64,
    pose: [f32; 4],
    updated: Instant,
}
impl AcceptedPose {
    pub fn new(
        ride: u64,
        revision: u64,
        epoch: u64,
        pose: [f32; 4],
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
            updated,
        })
    }
    pub fn fresh(
        &self,
        ride: u64,
        revision: u64,
        epoch: u64,
        now: Instant,
        ground: f32,
        surface: &Surface,
    ) -> Option<[f32; 4]> {
        self.fresh_observation(ride, revision, epoch, now, ground, surface, None)
    }
    pub fn fresh_observation(
        &self,
        ride: u64,
        revision: u64,
        epoch: u64,
        now: Instant,
        ground: f32,
        surface: &Surface,
        observation: Option<([f32; 2], u32, u32)>,
    ) -> Option<[f32; 4]> {
        if self.ride != ride
            || self.revision != revision
            || self.epoch != epoch
            || now.checked_duration_since(self.updated)? > Duration::from_millis(250)
            || !match observation {
                Some((xy, layer, valid)) => {
                    surface.is_geometry()
                        && surface.observation(xy, ground, layer, valid)
                        && surface.contains_pose([self.pose[0], self.pose[1], self.pose[2]])
                }
                None => {
                    !surface.is_geometry()
                        && surface.contains([self.pose[0], self.pose[1], self.pose[2]], ground)
                }
            }
        {
            return None;
        }
        Some(self.pose)
    }
}
