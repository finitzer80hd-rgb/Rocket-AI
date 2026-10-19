# Automated Windows EXE builds

The workflow at `.github/workflows/build-windows.yml` builds `RocketAI.exe` on every push to `main` or `master`, and supports manual runs.

## Download the executable
1. Open the repository's **Actions** tab.
2. Select **Build RocketAI for Windows** and open the latest run.
3. When the run succeeds, download the **RocketAI-Windows-exe** artifact and extract it.
4. Run `RocketAI.exe`.

Each successful workflow run creates a new artifact, retained for 30 days. The executable bundles Python and the project's dependencies; a separate Python installation should not be required to launch it.

## Important limitations
- GitHub Actions must be enabled for the repository.
- The executable bundles PyTorch, so it can be large and take several minutes to build.
- The current PPO environment is a toy smoke test, not Rocket League physics.
- RLBot/RocketSim integration and replay ingestion are not implemented yet.
- The project is intended for authorized local/simulation use, not anti-cheat evasion or unauthorized online matchmaking automation.
