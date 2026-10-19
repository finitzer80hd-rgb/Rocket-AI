# Rocket AI

Windows-friendly starter for reinforcement-learning experiments, RLBot v5 offline matches, and optional RocketSim simulation.

## Download the Windows build

1. Open the **Actions** tab and select the latest successful **Build RocketAI for Windows** run.
2. Download the **RocketAI-Windows-exe** artifact and extract it to a folder.
3. Run `RocketAI.exe` for the desktop launcher.
4. To start an offline RLBot match, follow `ROCKETSIM_RLBOT_SETUP.md` (included in the artifact) and run `RUN_RLBOT.bat`. The RLBot installer and Rocket League must already be set up.

Workflow: https://github.com/finitzer80hd-rgb/Rocket-AI/actions

## Current capabilities and limitations

- `RocketAIBot.exe` is an RLBot v5 bot entry point with a simple ball-chasing baseline for offline matches.
- `rocketsim_smoke.py` checks a separately installed RocketSim Python binding and collision meshes.
- The existing PPO trainer still uses a toy environment. RocketSim-backed PPO training, replay ingestion, and policy transfer are not yet implemented.
- Native RocketSim bindings and collision meshes are not bundled in the EXE because they require a separate native setup.
- This project is intended for local simulation and authorized offline RLBot matches, not anti-cheat evasion or unauthorized online matchmaking automation.
