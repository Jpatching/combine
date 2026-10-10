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
