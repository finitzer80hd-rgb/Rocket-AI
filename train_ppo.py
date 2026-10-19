from __future__ import annotations

import argparse
from pathlib import Path

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from rocket_ai.envs.toy_env import ToyDrivingEnv


def main():
    parser = argparse.ArgumentParser(description="Smoke-test PPO pipeline on a toy task.")
    parser.add_argument("--timesteps", type=int, default=20_000)
    parser.add_argument("--out", default="runs/ppo_toy")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    args = parser.parse_args()

    env = ToyDrivingEnv()
    check_env(env, warn=True)
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=256,
        gamma=0.99,
        verbose=1,
        device=args.device,
        seed=42,
    )
    model.learn(total_timesteps=args.timesteps)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(output))
    print(f"Saved toy-task checkpoint: {output}.zip")
    print("Reminder: this toy environment is not Rocket League physics.")


if __name__ == "__main__":
    main()
