#[path = "../src/connection.rs"]
mod connection;
use connection::*;
/// Mount `triangles` for a grounded rider standing at `origin`.
fn mount(triangles: Vec<Triangle>, origin: [f32; 3], layer: u32) -> Result<Surface, &'static str> {
    Surface::install(None, triangles, Basis { origin, scale: 1., layer },
        &Rider { pose: origin, grounded: true, query: [origin[0], origin[1]], ground: origin[2], layer, valid: 1 },
        |_| Ok::<_, ()>(()))
}
/// A grounded host observation at `xy`.
fn seen(xy: [f32; 2], ground: f32, layer: u32, valid: u32) -> Rider {
    Rider { pose: [xy[0], xy[1], ground], grounded: true, query: xy, ground, layer, valid }
}
#[test]
fn floor_matches_gta_axes() {
    let floor = vec![
        [[96., 196., 10.], [112., 196., 10.], [112., 212., 10.]],
        [[96., 196., 10.], [112., 212., 10.], [96., 212., 10.]],
    ];
    let surface = mount(floor, [104., 204., 10.], 1).unwrap();
    assert_eq!(surface.to_skate([106., 207., 12.]), [2., 2., -3.]);
    assert_eq!(surface.to_gta([2., 2., -3.]), [106., 207., 12.]);
    assert_eq!(surface.triangles().len(), 2);
    assert!(surface.contains_pose([107., 207., 10.]));
    assert!(!surface.contains_pose([113., 207., 10.]));
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
#[test]
fn qualified_slope_keeps_riding_when_query_and_pose_move_to_different_heights() {
    let surface = mount(SLOPE.to_vec(), [1., 1., 0.25], 7).unwrap();
    assert!(surface.observation(&seen([1., 1.], 0.25, 7, 1)));
    assert!(surface.observation(&seen([6., 2.], 1.5, 7, 1)));
    assert!(surface.contains_pose([6., 2., 2.5]));
    assert!(!surface.observation(&seen([6., 2.], 0.25, 7, 1)));
    assert!(!surface.observation(&seen([6., 2.], 1.5, 8, 1)));
    assert!(!surface.observation(&seen([6., 2.], 1.5, 7, 0)));
    assert!(!surface.contains_pose([9., 2., 2.5]));
    assert_eq!(surface.triangles().len(), 2);
}
#[test]
fn geometry_refuses_ambiguous_invalid_or_uncovered_ground() {
    let t = SLOPE[0];
    for (triangles, layer) in [
        (vec![t], 0),
        (vec![], 7),
        (vec![[[0.; 3]; 3]], 7),
        (vec![[[f32::NAN, 0., 0.], t[1], t[2]]], 7),
        (vec![t; 4097], 7),
        (vec![t, t.map(|p| [p[0], p[1], p[2] + 1.])], 7),
    ] {
        assert!(mount(triangles, [1., 1., 0.25], layer).is_err());
    }
    let surface = mount(vec![t], [1., 1., 0.25], 7).unwrap();
    assert!(!surface.observation(&seen([9., 0.], 2.25, 7, 1)));
    assert!(!surface.observation(&seen([1., 1.], 0.25, 7, 2)));
    assert!(!surface.observation(&seen([f32::NAN, 1.], 0.25, 7, 1)));
    assert!(!surface.contains_pose([1., 1., 4.]));
    assert!(!surface.contains_pose([1., 1., f32::NAN]));
}
#[test]
fn vertical_faces_stay_in_collision_without_becoming_support() {
    let surface = mount(
        vec![
            [[-4., -4., -1.], [4., -4., 1.], [-4., 4., -1.]],
            [[4., -4., 1.], [4., 4., 1.], [-4., 4., -1.]],
            [[4., -4., 1.], [4., 4., 1.], [4., 4., 3.]],
        ],
        [0.; 3],
        7,
    )
    .unwrap();
    assert!(surface.observation(&seen([2., 0.], 0.5, 7, 1)));
    assert!(surface.contains_pose([2., 0., 1.5]));
    assert_eq!(surface.triangles().len(), 3);
}
#[test]
fn stacked_floors_require_an_explicit_selected_layer() {
    let floor = |z: f32| vec![
        [[0., 0., z], [8., 0., z], [8., 8., z]],
        [[0., 0., z], [8., 8., z], [0., 8., z]],
    ];
    let lower = mount(floor(0.), [2., 2., 0.], 7).unwrap();
    let upper = mount(floor(5.), [2., 2., 5.], 8).unwrap();
    assert!(lower.observation(&seen([4., 4.], 0., 7, 1)));
    assert!(!lower.observation(&seen([4., 4.], 5., 8, 1)));
    assert!(upper.observation(&seen([4., 4.], 5., 8, 1)));
    assert!(!upper.observation(&seen([4., 4.], 0., 7, 1)));
    assert!(mount([floor(0.), floor(5.)].concat(), [2., 2., 0.], 7).is_err());
}
#[test]
fn floor_agreement_allows_sampling_error_up_to_the_wall_threshold() {
    let floor = vec![
        [[0., 0., 0.], [4., 0., 0.], [4., 4., 0.]],
        [[0., 0., 0.], [4., 4., 0.], [0., 4., 0.]],
    ];
    let surface = mount(floor, [2., 2., 0.], 7).unwrap();
    assert!(surface.observation(&seen([2., 2.], 0.29, 7, 1)));
    assert!(surface.observation(&seen([2., 2.], -0.29, 7, 1)));
    assert!(!surface.observation(&seen([2., 2.], 0.31, 7, 1)));
    assert!(!surface.observation(&seen([2., 2.], -0.31, 7, 1)));
}
#[test]
fn only_air_states_lose_ground_contact() {
    for state in ["PhysicsAir", "KnownAir", "PhysicsAirSecondary", "BipedAir"] {
        assert!(!grounded(state), "{state}");
    }
    for state in ["PhysicsGround", "SlideGround", "WipeoutGround", "BipedGround", "OffBoardPushing"] {
        assert!(grounded(state), "{state}");
    }
}
const SLOPE: [[[f32; 3]; 3]; 2] = [
    [[0., 0., 0.], [8., 0., 2.], [0., 8., 0.]],
    [[8., 0., 2.], [8., 8., 2.], [0., 8., 0.]],
];
fn basis() -> Basis {
    Basis { origin: [1., 1., 0.25], scale: 1., layer: 7 }
}
fn rider(pose: [f32; 3], ground: f32, grounded: bool) -> Rider {
    Rider { pose, grounded, query: [pose[0], pose[1]], ground, layer: 7, valid: 1 }
}
#[test]
fn mount_installs_skate_triangles_as_the_first_revision() {
    let mut installed = vec![];
    let floor = Surface::install(None, SLOPE.to_vec(), basis(), &rider([1., 1., 0.25], 0.25, true),
        |f| { installed = f.triangles(); Ok::<_, ()>(()) }).unwrap();
    assert_eq!(floor.revision(), 1);
    // GTA (6, 2, 1.5) on the slope is Skate (5, 1.25, -1) from origin (1, 1, 0.25).
    assert_eq!(installed[0][1], [7., 1.75, 1.]);
    assert_eq!(installed.len(), 2);
}
/// The slope z = x / 4 as a square window of two triangles centred on (cx, cy).
fn window(cx: f32, cy: f32) -> Vec<[[f32; 3]; 3]> {
    let p = |x: f32, y: f32| [x, y, x / 4.];
    let (a, b, c, d) = (p(cx - 4., cy - 4.), p(cx + 4., cy - 4.), p(cx + 4., cy + 4.), p(cx - 4., cy + 4.));
    vec![[a, b, c], [a, c, d]]
}
fn mount_slope() -> Surface {
    Surface::install(None, window(2., 2.), Basis { origin: [2., 2., 0.5], scale: 1., layer: 7 },
        &rider([2., 2., 0.5], 0.5, true), |_| Ok::<_, ()>(())).unwrap()
}
#[test]
fn crossing_a_cell_installs_the_next_window_as_a_new_revision_under_the_rider() {
    let first = mount_slope();
    let basis = first.basis();
    // The rider rolled 3 m east; the window recentred two metres on.
    let at = rider([5., 2., 1.25], 1.25, true);
    let mut calls = 0;
    let second = Surface::install(Some(&first), window(4., 2.), basis, &at,
        |_| { calls += 1; Ok::<_, ()>(()) }).unwrap();
    assert_eq!((second.revision(), calls), (2, 1));
    assert!(second.agrees(&at));
    let third = Surface::install(Some(&second), window(6., 2.), basis, &rider([7., 2., 1.75], 1.75, true),
        |_| Ok::<_, ()>(())).unwrap();
    assert_eq!(third.revision(), 3);
    // A window that has left the rider behind never reaches the Session.
    let behind = Surface::install(Some(&second), window(14., 2.), basis, &at,
        |_| { calls += 1; Ok::<_, ()>(()) });
    assert!(behind.is_err());
    assert_eq!(calls, 1);
    // The Skate frame stays at the mount origin across the swap: no remount.
    assert_eq!(third.to_skate([7., 2., 1.75]), [5., 1.25, 0.]);
    assert!(Surface::install(Some(&second), window(6., 2.), Basis { origin: [6., 2., 1.5], ..basis },
        &at, |_| Ok::<_, ()>(())).is_err());
}
#[test]
fn a_session_that_refuses_the_floor_is_a_refusal_with_its_reason() {
    let first = mount_slope();
    let refused = Surface::install(Some(&first), window(4., 2.), first.basis(),
        &rider([5., 2., 1.25], 1.25, true), |_| Err("collision"));
    assert_eq!(refused.err(), Some("Session refused the floor"));
}
#[test]
fn floor_agreement_applies_only_while_skate_reports_ground_contact() {
    let first = mount_slope();
    // Host ground under the rider is a 0.5 m planter the window does not describe.
    let over_planter = |grounded| rider([5., 2., 2.5], 1.75, grounded);
    assert!(!first.agrees(&over_planter(true)), "grounded on another floor is refused");
    assert!(first.agrees(&over_planter(false)), "an airborne frame is not refused");
    let refreshed = Surface::install(Some(&first), window(4., 2.), first.basis(),
        &over_planter(false), |_| Ok::<_, ()>(()));
    assert_eq!(refreshed.map(|f| f.revision()), Ok(2), "the window follows an airborne rider");
    // Airborne is not a licence to leave coverage, the floor or the pose height limit.
    assert!(!first.agrees(&Rider { query: [9., 2.], pose: [9., 2., 2.5], ..over_planter(false) }));
    assert!(!first.agrees(&Rider { layer: 8, ..over_planter(false) }));
    assert!(!first.agrees(&Rider { pose: [5., 2., 4.5], ..over_planter(false) }));
    assert!(!first.agrees(&Rider { ground: f32::NAN, ..over_planter(false) }));
}
#[test]
fn a_ride_far_beyond_1000_m_keeps_the_mount_frame_to_the_millimetre() {
    let mut floor = mount_slope();
    let basis = floor.basis();
    // Follow the rider 1500 m east in 2 m cells, as the coverage window does.
    for cell in 1..=750 {
        let x = 2. + cell as f32 * 2.;
        let at = rider([x + 0.5, 2., (x + 0.5) / 4.], (x + 0.5) / 4., true);
        floor = Surface::install(Some(&floor), window(x, 2.), basis, &at, |_| Ok::<_, ()>(())).unwrap();
        let back = floor.to_gta(floor.to_skate(at.pose));
        assert!(back.iter().zip(at.pose).all(|(a, b)| (a - b).abs() < 0.001), "{back:?} at {x}");
    }
    assert_eq!(floor.revision(), 751);
    // One upload still reaches no farther than 1000 m from the rider.
    let at = rider([1502.5, 2., 1502.5 / 4.], 1502.5 / 4., true);
    let mut reaching = window(1502., 2.);
    reaching.push([[400., 0., 100.], [404., 0., 101.], [400., 4., 100.]]);
    assert!(Surface::install(Some(&floor), reaching, basis, &at, |_| Ok::<_, ()>(())).is_err());
}
#[test]
fn the_skate_frame_extent_is_bounded_where_f32_still_resolves_a_millimetre() {
    let far = |x: f32| mount(window(x, 2.), [x, 2., x / 4.], 7);
    assert!(far(8000.).is_ok());
    let origin = mount_slope();
    let at = rider([8300., 2., 2075.], 2075., true);
    assert!(Surface::install(Some(&origin), window(8300., 2.), origin.basis(), &at, |_| Ok::<_, ()>(())).is_err());
}
