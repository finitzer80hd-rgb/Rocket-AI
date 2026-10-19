"""Start an offline Rocket League match through RLBot v5."""
from __future__ import annotations

import sys
import time
from pathlib import Path

from rlbot import flat
from rlbot.managers import MatchManager


def main() -> None:
    # In a PyInstaller build, configs live beside the EXE, not in the temp extraction dir.
    root = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    config = root / "rlbot.toml"
    if not config.is_file():
        raise FileNotFoundError(f"Could not find match config: {config}")
    manager = MatchManager()
    try:
        manager.start_match(config)
        print("RLBot match started. Press Ctrl+C here to stop.")
        while (
            manager.packet is None
            or manager.packet.match_info.match_phase != flat.MatchPhase.Ended
        ):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping RLBot match...")
    finally:
        manager.shut_down()


if __name__ == "__main__":
    main()
