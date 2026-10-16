use crate::connection::{Clock, GeometryBuilder, Surface, gta_heading, skate_heading};
use skate_host::bridge::{Controls, Session};
use std::{
    cell::RefCell,
    ffi::OsString,
    os::windows::ffi::OsStringExt,
    panic::{AssertUnwindSafe, catch_unwind},
    path::PathBuf,
    sync::atomic::{AtomicU64, Ordering},
};

struct Ride {
    session: Session,
    surface: Surface,
    clock: Option<Clock>,
    pose: [f32; 4],
}
#[derive(Default)]
struct Adapter {
    generation: u64,
    points: Vec<[f32; 3]>,
    geometry: GeometryBuilder,
    ride: Option<Ride>,
    idle: Option<Session>,
    assets: Option<PathBuf>,
    config: Option<PathBuf>,
}
thread_local! { static ADAPTER: RefCell<Adapter> = RefCell::new(Adapter::default()); }
static RESET_GENERATION: AtomicU64 = AtomicU64::new(1);
use crate::Packet;
fn synchronize_reset(adapter: &mut Adapter) {
    let generation = RESET_GENERATION.load(Ordering::Acquire);
    if adapter.generation != generation {
        // A reset callback can run on another thread. Retire the old Session
        // here, on its owning thread, before any read or operation can use it.
        *adapter = Adapter { generation, ..Adapter::default() };
    }
}
fn guarded(operation: impl FnOnce(&mut Adapter) -> Result<(), ()>) -> i32 {
    let result = catch_unwind(AssertUnwindSafe(|| {
        ADAPTER.with(|a| {
            let mut adapter = a.borrow_mut();
            synchronize_reset(&mut adapter);
            operation(&mut adapter)?;
            if adapter.generation != RESET_GENERATION.load(Ordering::Acquire) {
                synchronize_reset(&mut adapter);
                return Err(());
            }
            Ok(())
        })
    }));
    if matches!(result, Ok(Ok(()))) {
        1
    } else {
        ADAPTER.with(|a| {
            let mut adapter = a.borrow_mut();
            adapter.ride = None;
            adapter.idle = None;
            adapter.points.clear();
            adapter.geometry = GeometryBuilder::default();
        });
        0
    }
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_stop() {
    ADAPTER.with(|a| {
        let mut adapter = a.borrow_mut();
        synchronize_reset(&mut adapter);
        if let Some(mut ride) = adapter.ride.take() {
            ride.session.suspend_input();
            adapter.idle = Some(ride.session);
        }
        adapter.points.clear();
        adapter.geometry = GeometryBuilder::default();
    });
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_vertex(x: f32, y: f32, z: f32) -> i32 {
    guarded(|a| {
        if a.points.len() >= 25 || ![x, y, z].iter().all(|v| v.is_finite()) {
            return Err(());
        }
        a.points.push([x, y, z]);
        Ok(())
    })
}
#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_config(plugin_path: *const u16, length: u32) -> i32 {
    guarded(|a| {
        let previous = a.assets.take();
        if plugin_path.is_null() || length == 0 || length >= 32768 {
            return Err(());
        }
        let wide = unsafe { std::slice::from_raw_parts(plugin_path, length as usize) };
        let plugin = PathBuf::from(OsString::from_wide(wide));
        let config = plugin.parent().ok_or(())?.join("combine_skate.assets.txt");
        let content = std::fs::read_to_string(&config).map_err(|_| ())?;
        let value = content.trim_start_matches('\u{feff}').trim();
        if value.is_empty() || value.lines().count() != 1 {
            return Err(());
        }
        let root = PathBuf::from(value);
        if !root.is_absolute() || !root.is_dir() {
            return Err(());
        }
        // Session data belongs to both the selected root and configuration
        // location. A changed pointer starts a fresh Session, even while idle.
        if previous.as_ref() != Some(&root) || a.config.as_ref() != Some(&config) {
            a.ride = None;
            a.idle = None;
        }
        a.config = Some(config);
        a.assets = Some(root);
        Ok(())
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_mount(x: f32, y: f32, ground: f32, heading: f32, scale: f32) -> i32 {
    guarded(|a| {
        a.ride = None;
        if !heading.is_finite() {
            return Err(());
        }
        let surface =
            Surface::new(std::mem::take(&mut a.points), [x, y, ground], scale).map_err(|_| ())?;
        start_ride(a, surface, ground, heading)
    })
}
fn start_ride(a: &mut Adapter, surface: Surface, ground: f32, heading: f32) -> Result<(), ()> {
    let root = a.assets.as_ref().ok_or(())?;
    if !root.is_dir() {
        return Err(());
    }
    let mut session = if let Some(mut session) = a.idle.take() {
        // Every mount supplies new collision before activation. Keeping assets
        // warm never permits the previous ride's surface or input to survive.
        let collision = session.collision_builder().build(surface.triangles(), vec![])
            .map_err(|_| ())?;
        session.install_collision(collision).map_err(|_| ())?;
        session
    } else {
        Session::new(root, surface.triangles(), vec![], [0., 1., 0.], skate_heading(heading))
            .map_err(|_| ())?
    };
    let pose = session
        .activate([0., 1., 0.], skate_heading(heading))
        .map_err(|_| ())?;
    let position = surface.to_gta(pose.root.w_axis.truncate().to_array());
    Clock::new(0, session.period()).map_err(|_| ())?;
    if !(if surface.is_geometry() {
        surface.contains_pose(position)
    } else {
        surface.contains(position, ground)
    }) {
        return Err(());
    }
    a.ride = Some(Ride {
        session,
        surface,
        clock: None,
        pose: [position[0], position[1], position[2], heading],
    });
    Ok(())
}

#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_tick(now: u32, ground: f32, packet: *const Packet) -> i32 {
    tick_at(now, ground, None, packet)
}
fn tick_at(
    now: u32,
    ground: f32,
    observation: Option<([f32; 2], u32, u32)>,
    packet: *const Packet,
) -> i32 {
    guarded(|a| {
        if packet.is_null() {
            return Err(());
        }
        let p = unsafe { &*packet };
        let ride = a.ride.as_mut().ok_or(())?;
        let accepted = match observation {
            Some((xy, layer, valid)) => {
                ride.surface.is_geometry()
                    && ride
                        .surface
                        .query_matches_pose(xy, [ride.pose[0], ride.pose[1], ride.pose[2]])
                    && ride.surface.observation(xy, ground, layer, valid)
                    && ride
                        .surface
                        .contains_pose([ride.pose[0], ride.pose[1], ride.pose[2]])
            }
            None => {
                !ride.surface.is_geometry()
                    && ride
                        .surface
                        .contains([ride.pose[0], ride.pose[1], ride.pose[2]], ground)
            }
        };
        if !accepted {
            return Err(());
        }
        if ride.clock.is_none() {
            ride.clock = Some(Clock::new(now, ride.session.period()).map_err(|_| ())?);
        }
        let count = ride.clock.as_mut().unwrap().steps(now).map_err(|_| ())?;
        // #20 only: allow the stock push buttons and steering. Trick/recovery
        // controls belong to later tickets and are deliberately not enabled here.
        let controls = Controls {
            buttons: p.buttons & (0x1000 | 0x4000),
            left: p.left,
            ..Controls::default()
        };
        for _ in 0..count {
            ride.session.tick(controls).map_err(|_| ())?;
        }
        let pose = ride.session.pose();
        if !pose.root.to_cols_array().iter().all(|v| v.is_finite()) {
            return Err(());
        }
        let pos = ride.surface.to_gta(pose.root.w_axis.truncate().to_array());
        if !(if ride.surface.is_geometry() {
            ride.surface.contains_pose(pos)
        } else {
            ride.surface.contains(pos, ground)
        }) {
            return Err(());
        }
        // Skate root local +Z is forward, GTA heading zero points along +Y.
        let forward = pose.root.z_axis;
        let heading = gta_heading([forward.x, forward.y, forward.z]);
        ride.pose = [pos[0], pos[1], pos[2], heading];
        Ok(())
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_value(index: i32) -> f32 {
    ADAPTER.with(|a| {
        let mut adapter = a.borrow_mut();
        synchronize_reset(&mut adapter);
        adapter
            .ride
            .as_ref()
            .and_then(|r| r.pose.get(index as usize).copied())
            .unwrap_or(f32::NAN)
    })
}

#[unsafe(no_mangle)]
pub extern "C" fn combine_poll() -> i32 {
    ADAPTER.with(|a| {
        let mut adapter = a.borrow_mut();
        synchronize_reset(&mut adapter);
        i32::from(adapter.ride.is_some())
    })
}

#[unsafe(no_mangle)]
pub extern "C" fn combine_reset() {
    RESET_GENERATION.fetch_add(1, Ordering::AcqRel);
}

#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_begin(layer: u32, triangles: u32) -> i32 {
    guarded(|a| {
        if a.ride.as_ref().is_some_and(|r| r.surface.refresh_basis().is_none())
            || a.geometry.begin(layer, triangles) != 1 {
            Err(())
        } else {
            Ok(())
        }
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_vertex(x: f32, y: f32, z: f32) -> i32 {
    guarded(|a| {
        if a.ride.as_ref().is_some_and(|r| r.surface.refresh_basis().is_none())
            || a.geometry.vertex([x, y, z]) != 1 {
            Err(())
        } else {
            Ok(())
        }
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_replace(
    x: f32, y: f32, ground: f32, layer: u32, valid: u32,
) -> i32 {
    guarded(|a| {
        let ride = a.ride.as_mut().ok_or(())?;
        let (origin, scale, selected_layer) = ride.surface.refresh_basis().ok_or(())?;
        let xy = [x, y];
        if layer != selected_layer || valid != 1
            || !ride.surface.query_matches_pose(xy, [ride.pose[0], ride.pose[1], ride.pose[2]])
            || !ride.surface.observation(xy, ground, layer, valid) {
            return Err(());
        }
        let (next, _) = a.geometry.finish_at(origin, scale, layer, valid, xy, ground).map_err(|_| ())?;
        if !next.contains_pose([ride.pose[0], ride.pose[1], ride.pose[2]]) {
            return Err(());
        }
        let collision = ride.session.collision_builder().build(next.triangles(), vec![]).map_err(|_| ())?;
        ride.session.install_collision(collision).map_err(|_| ())?;
        ride.surface = next;
        Ok(())
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_mount_surface(
    x: f32,
    y: f32,
    ground: f32,
    heading: f32,
    scale: f32,
    layer: u32,
    valid: u32,
) -> i32 {
    guarded(|a| {
        a.ride = None;
        let (surface, _) = a
            .geometry
            .finish([x, y, ground], scale, layer, valid)
            .map_err(|_| ())?;
        if !heading.is_finite() {
            return Err(());
        }
        start_ride(a, surface, ground, heading)
    })
}
#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_tick_surface(
    now: u32,
    x: f32,
    y: f32,
    ground: f32,
    layer: u32,
    valid: u32,
    packet: *const Packet,
) -> i32 {
    tick_at(now, ground, Some(([x, y], layer, valid)), packet)
}
