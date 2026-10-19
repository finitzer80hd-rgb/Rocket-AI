from __future__ import annotations

import numpy as np

from toy_env import ToyDrivingEnv


def test_toy_env_reset_and_step_contract():
    env = ToyDrivingEnv()
    obs, info = env.reset(seed=123)
    assert env.observation_space.contains(obs)
    assert isinstance(info, dict)

    obs, reward, terminated, truncated, info = env.step(
        np.zeros(env.action_space.shape, dtype=np.float32)
    )
    assert env.observation_space.contains(obs)
    assert np.isfinite(reward)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)
