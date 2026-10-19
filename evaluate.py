from __future__ import annotations

import argparse
import numpy as np
from stable_baselines3 import PPO

from toy_env import ToyDrivingEnv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="runs/ppo_toy.zip")
    parser.add_argument("--episodes", type=int, default=5)
    args = parser.parse_args()

    env = ToyDrivingEnv()
    model = PPO.load(args.model)
    returns = []
    for episode in range(args.episodes):
        obs, _ = env.reset(seed=1000 + episode)
        done = False
        total = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total += reward
            done = terminated or truncated
        returns.append(total)
    print(f"episodes={len(returns)} mean_return={np.mean(returns):.3f} std={np.std(returns):.3f}")


if __name__ == "__main__":
    main()
