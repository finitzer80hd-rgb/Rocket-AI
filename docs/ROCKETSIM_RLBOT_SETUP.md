# RocketSim + RLBot integration

This project includes an RLBot v5 bot entry point and a RocketSim Python-binding smoke test. They have different roles:

- **RLBot v5** connects the bot to an offline Rocket League match and passes game observations / receives controller actions.
- **RocketSim** is a separate, fast physics simulator intended for training and evaluation. Its Python bindings and collision meshes must be installed locally; RocketSim is not bundled into the Windows executable.

## 1. RLBot v5 (Windows)

Prerequisites:
- Rocket League installed through Steam (the checked-in `rlbot.toml` currently selects Steam).
- RLBot v5 installed/configured using the official instructions: https://wiki.rlbot.org/v5/
- Downloaded Windows package or the source project.

For the packaged build:
1. Open the latest successful **Build RocketAI for Windows** run under GitHub Actions and download the `RocketAI-Windows-exe` artifact.
2. Extract all files into one folder.
3. Install/configure RLBot v5 and Rocket League first.
4. Run `RUN_RLBOT.bat`. It starts `RocketAIRunner.exe`, which loads `rlbot.toml` and launches the match. The config starts a local human on Blue and Rocket AI on Orange.

For source development, install Python 3.12 and run:

```bat
py -3.12 -m venv venv
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -e ".[rlbot]"
RUN_RLBOT.bat
```

If you use Epic instead of Steam, change `launcher = "Steam"` in `rlbot.toml` to the launcher supported by your RLBot installation. This is an offline RLBot match, not online matchmaking automation.

The current bot chases the ball and uses boost conservatively. It is a connectivity baseline, not a trained policy. The next step is to load a saved policy inside `RocketAIBot.get_output` after observation/action dimensions and normalization are stable.

## 2. RocketSim Python bindings (training/simulation)

RocketSimPy is a native C++ extension with Python bindings and may require a local native build. Follow the binding project's current instructions rather than assuming a generic pip wheel exists:

- Project: https://github.com/pjsny/RocketSimPy
- Python binding build guide: https://github.com/pjsny/RocketSimPy/blob/main/python/README.md
- Upstream simulator: https://github.com/ZealanL/RocketSim

Collision meshes are required. Follow the RocketSimPy documentation and its linked collision-mesh dumper instructions, then set the environment variable to the directory containing those meshes.

```bat
set ROCKETSIM_COLLISION_MESHES=C:\path\to\collision_meshes
venv\Scripts\python.exe rocketsim_smoke.py
```

A successful run initializes Soccar, adds an Octane, advances 120 simulation ticks, and prints its state. This is a native simulator smoke test, not yet the full PPO training environment. We should validate the native binding and field layout on a Windows machine before connecting PPO to it.

## 3. Current status and next step

- RLBot v5 match config, Python bot, and match runner are checked in.
- Windows CI is configured to build the launcher, RLBot agent EXE, and match-runner EXE.
- RocketSim binding smoke test is checked in; it requires local native bindings and collision meshes.
- The PPO demo still uses the toy environment. No RocketSim-trained policy is claimed yet.
- Use these tools only in authorized offline matches and local simulations; this project does not bypass anti-cheat or automate protected online matchmaking.
