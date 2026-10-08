//! Private binary pipe contract. Fixed-size messages are bounded before allocation.
use std::io::{self, Read, Write};
pub const REQUEST_SIZE: usize = 364;
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
    pub points: [[f32; 3]; 25],
    pub buttons: u16,
    pub left: [i16; 2],
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
            points: [[0.; 3]; 25],
            buttons: 0,
            left: [0; 2],
        }
    }
}
#[derive(Clone, Debug)]
pub struct Response {
    pub ride: u64,
    pub sequence: u64,
    pub revision: u64,
    pub pose: [f32; 4],
    pub period: f32,
}
fn invalid() -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, "invalid worker frame")
}
impl Request {
    pub fn write(&self, w: &mut impl Write) -> io::Result<()> {
        let mut b = Vec::with_capacity(REQUEST_SIZE);
        b.extend(self.kind.to_le_bytes());
        for v in [self.ride, self.sequence, self.revision] {
            b.extend(v.to_le_bytes());
        }
        b.extend(self.now.to_le_bytes());
        for v in [self.ground, self.heading, self.scale]
            .into_iter()
            .chain(self.origin)
            .chain(self.points.into_iter().flatten())
        {
            b.extend(v.to_le_bytes());
        }
        b.extend(self.buttons.to_le_bytes());
        for v in self.left {
            b.extend(v.to_le_bytes());
        }
        b.resize(REQUEST_SIZE, 0);
        w.write_all(&b)?;
        w.flush()
    }
    pub fn read(r: &mut impl Read) -> io::Result<Self> {
        let mut b = [0; REQUEST_SIZE];
        r.read_exact(&mut b)?;
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
            points: std::array::from_fn(|i| std::array::from_fn(|j| f(56 + (i * 3 + j) * 4))),
            buttons: u16::from_le_bytes(b[356..358].try_into().unwrap()),
            left: [
                i16::from_le_bytes(b[358..360].try_into().unwrap()),
                i16::from_le_bytes(b[360..362].try_into().unwrap()),
            ],
        };
        if !(1..=3).contains(&request.kind)
            || request.ride == 0
            || request.revision == 0
            || ![request.ground, request.heading, request.scale]
                .iter()
                .chain(request.origin.iter())
                .chain(request.points.iter().flatten())
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
        b.resize(RESPONSE_SIZE, 0);
        w.write_all(&b)?;
        w.flush()
    }
    pub fn read(r: &mut impl Read) -> io::Result<Self> {
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
        };
        if response.ride == 0
            || response.revision == 0
            || !response.pose.iter().all(|v| v.is_finite())
            || !(0.001..=0.1).contains(&response.period)
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
