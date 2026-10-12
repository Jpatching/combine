#[path = "../src/accepted_pose.rs"]
mod accepted_pose;
#[path = "../src/connection.rs"]
mod connection;
use accepted_pose::AcceptedPose;
use connection::Surface;
use std::time::{Duration, Instant};
#[test]
fn last_validated_bridge_pose_survives_publication_until_original_deadline() {
    let points = (0..25)
        .map(|i| [96. + (i % 5) as f32 * 2., 196. + (i / 5) as f32 * 2., 10.])
        .collect();
    let surface = Surface::new(points, [100., 200., 10.], 1.).unwrap();
    let start = Instant::now();
    let pose = AcceptedPose::new(7, 9, 3, [100., 200., 11., 90.], start).unwrap();
    assert_eq!(
        pose.fresh(7, 9, 3, start + Duration::from_millis(250), 10., &surface),
        Some([100., 200., 11., 90.])
    );
    // Re-reading the same pose never renews its timestamp.
    assert!(
        pose.fresh(7, 9, 3, start + Duration::from_millis(251), 10., &surface)
            .is_none()
    );
    assert!(pose.fresh(8, 9, 3, start, 10., &surface).is_none());
    assert!(pose.fresh(7, 10, 3, start, 10., &surface).is_none());
    assert!(pose.fresh(7, 9, 4, start, 10., &surface).is_none());
    assert!(pose.fresh(7, 9, 3, start, 10.1, &surface).is_none());
    assert!(pose.fresh(7, 9, 3, start, f32::NAN, &surface).is_none());
    assert!(AcceptedPose::new(7, 9, 3, [f32::NAN, 200., 11., 90.], start).is_none());
}
#[test]
fn qualified_observation_follows_its_query_while_fresh_pose_uses_own_mesh_height() {
    let surface = Surface::from_triangles(
        vec![
            [[0., 0., 0.], [8., 0., 2.], [0., 8., 0.]],
            [[8., 0., 2.], [8., 8., 2.], [0., 8., 0.]],
        ],
        [1., 1., 0.25],
        1.,
        7,
    )
    .unwrap();
    let start = Instant::now();
    let pose = AcceptedPose::new(7, 9, 3, [6., 2., 2.5, 90.], start).unwrap();
    assert_eq!(
        pose.fresh_observation(7, 9, 3, start, 0.25, &surface, Some(([1., 1.], 7, 1))),
        Some([6., 2., 2.5, 90.])
    );
    assert!(pose.fresh(7, 9, 3, start, 0.25, &surface).is_none());
    assert!(
        pose.fresh_observation(7, 9, 3, start, 0.25, &surface, Some(([6., 2.], 7, 1)))
            .is_none()
    );
    assert!(
        pose.fresh_observation(7, 9, 3, start, 0.25, &surface, Some(([1., 1.], 7, 0)))
            .is_none()
    );
    assert!(
        pose.fresh_observation(
            7,
            9,
            3,
            start + Duration::from_millis(251),
            0.25,
            &surface,
            Some(([1., 1.], 7, 1))
        )
        .is_none()
    );
    assert!(
        pose.fresh_observation(8, 9, 3, start, 0.25, &surface, Some(([1., 1.], 7, 1)))
            .is_none()
    );
}
