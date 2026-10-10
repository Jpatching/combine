use crate::{Packet, worker_parent::Adapter};
use std::{
    cell::RefCell,
    ffi::OsString,
    os::windows::ffi::OsStringExt,
    panic::{AssertUnwindSafe, catch_unwind},
    path::PathBuf,
};
thread_local! {static ADAPTER:RefCell<Adapter>=RefCell::new(Adapter::default());}
fn guarded(f: impl FnOnce(&mut Adapter) -> i32) -> i32 {
    catch_unwind(AssertUnwindSafe(|| {
        ADAPTER.with(|a| f(&mut a.borrow_mut()))
    }))
    .unwrap_or(0)
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_stop() {
    guarded(|a| {
        a.stop();
        1
    });
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_vertex(x: f32, y: f32, z: f32) -> i32 {
    guarded(|a| a.vertex([x, y, z]))
}
#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_config(path: *const u16, length: u32) -> i32 {
    if path.is_null() || length == 0 || length >= 32768 {
        return 0;
    }
    let path = PathBuf::from(OsString::from_wide(unsafe {
        std::slice::from_raw_parts(path, length as usize)
    }));
    guarded(|a| {
        a.config(path);
        1
    })
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_mount(x: f32, y: f32, z: f32, heading: f32, scale: f32) -> i32 {
    guarded(|a| a.mount([x, y, z], heading, scale))
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_poll() -> i32 {
    guarded(|a| a.poll())
}
#[unsafe(no_mangle)]
pub unsafe extern "C" fn combine_tick(now: u32, ground: f32, packet: *const Packet) -> i32 {
    if packet.is_null() {
        return 0;
    }
    guarded(|a| a.tick(now, ground, unsafe { &*packet }))
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_value(index: i32) -> f32 {
    ADAPTER.with(|a| a.borrow().value(index))
}

#[unsafe(no_mangle)]
pub extern "C" fn combine_reset() {
    crate::worker_parent::reset_workers();
}

#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_begin(layer: u32, triangles: u32) -> i32 {
    guarded(|a| a.surface_begin(layer, triangles))
}
#[unsafe(no_mangle)]
pub extern "C" fn combine_surface_vertex(x: f32, y: f32, z: f32) -> i32 {
    guarded(|a| a.surface_vertex([x, y, z]))
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
    guarded(|a| a.mount_surface([x, y, ground], heading, scale, layer, valid))
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
    if packet.is_null() {
        return 0;
    }
    guarded(|a| a.tick_surface(now, [x, y], ground, layer, valid, unsafe { &*packet }))
}
