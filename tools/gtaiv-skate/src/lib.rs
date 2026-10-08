#[cfg(not(all(windows, target_arch = "x86", target_pointer_width = "32")))]
compile_error!("GTA IV adapter requires x86 Windows");
mod connection;
use connection::{Clock, Surface, gta_heading, skate_heading};
use skate_host::bridge::{Controls, Session};
use std::{
    cell::RefCell,
    ffi::OsString,
    os::windows::ffi::OsStringExt,
    panic::{AssertUnwindSafe, catch_unwind},
    path::PathBuf,
};

struct Ride {
    session: Session,
    surface: Surface,
    clock: Option<Clock>,
    pose: [f32; 4],
}
#[derive(Default)]
struct Adapter {
    points: Vec<[f32; 3]>,
    ride: Option<Ride>,
    assets: Option<PathBuf>,
}
thread_local! { static ADAPTER: RefCell<Adapter> = RefCell::new(Adapter::default()); }
/// ABI packet uses fixed-width fields; XInput's raw Xbox fields need no GTA mapping.
#[repr(C)]
pub struct Packet {
    pub buttons: u16,
    pub left: [i16; 2],
    pub right: [i16; 2],
    pub triggers: [u8; 2],
}
fn guarded(operation: impl FnOnce(&mut Adapter) -> Result<(), ()>) -> i32 {
    let result = catch_unwind(AssertUnwindSafe(|| {
        ADAPTER.with(|a| operation(&mut a.borrow_mut()))
    }));
    if matches!(result, Ok(Ok(()))) {
        1
    } else {
        ADAPTER.with(|a| a.borrow_mut().ride = None);
        0
    }
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_stop() {
    ADAPTER.with(|a| *a.borrow_mut() = Adapter::default());
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
        a.assets = None;
        if plugin_path.is_null() || length == 0 || length >= 32768 {
            return Err(());
        }
        let wide = unsafe { std::slice::from_raw_parts(plugin_path, length as usize) };
        let plugin = PathBuf::from(OsString::from_wide(wide));
        let config = plugin.parent().ok_or(())?.join("combine_skate.assets.txt");
        let content = std::fs::read_to_string(config).map_err(|_| ())?;
        let value = content.trim_start_matches('\u{feff}').trim();
        if value.is_empty() || value.lines().count() != 1 {
            return Err(());
        }
        let root = PathBuf::from(value);
        if !root.is_absolute() || !root.is_dir() {
            return Err(());
        }
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
        let root = a.assets.as_ref().ok_or(())?;
        if !root.is_dir() {
            return Err(());
        }
        let mut session = Session::new(
            root,
            surface.triangles(),
            vec![],
            [0., 1., 0.],
            skate_heading(heading),
        )
        .map_err(|_| ())?;
        let pose = session
            .activate([0., 1., 0.], skate_heading(heading))
            .map_err(|_| ())?;
        let position = surface.to_gta(pose.root.w_axis.truncate().to_array());
        Clock::new(0, session.period()).map_err(|_| ())?;
        if !surface.contains(position, ground) {
            return Err(());
        }
        a.ride = Some(Ride {
            session,
            surface,
            clock: None,
            pose: [position[0], position[1], position[2], heading],
        });
        Ok(())
    })
}
#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_tick(now: u32, ground: f32, packet: *const Packet) -> i32 {
    guarded(|a| {
        if packet.is_null() {
            return Err(());
        }
        let p = unsafe { &*packet };
        let ride = a.ride.as_mut().ok_or(())?;
        if !ride
            .surface
            .contains([ride.pose[0], ride.pose[1], ride.pose[2]], ground)
        {
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
        if !ride.surface.contains(pos, ground) {
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
        a.borrow()
            .ride
            .as_ref()
            .and_then(|r| r.pose.get(index as usize).copied())
            .unwrap_or(f32::NAN)
    })
}
