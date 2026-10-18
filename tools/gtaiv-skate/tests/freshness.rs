#[path = "../src/accepted_pose.rs"]
mod accepted_pose;
#[path = "../src/connection.rs"]
mod connection;
use accepted_pose::AcceptedPose;
use connection::{Basis, Rider, Surface};
use std::time::{Duration, Instant};
fn slope() -> Surface {
    Surface::install(
        None,
        vec![
            [[0., 0., 0.], [8., 0., 2.], [0., 8., 0.]],
            [[8., 0., 2.], [8., 8., 2.], [0., 8., 0.]],
        ],
        Basis { origin: [1., 1., 0.25], scale: 1., layer: 7 },
        &Rider { pose: [1., 1., 0.25], grounded: true, query: [1., 1.], ground: 0.25, layer: 7, valid: 1 },
        |_| Ok::<_, ()>(()),
    )
    .unwrap()
}
#[test]
fn last_validated_bridge_pose_survives_publication_until_original_deadline() {
    let surface = slope();
    let start = Instant::now();
    let pose = AcceptedPose::new(7, 9, 3, [6., 2., 2.5, 90.], true, start).unwrap();
    let at = |now, ground| pose.fresh(7, 9, 3, now, &surface, [1., 1.], ground, 7, 1);
    assert_eq!(at(start + Duration::from_millis(250), 0.25), Some([6., 2., 2.5, 90.]));
    // Re-reading the same pose never renews its timestamp.
    assert!(at(start + Duration::from_millis(251), 0.25).is_none());
    assert!(pose.fresh(8, 9, 3, start, &surface, [1., 1.], 0.25, 7, 1).is_none());
    assert!(pose.fresh(7, 10, 3, start, &surface, [1., 1.], 0.25, 7, 1).is_none());
    assert!(pose.fresh(7, 9, 4, start, &surface, [1., 1.], 0.25, 7, 1).is_none());
    assert!(at(start, f32::NAN).is_none());
    assert!(AcceptedPose::new(7, 9, 3, [f32::NAN, 200., 11., 90.], true, start).is_none());
}
#[test]
fn qualified_observation_follows_its_query_while_fresh_pose_uses_own_mesh_height() {
    let surface = slope();
    let start = Instant::now();
    let pose = AcceptedPose::new(7, 9, 3, [6., 2., 2.5, 90.], true, start).unwrap();
    assert_eq!(
        pose.fresh(7, 9, 3, start, &surface, [1., 1.], 0.25, 7, 1),
        Some([6., 2., 2.5, 90.])
    );
    assert!(pose.fresh(7, 9, 3, start, &surface, [6., 2.], 0.25, 7, 1).is_none());
    assert!(pose.fresh(7, 9, 3, start, &surface, [1., 1.], 0.25, 7, 0).is_none());
    assert!(pose.fresh(7, 9, 3, start, &surface, [1., 1.], 0.25, 8, 1).is_none());
}
#[test]
fn an_airborne_accepted_pose_is_not_refused_by_floor_agreement() {
    let surface = slope();
    let start = Instant::now();
    // Host ground 0.5 m above the floor at the query: a planter under a jump.
    let airborne = AcceptedPose::new(7, 9, 3, [6., 2., 3., 90.], false, start).unwrap();
    let grounded = AcceptedPose::new(7, 9, 3, [6., 2., 3., 90.], true, start).unwrap();
    assert!(airborne.fresh(7, 9, 3, start, &surface, [6., 2.], 2., 7, 1).is_some());
    assert!(grounded.fresh(7, 9, 3, start, &surface, [6., 2.], 2., 7, 1).is_none());
    assert!(airborne.fresh(7, 9, 3, start, &surface, [9., 2.], 2., 7, 1).is_none(), "still within coverage");
}
