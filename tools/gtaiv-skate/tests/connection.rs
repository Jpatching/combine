#[path = "../src/connection.rs"]
mod connection;
use connection::*;
#[test]
fn ground_patch_matches_gta_axes_and_rejects_leaving_selected_surface() {
    let points = (0..25)
        .map(|i| [100. + (i % 5) as f32 * 2., 200. + (i / 5) as f32 * 2., 10.])
        .collect();
    let patch = Surface::new(points, [104., 204., 10.], 1.).unwrap();
    assert_eq!(patch.to_skate([106., 207., 12.]), [2., 2., -3.]);
    assert_eq!(patch.to_gta([2., 2., -3.]), [106., 207., 12.]);
    assert!(patch.contains([107., 207., 10.], 10.));
    assert!(!patch.contains([109., 207., 10.], 10.));
    assert!(!patch.contains([107., 207., 10.], 15.));
    assert_eq!(patch.triangles().len(), 32);
}
#[test]
fn clock_advances_fixed_ticks_and_abandons_long_or_reversed_frames() {
    let mut clock = Clock::new(1000, 0.01).unwrap();
    assert_eq!(clock.steps(1004).unwrap(), 0);
    assert_eq!(clock.steps(1025).unwrap(), 2);
    assert_eq!(clock.steps(1030).unwrap(), 1);
    assert!(clock.steps(2000).is_err());
    let mut clock = Clock::new(1000, 0.01).unwrap();
    assert!(clock.steps(999).is_err());
}
#[test]
fn gta_cardinal_headings_preserve_skate_forward_orientation() {
    // GTA heading 0 faces north (+Y); 90 faces west (-X).
    for (heading, forward) in [
        (0., [0., 0., -1.]),
        (90., [-1., 0., 0.]),
        (180., [0., 0., 1.]),
    ] {
        let yaw = skate_heading(heading);
        let actual = [yaw.sin(), 0., yaw.cos()];
        assert!(
            actual
                .iter()
                .zip(forward)
                .all(|(a, b)| (a - b).abs() < 0.0001)
        );
        assert!((gta_heading(forward) - heading).abs() < 0.0001);
    }
}
