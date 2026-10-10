#[path = "../connection.rs"]
mod connection;
#[path = "../wire.rs"]
mod wire;
use connection::{Clock, Surface, gta_heading, skate_heading};
use skate_host::bridge::{Controls, Session};
use std::{io, path::PathBuf};
fn main() {
    if run().is_err() {
        std::process::exit(2);
    }
}
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let config = std::env::current_exe()?
        .parent()
        .ok_or("worker directory")?
        .join("combine_skate.assets.txt");
    let content = std::fs::read_to_string(config)?;
    let root = PathBuf::from(content.trim_start_matches('\u{feff}').trim());
    if !root.is_absolute() || !root.is_dir() || content.trim().lines().count() != 1 {
        return Err("assets unavailable".into());
    }
    let mut session: Option<Session> = None;
    let mut surface: Option<Surface> = None;
    let mut clock: Option<Clock> = None;
    let mut identity = 0;
    let mut revision = 0;
    let mut sequence = 0;
    let mut riding = false;
    let mut input = io::stdin().lock();
    let mut output = io::stdout().lock();
    loop {
        let request = wire::Request::read(&mut input)?;
        match request.kind {
            1 => {
                if riding
                    || request.ride <= identity
                    || request.sequence != 0
                    || request.revision <= revision
                {
                    return Err("stale prepare".into());
                }
                let next = Surface::new(request.points.to_vec(), request.origin, request.scale)?;
                if let Some(active) = session.as_mut() {
                    active.suspend_input();
                    let collision = active.collision_builder().build(next.triangles(), vec![])?;
                    active.install_collision(collision)?;
                } else {
                    session = Some(Session::new(
                        &root,
                        next.triangles(),
                        vec![],
                        [0., 1., 0.],
                        skate_heading(request.heading),
                    )?);
                }
                let active = session.as_mut().ok_or("session missing")?;
                active.activate([0., 1., 0.], skate_heading(request.heading))?;
                clock = None;
                identity = request.ride;
                revision = request.revision;
                sequence = 0;
                riding = true;
                surface = Some(next);
            }
            2 => {
                if !riding
                    || request.ride != identity
                    || request.revision != revision
                    || request.sequence != sequence + 1
                {
                    return Err("stale tick".into());
                }
                let active = session.as_mut().ok_or("session missing")?;
                if clock.is_none() {
                    clock = Some(Clock::new(request.now, active.period())?);
                }
                let count = clock.as_mut().unwrap().steps(request.now)?;
                for _ in 0..count {
                    active.tick(Controls {
                        buttons: request.buttons & (0x1000 | 0x4000),
                        left: request.left,
                        ..Controls::default()
                    })?;
                }
                sequence = request.sequence;
            }
            3 => {
                if request.ride != identity || request.revision != revision {
                    return Err("stale stop".into());
                }
                session.as_mut().ok_or("session missing")?.suspend_input();
                riding = false;
            }
            _ => return Err("unsupported request".into()),
        }
        let active = session.as_ref().ok_or("session missing")?;
        let selected = surface.as_ref().ok_or("surface missing")?;
        let pose = active.pose();
        if !pose
            .root
            .to_cols_array()
            .iter()
            .chain(pose.velocity.to_array().iter())
            .all(|v| v.is_finite())
            || !pose
                .bones
                .iter()
                .all(|m| m.to_cols_array().iter().all(|v| v.is_finite()))
        {
            return Err("invalid pose".into());
        }
        let pos = selected.to_gta(pose.root.w_axis.truncate().to_array());
        if request.kind != 3 && !selected.contains(pos, request.ground) {
            return Err("surface exit".into());
        }
        let heading = gta_heading(pose.root.z_axis.truncate().to_array());
        wire::Response {
            ride: identity,
            revision,
            sequence: request.sequence,
            pose: [pos[0], pos[1], pos[2], heading],
            period: active.period(),
        }
        .write(&mut output)?;
    }
}
