# RocketSim + RLBot integration

This project now has an RLBot v5 bot entry point and a RocketSim Python-binding smoke test. These serve different roles:

- **RLBot v5** connects the bot to an offline Rocket League match and passes game observations / receives controller actions.
- **RocketSim** is a separate, fast physics simulator intended for training and evaluation. Its Python bindings and collision meshes must be installed locally; RocketSim is not bundled into the Windows launcher yet.

## 1. RLBot v5 (Windows)

Prerequisites:
- Rocket League installed through Steam (the checked-in `rlbot.toml` currently selects Steam).
- Python 3.12 recommended for the current official RLBot Python example.
- RLBot v5 installed/configured using the official instructions: https://wiki.rlbot.org/v5/
- The project virtual environment.

From a terminal in the project directory:

```bat
py -3.12 -m venv venv
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -e ".[rlbot]"
RUN_RLBOT.bat
```

The match config runs a local human on Blue and Rocket AI on Orange. It uses offline RLBot match orchestration; it does not automate online matchmaking. If you use Epic instead of Steam, change `launcher = "Steam"` in `rlbot.toml` to the launcher supported by your RLBot installation.

The current bot chases the ball and uses boost conservatively. It is a connectivity baseline, not a trained policy. The next step is to load a saved policy inside `RocketAIBot.get_output` after observation/action dimensions and normalization are stable.

## 2. RocketSim Python bindings (training/simulation)

RocketSimPy is a native C++ extension with Python bindings, and may require a local native build. Follow the binding project's current instructions rather than assuming a generic pip wheel exists:

- Project: https://github.com/pjsny/RocketSimPy
- Python binding build guide: https://github.com/pjsny/RocketSimPy/blob/main/python/README.md
- Upstream simulator: https://github.com/ZealanL/RocketSim
- Collision meshes are required. Follow the RocketSimPy documentation / its linked collision-mesh dumper instructions, then set the environment variable to the directory containing those meshes.

Example:

```bat
set ROCKETSIM_COLLISION_MESHES=C:\path\to\collision_meshes
venv\Scripts\python.exe rocketsim_smoke.py
```

A successful run initializes Soccar, adds an Octane, advances 120 simulation ticks, and prints its state. This is a native simulator smoke test, not yet the full PPO training environment. We should validate the native binding and field layout on your Windows machine before connecting PPO to it.

## 3. Current status and next step

- RLBot v5 match config, Python bot, and run script are checked in.
- RocketSim binding smoke test is checked in; it requires local native bindings and collision meshes.
- The PPO demo still uses the toy environment. No RocketSim-trained policy is claimed yet.
- Use these tools only in authorized offline matches and local simulations; this project does not bypass anti-cheat or automate protected online matchmaking.
