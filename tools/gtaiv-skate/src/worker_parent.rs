//! GTA commands perform no pipe/process IO; a supervisor owns the child lifetime.
use crate::{
    Packet,
    accepted_pose::AcceptedPose,
    connection::Surface,
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
    state: i32,
    pose: [f32; 4],
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
            state: 0,
            pose: [f32::NAN; 4],
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
            let mut stdin = None;
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
                        stdin = None;
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
                        stdin = spawned.stdin.take();
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
                    request.write(stdin.as_mut().ok_or(())?).map_err(|_| ())?;
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
                        state.state = 1;
                        state.pose = response.pose;
                        state.updated = Instant::now();
                    }
                } else {
                    if let Some(mut owned) = child.take() {
                        let _ = owned.kill();
                        let _ = owned.wait();
                    }
                    stdin = None;
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
    points: Vec<[f32; 3]>,
    exe: Option<PathBuf>,
    bridge: Option<Bridge>,
    surface: Option<Surface>,
    pose: [f32; 4],
    deferred: Option<Request>,
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
        }
        self.exe = path.parent().map(|p| p.join("combine_skate_worker.exe"));
    }
    pub fn stop(&mut self) {
        self.deferred = None;
        let active = self.surface.take().is_some();
        self.points.clear();
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
    pub fn vertex(&mut self, p: [f32; 3]) -> i32 {
        if self.points.len() >= 25 || !p.iter().all(|v| v.is_finite()) {
            0
        } else {
            self.points.push(p);
            1
        }
    }
    pub fn mount(&mut self, origin: [f32; 3], heading: f32, scale: f32) -> i32 {
        let points: [[f32; 3]; 25] = match self.points.clone().try_into() {
            Ok(v) => v,
            Err(_) => return 0,
        };
        let Ok(surface) = Surface::new(std::mem::take(&mut self.points), origin, scale) else {
            return 0;
        };
        if !heading.is_finite() {
            return 0;
        }
        if self.bridge.is_none() {
            let Some(exe) = self.exe.clone() else {
                return 0;
            };
            self.bridge = Some(Bridge::start(exe));
        }
        let b = self.bridge.as_mut().unwrap();
        b.ride = match b.ride.checked_add(1) {
            Some(v) => v,
            None => return 0,
        };
        b.revision = match b.revision.checked_add(1) {
            Some(v) => v,
            None => return 0,
        };
        b.sequence = 0;
        let request = Request {
            kind: 1,
            ride: b.ride,
            revision: b.revision,
            origin,
            ground: origin[2],
            heading,
            scale,
            points,
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
        match b.sender.try_send(request) {
            Ok(()) => {}
            Err(mpsc::TrySendError::Full(request)) => self.deferred = Some(request),
            Err(mpsc::TrySendError::Disconnected(_)) => return 0,
        }
        self.surface = Some(surface);
        2
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
                    self.pose = s.pose;
                    if s.state == 1 {
                        self.accepted =
                            AcceptedPose::new(s.ride, s.revision, b.epoch, s.pose, s.updated);
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
        self.pose.get(index as usize).copied().unwrap_or(f32::NAN)
    }
    pub fn tick(&mut self, now: u32, ground: f32, p: &Packet) -> i32 {
        let Some(b) = self.bridge.as_mut() else {
            return 0;
        };
        if b.epoch != EPOCH.load(Ordering::Acquire) {
            return 0;
        }
        let Some(surface) = self.surface.as_ref() else {
            return 0;
        };
        let candidate = match b.snapshot.try_lock() {
            Ok(s) => {
                if s.ride != b.ride || s.revision != b.revision || s.state != 1 {
                    self.accepted = None;
                    return 0;
                }
                self.accepted = AcceptedPose::new(s.ride, s.revision, b.epoch, s.pose, s.updated);
                self.accepted.as_ref().and_then(|pose| {
                    pose.fresh(b.ride, b.revision, b.epoch, Instant::now(), ground, surface)
                })
            }
            Err(std::sync::TryLockError::WouldBlock) => self.accepted.as_ref().and_then(|pose| {
                pose.fresh(b.ride, b.revision, b.epoch, Instant::now(), ground, surface)
            }),
            Err(std::sync::TryLockError::Poisoned(_)) => return 0,
        };
        let Some(pose) = candidate else {
            return 0;
        };
        self.pose = pose;
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
