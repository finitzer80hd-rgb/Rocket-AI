from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path

# In a PyInstaller one-file build, the app code lives in a temporary extraction
# directory. Persistent outputs belong beside the executable (or project root).
if getattr(sys, "frozen", False):
    _exe_dir = Path(sys.executable).resolve().parent
    WORK_DIR = _exe_dir.parent if _exe_dir.name.lower() == "dist" else _exe_dir
else:
    WORK_DIR = Path(__file__).resolve().parent


def _run_worker():
    """Internal CLI mode used by the packaged EXE to run tasks without Python installed."""
    if len(sys.argv) < 2:
        raise SystemExit("Missing worker command")
    command = sys.argv[1]
    # Windowed PyInstaller builds may not provide stdout/stderr. Write worker
    # output to a persistent file that the GUI reads after the subprocess exits.
    log_path = WORK_DIR / "worker_output.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    _worker_log = log_path.open("a", encoding="utf-8", buffering=1)
    sys.stdout = _worker_log
    sys.stderr = _worker_log
    print("\\n=== Rocket AI worker:", command, "===")
    if command == "--worker-gpu":
        from rocket_ai.tools.check_torch import main
        main()
    elif command == "--worker-train":
        from rocket_ai.train_ppo import main
        sys.argv = ["rocket_ai.train_ppo"] + sys.argv[2:]
        main()
    elif command == "--worker-evaluate":
        from rocket_ai.evaluate import main
        sys.argv = ["rocket_ai.evaluate"] + sys.argv[2:]
        main()
    else:
        raise SystemExit(f"Unknown worker command: {command}")


class RocketAILauncher:
    def __init__(self, root):
        self.root = root
        root.title("Rocket AI Launcher")
        root.geometry("760x560")
        root.minsize(680, 480)

        tk.Label(root, text="Rocket AI", font=("Segoe UI", 22, "bold")).pack(pady=(16, 2))
        tk.Label(root, text="Training and diagnostics launcher • Starter build", font=("Segoe UI", 10)).pack(pady=(0, 12))
        self.status = tk.StringVar(value="Ready")
        tk.Label(root, textvariable=self.status, anchor="w").pack(fill="x", padx=16)

        buttons = tk.Frame(root)
        buttons.pack(fill="x", padx=16, pady=10)
        tk.Button(buttons, text="Check Python / NVIDIA GPU", command=self.check_gpu, height=2).pack(fill="x", pady=3)
        tk.Button(buttons, text="Train PPO demo (toy environment)", command=self.train, height=2).pack(fill="x", pady=3)
        tk.Button(buttons, text="Evaluate saved toy model", command=self.evaluate, height=2).pack(fill="x", pady=3)
        tk.Button(buttons, text="Open output folder", command=self.open_folder, height=2).pack(fill="x", pady=3)

        tk.Label(root, text="Output", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x", padx=16, pady=(8, 0))
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=14, state="disabled")
        self.output.pack(fill="both", expand=True, padx=16, pady=(4, 14))
        self.log("This starter uses a toy environment, NOT Rocket League physics.")
        self.log("Packaged training runs inside this EXE; model output is saved beside the EXE.")

    def log(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text.rstrip() + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def run_command(self, args, label):
        def worker():
            self.root.after(0, lambda: self.status.set(label + "…"))
            self.root.after(0, lambda: self.log("> " + " ".join(map(str, args))))
            try:
                if getattr(sys, "frozen", False):
                    command = args[0]
                    argv = [sys.executable, command] + args[1:]
                else:
                    argv = args
                completed = subprocess.run(
                    argv, cwd=str(WORK_DIR), stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, errors="replace",
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                output = completed.stdout or ""
                worker_log = WORK_DIR / "worker_output.log"
                if getattr(sys, "frozen", False) and worker_log.exists():
                    try:
                        output += "\\n" + worker_log.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        pass
                output = output.strip() or "(task finished; no output captured)"
                self.root.after(0, lambda out=output: self.log(out))
                self.root.after(0, lambda code=completed.returncode: self.status.set(f"{label} finished (exit code {code})"))
            except Exception as exc:
                self.root.after(0, lambda e=exc: self.log(f"Error: {e}"))
                self.root.after(0, lambda: self.status.set("Command failed"))
        threading.Thread(target=worker, daemon=True).start()

    def check_gpu(self):
        self.run_command(["--worker-gpu"], "GPU check")

    def train(self):
        self.run_command(["--worker-train", "--timesteps", "20000", "--out", str(WORK_DIR / "runs" / "ppo_toy")], "Toy PPO training")

    def evaluate(self):
        model = WORK_DIR / "runs" / "ppo_toy.zip"
        if not model.exists():
            messagebox.showinfo("No model yet", "Train the toy PPO model first.")
            return
        self.run_command(["--worker-evaluate", "--model", str(model), "--episodes", "5"], "Toy evaluation")

    def open_folder(self):
        try:
            os.startfile(str(WORK_DIR))
        except Exception as exc:
            messagebox.showerror("Could not open folder", str(exc))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1].startswith("--worker-"):
    _run_worker()
elif __name__ == "__main__":
    root = tk.Tk()
    RocketAILauncher(root)
    root.mainloop()
