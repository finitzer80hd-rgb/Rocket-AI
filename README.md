# Rocket AI (starter)

A Windows-friendly starter for experimenting with reinforcement learning and packaging a desktop launcher.

## Build and run

- Open the **Actions** tab and select **Build RocketAI for Windows**.
- Open the latest successful run and download the `RocketAI-Windows-exe` artifact.
- Extract the artifact and run `RocketAI.exe`.

The workflow is located at `.github/workflows/build-windows.yml` and runs on pushes to `main` or `master`, or manually from Actions.

## Current limitations

The PPO environment is a small toy driving task used to verify the training pipeline. It is **not Rocket League physics** and the project does not yet control the actual game. RocketSim/RLBot adapters and replay ingestion are not implemented.

The intended next step is to integrate a pinned, documented RocketSim and/or RLBot interface, validate observations and actions with contract tests, and train/evaluate in an authorized simulation environment. Do not use this project to evade anti-cheat or automate protected online matchmaking.
