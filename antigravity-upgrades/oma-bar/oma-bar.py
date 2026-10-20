#!/usr/bin/env python3
"""
OMA Status Bar Generator for Antigravity (AGY)
Updates Tmux status-right, Terminal Window Title, and state files with real-time OMA telemetry.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Ensure standard bin paths are in PATH
os.environ["PATH"] = f"/opt/homebrew/bin:/usr/local/bin:{os.environ.get('PATH', '')}"

def get_git_info():
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL, text=True
        ).strip()
        if not branch:
            # Detached head or commit sha
            branch = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL, text=True
            ).strip()
        
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            stderr=subprocess.DEVNULL, text=True
        ).strip()
        dirty = "*" if len(status) > 0 else ""
        return f"{branch}{dirty}" if branch else "no-git"
    except Exception:
        return "no-git"

def read_json_state(path, default=None):
    try:
        p = Path(path)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default or {}

def get_oma_state(cwd):
    omg_dir = Path(cwd) / ".omg" / "state"
    global_gemini = Path.home() / ".gemini"
    
    # 1. Mode & Stage
    mode_data = read_json_state(omg_dir / "mode.json")
    mode = mode_data.get("mode", mode_data.get("active", "balanced"))
    
    stage_data = read_json_state(omg_dir / "stage.json")
    stage = stage_data.get("stage", stage_data.get("current", "idle"))
    
    # 2. Ralph / Quality Gate
    ralph_data = read_json_state(omg_dir / "ralph.json")
    ralph = ralph_data.get("status", ralph_data.get("gate", "PASS"))
    
    # 3. Task Progress
    taskboard_md = omg_dir / "taskboard.md"
    done_count = 0
    total_count = 0
    if taskboard_md.exists():
        try:
            with open(taskboard_md, "r", encoding="utf-8") as f:
                for line in f:
                    if "- [x]" in line or "- [X]" in line:
                        done_count += 1
                        total_count += 1
                    elif "- [ ]" in line:
                        total_count += 1
        except Exception:
            pass
    tasks_str = f"{done_count}/{total_count}" if total_count > 0 else "0/0"
    
    # 4. Active Model
    model_data = read_json_state(omg_dir / "model.json")
    model = model_data.get("model", model_data.get("active", "gemini-3.8-flash"))
    # shorten model name if needed
    model_short = model.replace("gemini-", "g-")
    
    # 5. Context & Cost
    token_data = read_json_state(omg_dir / "tokens.json")
    tokens = token_data.get("tokens", token_data.get("context_tokens", None))
    cost = token_data.get("cost", 0.0)
    if tokens:
        if tokens >= 1000000:
            ctx_str = f"{tokens / 1000000:.1f}M"
        elif tokens >= 1000:
            ctx_str = f"{tokens // 1000}k"
        else:
            ctx_str = f"{tokens}"
    else:
        ctx_str = "ctx:ok"
    
    return {
        "mode": mode,
        "stage": stage,
        "ralph": ralph,
        "tasks": tasks_str,
        "model": model_short,
        "ctx": ctx_str,
        "cost": f"${cost:.2f}"
    }

def build_plain_bar(state, git_info):
    return (
        f"[OMA:{state['mode']}:{state['stage']} | "
        f"ralph:{state['ralph']} | "
        f"tasks:{state['tasks']} | "
        f"{state['model']} | "
        f"git:{git_info} | "
        f"{state['ctx']}]"
    )

def build_tmux_bar(state, git_info):
    # ANSI / Tmux formatting with color segments
    ralph_color = "colour82" if state['ralph'] in ("PASS", "OK") else ("colour214" if state['ralph'] == "WARN" else "colour196")
    
    return (
        f"#[fg=colour75,bold][OMA:#[fg=colour221]{state['mode']}:#[fg=colour229]{state['stage']}#[fg=colour75]]#[default] "
        f"#[fg={ralph_color}]ralph:{state['ralph']}#[default] "
        f"#[fg=colour214]tasks:{state['tasks']}#[default] "
        f"#[fg=colour141]{state['model']}#[default] "
        f"#[fg=colour39]git:{git_info}#[default] "
        f"#[fg=colour245]{state['ctx']}#[default]"
    )

def update_tmux(tmux_formatted_str):
    try:
        # Check if tmux is running
        res = subprocess.run(["tmux", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0 or os.environ.get("TMUX"):
            subprocess.run(["tmux", "set-option", "-g", "status-right-length", "150"], check=False)
            subprocess.run(["tmux", "set-option", "-g", "status-right", tmux_formatted_str], check=False)
            return True
    except Exception:
        pass
    return False

def update_state_files(plain_str, cwd):
    # 1. Update in project .omg/state/status-bar.txt
    try:
        omg_dir = Path(cwd) / ".omg" / "state"
        omg_dir.mkdir(parents=True, exist_ok=True)
        with open(omg_dir / "status-bar.txt", "w", encoding="utf-8") as f:
            f.write(plain_str + "\n")
    except Exception:
        pass
    
    # 2. Update global ~/.gemini/oma-status-bar.txt
    try:
        gemini_dir = Path.home() / ".gemini"
        gemini_dir.mkdir(parents=True, exist_ok=True)
        with open(gemini_dir / "oma-status-bar.txt", "w", encoding="utf-8") as f:
            f.write(plain_str + "\n")
    except Exception:
        pass

def update_terminal_title(plain_str):
    try:
        with open("/dev/tty", "w") as tty:
            tty.write(f"\033]0;{plain_str}\007")
            tty.flush()
    except Exception:
        if sys.stdout.isatty():
            sys.stdout.write(f"\033]0;{plain_str}\007")
            sys.stdout.flush()

def main():
    cwd = os.getcwd()
    git_info = get_git_info()
    state = get_oma_state(cwd)
    
    plain_bar = build_plain_bar(state, git_info)
    tmux_bar = build_tmux_bar(state, git_info)
    
    # Update tmux if active
    tmux_updated = update_tmux(tmux_bar)
    
    # Always update terminal window title
    update_terminal_title(plain_bar)
    
    # Update persistent state files
    update_state_files(plain_bar, cwd)
    
    # Check flags
    if "--print" in sys.argv:
        print(plain_bar)
    elif "--tmux" in sys.argv:
        print(tmux_bar)
    elif "--title" in sys.argv:
        pass
    else:
        # Default run: output status if not quiet
        if not tmux_updated and "--quiet" not in sys.argv:
            print(plain_bar)

if __name__ == "__main__":
    main()
