#!/usr/bin/env python3
import subprocess, sys, pathlib

repo_dir = pathlib.Path(__file__).parent

def run(cmd, ignore_error=False):
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)}")
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        if not ignore_error:
            sys.exit(result.returncode)

# 1️⃣ Ensure we are on the main branch (rename if needed)
run(["git", "branch", "-M", "main"], ignore_error=True)

# 2️⃣ Remove existing remote if it exists (ignore error if it doesn't)
run(["git", "remote", "remove", "origin"], ignore_error=True)

# 3️⃣ Add the correct remote
run(["git", "remote", "add", "origin", "https://github.com/sofivillasmil26-gif/Serindipiafinal.git"])

# 4️⃣ Stage required files
files_to_add = ["app.py", "style.css", "requirements.txt", "config.json"]
run(["git", "add"] + files_to_add)
# Add the library folder if present
library_path = repo_dir / "library"
if library_path.exists():
    run(["git", "add", "library/"])

# 5️⃣ Commit changes (allow empty commit if nothing changed)
run(["git", "commit", "-m", "Deploy final spaceship build to Serindipiafinal repo"], ignore_error=True)

# 6️⃣ Force‑push to main
run(["git", "push", "-u", "origin", "main", "--force"])
