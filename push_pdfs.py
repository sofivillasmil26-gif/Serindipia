#!/usr/bin/env python3
import subprocess, sys, pathlib, os

repo_dir = pathlib.Path(__file__).parent

def run(cmd, ignore_error=False):
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)}")
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        if not ignore_error:
            sys.exit(result.returncode)

# 1️⃣ Ensure we are on main branch (rename if needed)
run(["git", "branch", "-M", "main"], ignore_error=True)

# 2️⃣ Reset remote (remove then add)
run(["git", "remote", "remove", "origin"], ignore_error=True)
run(["git", "remote", "add", "origin", "https://github.com/sofivillasmil26-gif/Serindipiafinal.git"])

# 3️⃣ Stage required files – core + data folder + PDFs in root
files = ["app.py", "style.css", "requirements.txt", "config.json", "data"]
# add PDFs (any .pdf in repo root)
pdfs = [p.name for p in repo_dir.iterdir() if p.suffix.lower() == ".pdf"]
run(["git", "add"] + files + pdfs)

# 4️⃣ Commit (allow empty commit if nothing changed)
run(["git", "commit", "-m", "Add PDFs, data folder, and core files"], ignore_error=True)

# 5️⃣ Force‑push to main
run(["git", "push", "-u", "origin", "main", "--force"])

# 6️⃣ Clean up – delete this script itself
try:
    os.remove(__file__)
    print("Temporary script deleted.")
except Exception as e:
    print(f"Failed to delete script: {e}", file=sys.stderr)
