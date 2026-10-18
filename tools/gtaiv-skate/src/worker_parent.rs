//! GTA commands perform no pipe/process IO; a supervisor owns the child lifetime.
use crate::{
    Packet,
    accepted_pose::AcceptedPose,
    connection::{Basis, GeometryBuilder, Rider, Surface},
    wire::{Request, Response},
};
use std::os::windows::{io::AsRawHandle, process::CommandExt};
use std::{
    path::PathBuf,
    process::{Command, Stdio},
    sync::{
        Arc, Mutex,
        atomic::{AtomicU64, Ordering},
        mpsc::{self, SyncSender},
    },
    time::{Duration, Instant},
};
use windows_sys::Win32::{Foundation::CloseHandle, System::JobObjects::*};
static EPOCH: AtomicU64 = AtomicU64::new(1);
pub fn reset_workers() {
    EPOCH.fetch_add(1, Ordering::AcqRel);
}
struct Job(windows_sys::Win32::Foundation::HANDLE);
impl Job {
    fn new() -> Result<Self, ()> {
        unsafe {
            let handle = CreateJobObjectW(std::ptr::null(), std::ptr::null());
            if handle.is_null() {
                return Err(());
            }
            let mut info: JOBOBJECT_EXTENDED_LIMIT_INFORMATION = std::mem::zeroed();
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
            if SetInformationJobObject(
                handle,
                JobObjectExtendedLimitInformation,
                &info as *const _ as *const _,
                std::mem::size_of_val(&info) as u32,
            ) == 0
            {
                CloseHandle(handle);
                return Err(());
            }
            Ok(Self(handle))
        }
    }
}
impl Drop for Job {
    fn drop(&mut self) {
        unsafe {
            CloseHandle(self.0);
        }
    }
}
struct Snapshot {
    ride: u64,
    revision: u64,
    sequence: u64,
    state: i32,
    pose: [f32; 4],
    grounded: bool,
    updated: Instant,
}
struct Bridge {
    epoch: u64,
    sender: SyncSender<Request>,
    generation: Arc<AtomicU64>,
    snapshot: Arc<Mutex<Snapshot>>,
    ride: u64,
    sequence: u64,
    revision: u64,
}
impl Bridge {
    fn start(exe: PathBuf) -> Self {
        let epoch = EPOCH.load(Ordering::Acquire);
        let (tx, rx) = mpsc::sync_channel::<Request>(1);
        let generation = Arc::new(AtomicU64::new(0));
        let snapshot = Arc::new(Mutex::new(Snapshot {
            ride: 0,
            revision: 0,
            sequence: 0,
            state: 0,
            pose: [f32::NAN; 4],
            grounded: false,
            updated: Instant::now(),
        }));
        let shared = snapshot.clone();
        let token = generation.clone();
        std::thread::spawn(move || {
            let Ok(job) = Job::new() else {
                shared.lock().unwrap().state = 0;
                return;
            };
            let mut child: Option<std::process::Child> = None;
            let mut writes: Option<SyncSender<Request>> = None;
            let mut writer: Option<std::thread::JoinHandle<()>> = None;
            let mut responses = None;
            let mut active = false;
            loop {
                if EPOCH.load(Ordering::Acquire) != epoch {
                    break;
                }
                let request = match rx.recv_timeout(Duration::from_millis(10)) {
                    Ok(request) => request,
                    Err(mpsc::RecvTimeoutError::Timeout) => continue,
                    Err(mpsc::RecvTimeoutError::Disconnected) => break,
                };
                let success = (|| -> Result<Response, ()> {
                    if request.kind == 1 && active {
                        if let Some(mut owned) = child.take() {
                            let _ = owned.kill();
                            let _ = owned.wait();
                        }
                        writes = None;
                        if let Some(owned) = writer.take() {
                            let _ = owned.join();
                        }
                        responses = None;
                        active = false;
                    }
                    if child.is_none() && request.kind == 3 {
                        return Err(());
                    }
                    if child.is_none() {
                        let mut spawned = Command::new(&exe)
                            .creation_flags(0x08000000)
                            .stdin(Stdio::piped())
                            .stdout(Stdio::piped())
                            .stderr(Stdio::null())
                            .spawn()
                            .map_err(|_| ())?;
                        if unsafe { AssignProcessToJobObject(job.0, spawned.as_raw_handle()) } == 0
                        {
                            let _ = spawned.kill();
                            let _ = spawned.wait();
                            return Err(());
                        }
                        let mut stdin = spawned.stdin.take().ok_or(())?;
                        let (write_tx, write_rx) = mpsc::sync_channel::<Request>(1);
                        // A large prepare frame can exceed the pipe buffer. Keep writes off
                        // the supervisor so its deadline/cancellation can kill a stalled child.
                        writer = Some(std::thread::spawn(move || {
                            while let Ok(request) = write_rx.recv() {
                                if request.write(&mut stdin).is_err() {
                                    break;
                                }
                            }
                        }));
                        writes = Some(write_tx);
                        let mut stdout = spawned.stdout.take().ok_or(())?;
                        let (tx, rx) = mpsc::sync_channel(1);
                        std::thread::spawn(move || {
                            loop {
                                let value = Response::read(&mut stdout);
                                let failed = value.is_err();
                                if tx.send(value).is_err() || failed {
                                    break;
                                }
                            }
                        });
                        responses = Some(rx);
                        child = Some(spawned);
                    }
                    writes
                        .as_ref()
                        .ok_or(())?
                        .try_send(request.clone())
                        .map_err(|_| ())?;
                    let started = Instant::now();
                    let limit = if request.kind == 1 {
                        Duration::from_secs(60)
                    } else {
                        Duration::from_millis(250)
                    };
                    loop {
                        if EPOCH.load(Ordering::Acquire) != epoch
                            || request.kind != 3 && token.load(Ordering::Acquire) != request.ride
                        {
                            return Err(());
                        }
                        if started.elapsed() > limit {
                            return Err(());
                        }
                        match responses
                            .as_ref()
                            .ok_or(())?
                            .recv_timeout(Duration::from_millis(10))
                        {
                            Ok(Ok(response)) if response.matches(&request) => return Ok(response),
                            Ok(_) => return Err(()),
                            Err(mpsc::RecvTimeoutError::Disconnected) => return Err(()),
                            Err(mpsc::RecvTimeoutError::Timeout) => {}
                        }
                    }
                })();
                if let Ok(response) = success {
                    active = request.kind != 3;
                    if token.load(Ordering::Acquire) == request.ride && request.kind != 3 {
                        let mut state = shared.lock().unwrap();
                        state.ride = response.ride;
                        state.revision = response.revision;
                        state.sequence = response.sequence;
                        state.state = 1;
                        state.pose = response.pose;
                        state.grounded = response.grounded;
                        state.updated = Instant::now();
                    }
                } else {
                    if let Some(mut owned) = child.take() {
                        let _ = owned.kill();
                        let _ = owned.wait();
                    }
                    writes = None;
                    // Killing the child closes the blocked pipe; dropping the bounded
                    // channel wakes an idle writer before waiting for its termination.
                    if let Some(owned) = writer.take() {
                        let _ = owned.join();
                    }
                    responses = None;
                    active = false;
                    if token.load(Ordering::Acquire) == request.ride {
                        let mut state = shared.lock().unwrap();
                        state.ride = request.ride;
                        state.revision = request.revision;
                        state.state = 0;
                    }
                }
            }
            if let Some(mut owned) = child {
                let _ = owned.kill();
                let _ = owned.wait();
            }
            drop(writes);
            if let Some(owned) = writer {
                let _ = owned.join();
            }
        });
        Self {
            epoch,
            sender: tx,
            generation,
            snapshot,
            ride: 0,
            sequence: 0,
            revision: 0,
        }
    }
}
#[derive(Default)]
pub struct Adapter {
    geometry: GeometryBuilder,
    exe: Option<PathBuf>,
    bridge: Option<Bridge>,
    surface: Option<Surface>,
    pose: [f32; 4],
    /// Skate ground contact at the displayed pose.
    grounded: bool,
    deferred: Option<Request>,
    pending_surface: Option<(Surface, u64, Instant)>,
    accepted: Option<AcceptedPose>,
}
impl Adapter {
    pub fn config(&mut self, path: PathBuf) {
        if self
            .bridge
            .as_ref()
            .is_some_and(|b| b.epoch != EPOCH.load(Ordering::Acquire))
        {
            self.bridge = None;
            self.surface = None;
            self.pose = [f32::NAN; 4];
            self.accepted = None;
            self.pending_surface = None;
        }
        self.exe = path.parent().map(|p| p.join("combine_skate_worker.exe"));
    }
    pub fn stop(&mut self) {
        self.deferred = None;
        self.pending_surface = None;
        let active = self.surface.take().is_some();
        self.geometry = GeometryBuilder::default();
        self.pose = [f32::NAN; 4];
        self.accepted = None;
        if !active {
            return;
        }
        if let Some(b) = self.bridge.as_mut() {
            let old = b.ride;
            b.ride = b.ride.checked_add(1).unwrap_or(0);
            b.generation.store(b.ride, Ordering::Release);
            // Cancellation of an in-flight request kills that owned child. Idle warm stop
            // is sent under its old identity before advancing the next prepare generation.
            let request = Request {
                kind: 3,
                ride: old,
                revision: b.revision,
                ..Request::default()
            };
            let _ = b.sender.try_send(request);
            if let Ok(mut s) = b.snapshot.try_lock() {
                s.state = 0;
                s.pose = [f32::NAN; 4];
            }
        }
    }
    pub fn surface_begin(&mut self, layer: u32, triangles: u32) -> i32 {
        if self.pending_surface.is_some() {
            return 0;
        }
        self.geometry.begin(layer, triangles)
    }
    pub fn surface_vertex(&mut self, p: [f32; 3]) -> i32 {
        if self.pending_surface.is_some() {
            return 0;
        }
        self.geometry.vertex(p)
    }
    pub fn mount_surface(
        &mut self,
        origin: [f32; 3],
        heading: f32,
        scale: f32,
        layer: u32,
        valid: u32,
    ) -> i32 {
        let Ok(triangles) = self.geometry.finish(layer, valid) else {
            return 0;
        };
        if !heading.is_finite() {
            return 0;
        }
        let basis = Basis { origin, scale, layer };
        let query = [origin[0], origin[1]];
        let rider = Rider { pose: origin, grounded: true, query, ground: origin[2], layer, valid };
        // The worker installs; this side qualifies the floor and submits it.
        match Surface::install(None, triangles, basis, &rider, |floor| self.prepare(floor, heading)) {
            Ok(surface) => {
                self.surface = Some(surface);
                2
            }
            Err(_) => 0,
        }
    }
    fn prepare(&mut self, floor: &Surface, heading: f32) -> Result<(), ()> {
        if self.bridge.is_none() {
            self.bridge = Some(Bridge::start(self.exe.clone().ok_or(())?));
        }
        let b = self.bridge.as_mut().unwrap();
        b.ride = b.ride.checked_add(1).ok_or(())?;
        b.revision = b.revision.checked_add(1).ok_or(())?;
        b.sequence = 0;
        let Basis { origin, scale, layer } = floor.basis();
        let request = Request {
            kind: 1,
            ride: b.ride,
            revision: b.revision,
            origin,
            ground: origin[2],
            heading,
            scale,
            layer,
            valid: 1,
            query: [origin[0], origin[1]],
            triangles: floor.host_triangles().to_vec(),
            ..Request::default()
        };
        b.generation.store(b.ride, Ordering::Release);
        if let Ok(mut s) = b.snapshot.try_lock() {
            s.ride = b.ride;
            s.revision = b.revision;
            s.state = 2;
            s.pose = [f32::NAN; 4];
        }
        self.pose = [f32::NAN; 4];
        self.accepted = None;
        self.pending_surface = None;
        match b.sender.try_send(request) {
            Ok(()) => Ok(()),
            Err(mpsc::TrySendError::Full(request)) => {
                self.deferred = Some(request);
                Ok(())
            }
            Err(mpsc::TrySendError::Disconnected(_)) => Err(()),
        }
    }
    pub fn poll(&mut self) -> i32 {
        if self.surface.is_none() {
            return 0;
        }
        if let Some(b) = self.bridge.as_ref() {
            if b.epoch != EPOCH.load(Ordering::Acquire) {
                return 0;
            }
            if let Some(request) = self.deferred.take() {
                match b.sender.try_send(request) {
                    Ok(()) => {}
                    Err(mpsc::TrySendError::Full(request)) => {
                        self.deferred = Some(request);
                        return 2;
                    }
                    Err(mpsc::TrySendError::Disconnected(_)) => return 0,
                }
            }
            match b.snapshot.try_lock() {
                Ok(s) => {
                    if s.ride != b.ride || s.revision != b.revision {
                        return 2;
                    }
                    if s.state == 1 && s.updated.elapsed() > Duration::from_millis(250) {
                        return 0;
                    }
                    if let Some((_, sequence, started)) = self.pending_surface.as_ref() {
                        if s.state == 0 || started.elapsed() > Duration::from_millis(500) {
                            return 0;
                        }
                        if s.sequence < *sequence {
                            return 2;
                        }
                        let (next, _, _) = self.pending_surface.take().unwrap();
                        self.surface = Some(next);
                    }
                    self.pose = s.pose;
                    self.grounded = s.grounded;
                    if s.state == 1 {
                        self.accepted = AcceptedPose::new(
                            s.ride, s.revision, b.epoch, s.pose, s.grounded, s.updated,
                        );
                    }
                    return s.state;
                }
                Err(std::sync::TryLockError::Poisoned(_)) => return 0,
                Err(std::sync::TryLockError::WouldBlock) => {}
            }
        }
        2
    }
    pub fn value(&self, index: i32) -> f32 {
        match index {
            0..=3 => self.pose[index as usize],
            // Skate ground contact at the displayed pose: 1 grounded, 0 airborne.
            4 if self.pose[0].is_finite() => f32::from(u8::from(self.grounded)),
            _ => f32::NAN,
        }
    }
    pub fn tick_surface(
        &mut self,
        now: u32,
        xy: [f32; 2],
        ground: f32,
        layer: u32,
        valid: u32,
        p: &Packet,
    ) -> i32 {
        self.tick_at(now, xy, ground, layer, valid, p)
    }
    pub fn surface_replace(&mut self, xy: [f32; 2], ground: f32, layer: u32, valid: u32) -> i32 {
        if self.pending_surface.is_some() || self.deferred.is_some() { return 0; }
        let Some(bridge) = self.bridge.as_ref() else { return 0; };
        if bridge.epoch != EPOCH.load(Ordering::Acquire) { return 0; }
        match bridge.snapshot.try_lock() {
            Ok(snapshot) if snapshot.state == 1 && snapshot.ride == bridge.ride
                && snapshot.revision == bridge.revision => {
                if snapshot.sequence != bridge.sequence || snapshot.pose != self.pose { return 3; }
            }
            Err(std::sync::TryLockError::WouldBlock) => return 3,
            _ => return 0,
        }
        // Consume the staged upload only once the worker has caught up with the
        // displayed pose; a retry (3) keeps it for the next frame.
        let Ok(triangles) = self.geometry.finish(layer, valid) else { return 0; };
        let rider = Rider {
            pose: [self.pose[0], self.pose[1], self.pose[2]],
            grounded: self.grounded,
            query: xy,
            ground,
            layer,
            valid,
        };
        let Self { surface: Some(old), bridge: Some(b), .. } = &mut *self else { return 0; };
        let mut submitted = None;
        let next = Surface::install(Some(old), triangles, old.basis(), &rider, |floor| {
            let sequence = b.sequence.checked_add(1).ok_or(())?;
            let Basis { origin, scale, layer } = floor.basis();
            let request = Request { kind: 4, ride: b.ride, sequence, revision: b.revision,
                origin, scale, query: xy, ground, layer, valid,
                triangles: floor.host_triangles().to_vec(), ..Request::default() };
            b.sender.try_send(request).map_err(|_| ())?;
            b.sequence = sequence;
            submitted = Some(sequence);
            Ok::<_, ()>(())
        });
        match (next, submitted) {
            (Ok(next), Some(sequence)) => { self.pending_surface = Some((next, sequence, Instant::now())); 2 }
            _ => 0,
        }
    }
    fn tick_at(
        &mut self,
        now: u32,
        xy: [f32; 2],
        ground: f32,
        layer: u32,
        valid: u32,
        p: &Packet,
    ) -> i32 {
        if self.pending_surface.is_some() {
            if self.poll() != 1 { return 0; }
        }
        let Some(b) = self.bridge.as_mut() else {
            return 0;
        };
        if b.epoch != EPOCH.load(Ordering::Acquire) {
            return 0;
        }
        let Some(surface) = self.surface.as_ref() else {
            return 0;
        };
        if !surface.query_matches_pose(xy, [self.pose[0], self.pose[1], self.pose[2]]) {
            return 0;
        }
        let candidate = match b.snapshot.try_lock() {
            Ok(s) => {
                if s.ride != b.ride || s.revision != b.revision || s.state != 1 {
                    self.accepted = None;
                    return 0;
                }
                self.accepted =
                    AcceptedPose::new(s.ride, s.revision, b.epoch, s.pose, s.grounded, s.updated);
                self.accepted.as_ref().and_then(|pose| {
                    pose.fresh(b.ride, b.revision, b.epoch, Instant::now(), surface, xy, ground, layer, valid)
                })
            }
            Err(std::sync::TryLockError::WouldBlock) => self.accepted.as_ref().and_then(|pose| {
                pose.fresh(b.ride, b.revision, b.epoch, Instant::now(), surface, xy, ground, layer, valid)
            }),
            Err(std::sync::TryLockError::Poisoned(_)) => return 0,
        };
        let Some(pose) = candidate else {
            return 0;
        };
        self.pose = pose;
        self.grounded = self.accepted.is_some_and(|a| a.grounded());
        let sequence = match b.sequence.checked_add(1) {
            Some(v) => v,
            None => return 0,
        };
        let request = Request {
            kind: 2,
            ride: b.ride,
            sequence,
            revision: b.revision,
            now,
            ground,
            query: xy,
            layer,
            valid,
            buttons: p.buttons,
            left: p.left,
            ..Request::default()
        };
        match b.sender.try_send(request) {
            Ok(()) => b.sequence = sequence,
            Err(mpsc::TrySendError::Full(_)) => {}
            Err(_) => return 0,
        };
        1
    }
}
