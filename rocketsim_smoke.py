"""Verify that RocketSim Python bindings and collision meshes are available.

RocketSimPy is an optional, separately-built simulator dependency. This script
never installs or downloads native binaries automatically.
"""
from __future__ import annotations

import os
from pathlib import Path


def main() -> int:
    try:
        import RocketSim as rs
    except ImportError:
        print("RocketSim bindings are not installed.")
        print("See docs/ROCKETSIM_RLBOT_SETUP.md for the optional RocketSimPy setup.")
        return 2

    mesh_dir = Path(os.environ.get("ROCKETSIM_COLLISION_MESHES", "collision_meshes"))
    if not mesh_dir.is_dir():
        print(f"Collision mesh directory not found: {mesh_dir.resolve()}")
        print("Set ROCKETSIM_COLLISION_MESHES to your RocketSim collision_meshes folder.")
        return 3

    rs.init(str(mesh_dir))
    arena = rs.Arena(rs.GameMode.SOCCAR)
    car = arena.add_car(rs.Team.BLUE, rs.CAR_CONFIG_OCTANE)
    arena.step(120)
    state = car.get_state()
    print("RocketSim initialized successfully.")
    print(f"Simulated 1 second at {arena.tick_rate} ticks/s.")
    print(f"Car position: {state.pos.as_numpy()}")
    print(f"Ball state available: {arena.get_ball_state_array().shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
