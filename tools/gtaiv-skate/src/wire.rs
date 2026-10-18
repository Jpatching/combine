//! Private binary pipe contract. Fixed-size messages are bounded before allocation.
use crate::connection::MAX_TRIANGLES;
use std::io::{self, Read, Write};
pub const REQUEST_SIZE: usize = 96;
const MAGIC: u32 = 0x32534b43;
const VERSION: u32 = 4;
const HEADER: usize = 12;
/// Offset of the triangle count; triangles follow it.
const COUNT: usize = 80;
pub const RESPONSE_SIZE: usize = 48;
#[derive(Clone, Debug)]
pub struct Request {
    pub kind: u32,
    pub ride: u64,
    pub sequence: u64,
    pub revision: u64,
    pub now: u32,
    pub ground: f32,
    pub heading: f32,
    pub scale: f32,
    pub origin: [f32; 3],
    pub buttons: u16,
    pub left: [i16; 2],
    pub query: [f32; 2],
    pub layer: u32,
    pub valid: u32,
    pub triangles: Vec<[[f32; 3]; 3]>,
}
impl Default for Request {
    fn default() -> Self {
        Self {
            kind: 0,
            ride: 0,
            sequence: 0,
            revision: 0,
            now: 0,
            ground: 0.,
            heading: 0.,
            scale: 1.,
            origin: [0.; 3],
            buttons: 0,
            left: [0; 2],
            query: [0.; 2],
            layer: 0,
            valid: 0,
            triangles: vec![],
        }
    }
}
#[derive(Clone, Debug)]
pub struct Response {
    pub ride: u64,
    pub sequence: u64,
    pub revision: u64,
    pub pose: [f32; 4],
    /// Skate reported ground contact at this pose.
    pub grounded: bool,
    pub period: f32,
}
fn invalid() -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, "invalid worker frame")
}
/// Prepare (1) and replace (4) carry a floor; every frame but stop (3) names its layer.
fn carries_floor(kind: u32) -> bool {
    matches!(kind, 1 | 4)
}
impl Request {
    pub fn write(&self, w: &mut impl Write) -> io::Result<()> {
        if self.triangles.len() > MAX_TRIANGLES || !carries_floor(self.kind) && !self.triangles.is_empty() {
            return Err(invalid());
        }
        let mut b = Vec::with_capacity(REQUEST_SIZE + self.triangles.len() * 36);
        b.extend(self.kind.to_le_bytes());
        for v in [self.ride, self.sequence, self.revision] {
            b.extend(v.to_le_bytes());
        }
        b.extend(self.now.to_le_bytes());
        for v in [self.ground, self.heading, self.scale].into_iter().chain(self.origin) {
            b.extend(v.to_le_bytes());
        }
        b.extend(self.buttons.to_le_bytes());
        for v in self.left {
            b.extend(v.to_le_bytes());
        }
        b.resize(64, 0);
        for v in self.query {
            b.extend(v.to_le_bytes());
        }
        b.extend(self.layer.to_le_bytes());
        b.extend(self.valid.to_le_bytes());
        b.extend((self.triangles.len() as u32).to_le_bytes());
        for v in self.triangles.iter().flatten().flatten() {
            b.extend(v.to_le_bytes());
        }
        write_header(w, b.len())?;
        w.write_all(&b)?;
        w.flush()
    }
    pub fn read(r: &mut impl Read) -> io::Result<Self> {
        let size = read_header(r)?;
        if size < REQUEST_SIZE - HEADER || size > REQUEST_SIZE - HEADER + MAX_TRIANGLES * 36 {
            return Err(invalid());
        }
        let mut b = vec![0; size];
        r.read_exact(&mut b)?;
        let count = u32::from_le_bytes(b[COUNT..COUNT + 4].try_into().unwrap()) as usize;
        if count > MAX_TRIANGLES || size != REQUEST_SIZE - HEADER + count * 36 {
            return Err(invalid());
        }
        let u32at = |i| u32::from_le_bytes(b[i..i + 4].try_into().unwrap());
        let u64at = |i| u64::from_le_bytes(b[i..i + 8].try_into().unwrap());
        let f = |i| f32::from_le_bytes(b[i..i + 4].try_into().unwrap());
        let request = Self {
            kind: u32at(0),
            ride: u64at(4),
            sequence: u64at(12),
            revision: u64at(20),
            now: u32at(28),
            ground: f(32),
            heading: f(36),
            scale: f(40),
            origin: std::array::from_fn(|i| f(44 + i * 4)),
            buttons: u16::from_le_bytes(b[56..58].try_into().unwrap()),
            left: [
                i16::from_le_bytes(b[58..60].try_into().unwrap()),
                i16::from_le_bytes(b[60..62].try_into().unwrap()),
            ],
            query: [f(64), f(68)],
            layer: u32at(72),
            valid: u32at(76),
            triangles: (0..count)
                .map(|i| {
                    std::array::from_fn(|j| {
                        std::array::from_fn(|k| f(COUNT + 4 + i * 36 + j * 12 + k * 4))
                    })
                })
                .collect(),
        };
        if !(1..=4).contains(&request.kind)
            || carries_floor(request.kind) != (count != 0)
            || request.kind != 3 && (request.layer == 0 || request.valid != 1)
            || request.ride == 0
            || request.revision == 0
            || ![request.ground, request.heading, request.scale]
                .iter()
                .chain(request.origin.iter())
                .chain(request.query.iter())
                .chain(request.triangles.iter().flatten().flatten())
                .all(|v| v.is_finite())
        {
            return Err(invalid());
        }
        Ok(request)
    }
}
impl Response {
    pub fn write(&self, w: &mut impl Write) -> io::Result<()> {
        let mut b = Vec::with_capacity(RESPONSE_SIZE);
        for v in [self.ride, self.sequence, self.revision] {
            b.extend(v.to_le_bytes());
        }
        for v in self.pose.into_iter().chain([self.period]) {
            b.extend(v.to_le_bytes());
        }
        b.extend(u32::from(self.grounded).to_le_bytes());
        b.resize(RESPONSE_SIZE, 0);
        write_header(w, RESPONSE_SIZE)?;
        w.write_all(&b)?;
        w.flush()
    }
    pub fn read(r: &mut impl Read) -> io::Result<Self> {
        if read_header(r)? != RESPONSE_SIZE {
            return Err(invalid());
        }
        let mut b = [0; RESPONSE_SIZE];
        r.read_exact(&mut b)?;
        let u = |i| u64::from_le_bytes(b[i..i + 8].try_into().unwrap());
        let f = |i| f32::from_le_bytes(b[i..i + 4].try_into().unwrap());
        let response = Self {
            ride: u(0),
            sequence: u(8),
            revision: u(16),
            pose: std::array::from_fn(|i| f(24 + i * 4)),
            period: f(40),
            grounded: u32::from_le_bytes(b[44..48].try_into().unwrap()) == 1,
        };
        if response.ride == 0
            || response.revision == 0
            || !response.pose.iter().all(|v| v.is_finite())
            || !(0.001..=0.1).contains(&response.period)
            || u32::from_le_bytes(b[44..48].try_into().unwrap()) > 1
        {
            return Err(invalid());
        }
        Ok(response)
    }
    pub fn matches(&self, request: &Request) -> bool {
        self.ride == request.ride
            && self.revision == request.revision
            && self.sequence == request.sequence
    }
}

fn write_header(w: &mut impl Write, size: usize) -> io::Result<()> {
    for v in [MAGIC, VERSION, size as u32] {
        w.write_all(&v.to_le_bytes())?;
    }
    Ok(())
}
fn read_header(r: &mut impl Read) -> io::Result<usize> {
    let mut header = [0; 12];
    r.read_exact(&mut header)?;
    let u = |i| u32::from_le_bytes(header[i..i + 4].try_into().unwrap());
    if u(0) != MAGIC || u(4) != VERSION {
        return Err(invalid());
    }
    Ok(u(8) as usize)
}
