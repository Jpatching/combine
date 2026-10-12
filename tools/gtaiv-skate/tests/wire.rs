#[path = "../src/wire.rs"]
mod wire;
use wire::*;
#[test]
fn bridge_preserves_collision_input_and_identity() {
    let mut request = Request {
        kind: 1,
        ride: 7,
        revision: 9,
        sequence: 3,
        buttons: 0x4000,
        left: [-12000, 3000],
        ..Request::default()
    };
    request.points[24] = [14., 16., 10.];
    let mut bytes = Vec::new();
    request.write(&mut bytes).unwrap();
    assert_eq!(bytes.len(), REQUEST_SIZE);
    let decoded = Request::read(&mut &bytes[..]).unwrap();
    assert_eq!(decoded.points[24], [14., 16., 10.]);
    assert_eq!(decoded.left, [-12000, 3000]);
    let response = Response {
        ride: 7,
        revision: 9,
        sequence: 3,
        pose: [1., 2., 3., 90.],
        period: 1. / 60.,
    };
    assert!(response.matches(&decoded));
    request.ride = 8;
    assert!(!response.matches(&request));
    request.ride = 7;
    request.sequence = 4;
    assert!(!response.matches(&request));
    request.sequence = 3;
    request.revision = 10;
    assert!(!response.matches(&request));
}
#[test]
fn bridge_refuses_truncated_and_nonfinite_output() {
    assert!(Response::read(&mut &[0u8; 2][..]).is_err());
    let response = Response {
        ride: 1,
        revision: 1,
        sequence: 0,
        pose: [f32::NAN, 0., 0., 0.],
        period: 1. / 60.,
    };
    let mut bytes = Vec::new();
    response.write(&mut bytes).unwrap();
    assert!(Response::read(&mut &bytes[..]).is_err());
}
#[test]
fn geometry_prepare_preserves_observation_and_ticks_do_not_repeat_geometry() {
    let request = Request {
        kind: 1,
        ride: 1,
        revision: 1,
        layer: 7,
        valid: 1,
        query: [6., 2.],
        ground: 1.5,
        triangles: vec![[[0., 0., 0.], [8., 0., 2.], [0., 8., 0.]]],
        ..Request::default()
    };
    let mut bytes = vec![];
    request.write(&mut bytes).unwrap();
    let decoded = Request::read(&mut &bytes[..]).unwrap();
    assert_eq!(decoded.query, [6., 2.]);
    assert_eq!(decoded.layer, 7);
    assert_eq!(decoded.triangles, request.triangles);
    let tick = Request {
        kind: 2,
        triangles: vec![],
        ..request.clone()
    };
    let mut tick_bytes = vec![];
    tick.write(&mut tick_bytes).unwrap();
    assert_eq!(bytes.len() - tick_bytes.len(), 36);
    assert!(Request { kind: 2, ..request }.write(&mut vec![]).is_err());
    assert!(Request::read(&mut &[0u8; 364][..]).is_err());
}
#[test]
fn geometry_frames_refuse_oversize_payloads_wrong_version_and_invalid_observations() {
    let request = Request {
        kind: 1,
        ride: 1,
        revision: 1,
        layer: 7,
        valid: 1,
        triangles: vec![[[0., 0., 0.], [8., 0., 2.], [0., 8., 0.]]],
        ..Request::default()
    };
    assert!(
        Request {
            triangles: vec![[[0.; 3]; 3]; 4097],
            ..request.clone()
        }
        .write(&mut vec![])
        .is_err()
    );
    let mut bytes = vec![];
    request.write(&mut bytes).unwrap();
    bytes[4] = 1;
    assert!(Request::read(&mut &bytes[..]).is_err());
    bytes[4] = 2;
    bytes[8..12].copy_from_slice(&u32::MAX.to_le_bytes());
    assert!(Request::read(&mut &bytes[..]).is_err());
    let mut invalid = vec![];
    Request {
        valid: 0,
        ..request
    }
    .write(&mut invalid)
    .unwrap();
    assert!(Request::read(&mut &invalid[..]).is_err());
}
