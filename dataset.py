from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import numpy as np


def read_jsonl(path: str | Path) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Read versioned demonstration rows containing observation and action arrays."""
    with Path(path).open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if "observation" not in row or "action" not in row:
                raise ValueError(f"Line {line_number}: expected observation and action")
            obs = np.asarray(row["observation"], dtype=np.float32)
            action = np.asarray(row["action"], dtype=np.float32)
            if not np.isfinite(obs).all() or not np.isfinite(action).all():
                raise ValueError(f"Line {line_number}: non-finite values")
            yield obs, action
