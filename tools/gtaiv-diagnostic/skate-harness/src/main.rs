use skate_host::bridge::{Controls, Session};
use std::path::PathBuf;

fn run() -> Result<(), String> {
    let assets = std::env::args_os().nth(1).map(PathBuf::from)
        .ok_or("Supply the private converted Skate asset directory")?;
    if !assets.is_dir() { return Err("Asset directory is missing".into()); }
    // Synthetic Y-up floor only. This says nothing about GTA collision or scale.
    let triangles = vec![
        [[-100., 0., -100.], [-100., 0., 100.], [100., 0., -100.]],
        [[100., 0., -100.], [-100., 0., 100.], [100., 0., 100.]],
    ];
    let mut session = Session::new(&assets, triangles, vec![], [0., 1., 0.], 0.)?;
    let initial_tick = session.pose().tick;
    let period = session.period();
    if !period.is_finite() || period <= 0. { return Err("Invalid simulation period".into()); }
    for _ in 0..120 {
        session.tick(Controls::default())?;
        let pose = session.pose();
        if !pose.root.to_cols_array().iter().all(|v| v.is_finite()) {
            return Err("Non-finite simulation pose".into());
        }
    }
    let tick = session.pose().tick;
    if tick <= initial_tick { return Err("Simulation did not advance".into()); }
    println!("PASS: x86 standalone Skate session advanced {initial_tick}->{tick}; period={period}");
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        // Upstream initialization can include private asset paths. Keep output local.
        eprintln!("FAIL: {error}");
        std::process::exit(1);
    }
}
