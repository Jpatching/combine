use crate::connection::{
    Basis, Clock, GeometryBuilder, Rider, Surface, grounded, gta_heading, skate_heading,
};
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
    grounded: bool,
}
#[derive(Default)]
struct Adapter {
    generation: u64,
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
        adapter.geometry = GeometryBuilder::default();
    });
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
fn start_ride(
    a: &mut Adapter,
    triangles: Vec<[[f32; 3]; 3]>,
    basis: Basis,
    rider: Rider,
    heading: f32,
) -> Result<(), ()> {
    let root = a.assets.as_ref().ok_or(())?;
    if !root.is_dir() {
        return Err(());
    }
    // Every mount supplies new collision before activation. Keeping assets
    // warm never permits the previous ride's surface or input to survive.
    let mut idle = a.idle.take();
    let mut created = None;
    let surface = Surface::install(None, triangles, basis, &rider, |floor| match idle.as_mut() {
        Some(session) => {
            let collision = session
                .collision_builder()
                .build(floor.triangles(), vec![])
                .map_err(|_| ())?;
            session.install_collision(collision).map_err(|_| ())
        }
        None => {
            created = Some(
                Session::new(root, floor.triangles(), vec![], [0., 1., 0.], skate_heading(heading))
                    .map_err(|_| ())?,
            );
            Ok(())
        }
    })
    .map_err(|_| ())?;
    let mut session = idle.or(created).ok_or(())?;
    let pose = session
        .activate([0., 1., 0.], skate_heading(heading))
        .map_err(|_| ())?;
    let position = surface.to_gta(pose.root.w_axis.truncate().to_array());
    Clock::new(0, session.period()).map_err(|_| ())?;
    if !surface.contains_pose(position) {
        return Err(());
    }
    a.ride = Some(Ride {
        session,
        surface,
        clock: None,
        pose: [position[0], position[1], position[2], heading],
        grounded: grounded(&pose.state),
    });
    Ok(())
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_value(index: i32) -> f32 {
    ADAPTER.with(|a| {
        let mut adapter = a.borrow_mut();
        synchronize_reset(&mut adapter);
        adapter
            .ride
            .as_ref()
            .and_then(|r| match index {
                0..=3 => Some(r.pose[index as usize]),
                // Skate ground contact at the displayed pose: 1 grounded, 0 airborne.
                4 => Some(f32::from(u8::from(r.grounded))),
                _ => None,
            })
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
    guarded(|a| if a.geometry.begin(layer, triangles) == 1 { Ok(()) } else { Err(()) })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_vertex(x: f32, y: f32, z: f32) -> i32 {
    guarded(|a| if a.geometry.vertex([x, y, z]) == 1 { Ok(()) } else { Err(()) })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_replace(
    x: f32, y: f32, ground: f32, layer: u32, valid: u32,
) -> i32 {
    guarded(|a| {
        let ride = a.ride.as_mut().ok_or(())?;
        let triangles = a.geometry.finish(layer, valid).map_err(|_| ())?;
        let rider = Rider {
            pose: [ride.pose[0], ride.pose[1], ride.pose[2]],
            grounded: ride.grounded,
            query: [x, y],
            ground,
            layer,
            valid,
        };
        let session = &mut ride.session;
        let next = Surface::install(Some(&ride.surface), triangles, ride.surface.basis(), &rider, |floor| {
            let collision = session.collision_builder().build(floor.triangles(), vec![]).map_err(|_| ())?;
            session.install_collision(collision).map_err(|_| ())
        })
        .map_err(|_| ())?;
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
        let triangles = a.geometry.finish(layer, valid).map_err(|_| ())?;
        if !heading.is_finite() {
            return Err(());
        }
        let origin = [x, y, ground];
        let rider = Rider { pose: origin, grounded: true, query: [x, y], ground, layer, valid };
        start_ride(a, triangles, Basis { origin, scale, layer }, rider, heading)
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
    guarded(|a| {
        if packet.is_null() {
            return Err(());
        }
        let p = unsafe { &*packet };
        let ride = a.ride.as_mut().ok_or(())?;
        let rider = Rider {
            pose: [ride.pose[0], ride.pose[1], ride.pose[2]],
            grounded: ride.grounded,
            query: [x, y],
            ground,
            layer,
            valid,
        };
        if !ride.surface.agrees(&rider) {
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
        if !ride.surface.contains_pose(pos) {
            return Err(());
        }
        // Skate root local +Z is forward, GTA heading zero points along +Y.
        let forward = pose.root.z_axis;
        let heading = gta_heading([forward.x, forward.y, forward.z]);
        ride.pose = [pos[0], pos[1], pos[2], heading];
        ride.grounded = grounded(&pose.state);
        Ok(())
    })
}
