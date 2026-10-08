#[cfg(not(all(windows, target_arch = "x86", target_pointer_width = "32")))]
compile_error!("GTA IV adapter requires x86 Windows");
mod connection;
#[cfg(not(feature = "worker"))]
mod in_process;
#[cfg(feature = "worker")]
mod wire;
#[cfg(feature = "worker")]
mod worker_abi;
#[cfg(feature = "worker")]
mod worker_parent;
#[repr(C)]
pub struct Packet {
    pub buttons: u16,
    pub left: [i16; 2],
    pub right: [i16; 2],
    pub triggers: [u8; 2],
}
