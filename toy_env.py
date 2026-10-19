from __future__ import annotations

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class ToyDrivingEnv(gym.Env):
    """Tiny continuous-control toy task to smoke-test RL plumbing.

    This is NOT a Rocket League simulator and teaches no Rocket League mechanics.
    Observation: [position_error, velocity, heading_error].
    Action: [throttle, steering] in [-1, 1].
    """

    metadata = {"render_modes": []}

    def __init__(self, max_steps: int = 500):
        super().__init__()
        self.observation_space = spaces.Box(
            low=np.array([-1.0, -1.0, -np.pi], dtype=np.float32),
            high=np.array([1.0, 1.0, np.pi], dtype=np.float32),
            dtype=np.float32,
        )
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self.max_steps = max_steps
        self.state = np.zeros(3, dtype=np.float32)
        self.steps = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array([
            self.np_random.uniform(-1, 1),
            self.np_random.uniform(-0.2, 0.2),
            self.np_random.uniform(-np.pi, np.pi),
        ], dtype=np.float32)
        self.steps = 0
        return self.state.copy(), {}

    def step(self, action):
        throttle, steering = np.clip(np.asarray(action, dtype=np.float32), -1, 1)
        error, velocity, heading = self.state
        velocity = float(np.clip(velocity + 0.035 * throttle, -1, 1))
        heading = float(((heading + 0.08 * steering + np.pi) % (2 * np.pi)) - np.pi)
        error = float(np.clip(error - 0.025 * velocity * np.cos(heading), -1, 1))
        self.state = np.array([error, velocity, heading], dtype=np.float32)
        self.steps += 1
        reward = -abs(error) - 0.1 * abs(heading) - 0.02 * abs(steering)
        terminated = abs(error) < 0.03 and abs(heading) < 0.08
        truncated = self.steps >= self.max_steps
        return self.state.copy(), float(reward), terminated, truncated, {}
