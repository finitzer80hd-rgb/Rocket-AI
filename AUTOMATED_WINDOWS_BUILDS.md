# Automated Windows EXE builds

This repository includes `.github/workflows/build-windows.yml`. Once the project is in a GitHub repository, GitHub Actions builds `RocketAI.exe` on every push to `main`/`master`, and also supports manual runs.

## One-time setup (no command line required)
1. Sign in to GitHub and create a new repository.
2. Upload the contents of this folder to the repository using GitHub's web UI (Add file → Upload files). Make sure `.github/workflows/build-windows.yml` is included.
3. Commit the upload to `main`.
4. Open the repository's **Actions** tab. Open the latest **Build RocketAI for Windows** run.
5. When the run completes, download **RocketAI-Windows-exe** from the **Artifacts** section. Extract it and double-click `RocketAI.exe`.
6. Every future commit/push automatically creates a new downloadable EXE artifact. You can also run the workflow manually from Actions → Build RocketAI for Windows → Run workflow.

## Important
- GitHub Actions requires a GitHub account and the repository's Actions feature enabled.
- Artifacts are retained for 30 days by this workflow.
- The build includes PyTorch, which makes the executable large and the build slower.
- The starter's PPO environment is a toy smoke-test environment, not Rocket League physics. RLBot/RocketSim integration is not implemented yet.
- This workflow builds a Windows executable; it does not implement anti-cheat evasion or unauthorized matchmaking automation.
