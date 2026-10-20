---
name: orca
description: Operate Orca-managed worktrees, terminals, repos, automations, embedded browser, and supervised worker orchestration through the orca CLI. Main entry point routing to orca-cli, orchestration, orca-linear, orca-per-workspace-env, orca-emulator, and computer-use.
---

# Orca Skill Entry Point

Route to and read the corresponding specialized Orca skill based on the task:

1. **Worktrees, Terminals, Full Handoffs, Browser, Artifacts, Automations:**
   Read `~/.gemini/config/skills/orca-cli/SKILL.md`
2. **Supervised Multi-Agent Orchestration (Coordinator & Worker Lifecycle):**
   Read `~/.gemini/config/skills/orchestration/SKILL.md`
3. **Linear Ticket Workflow via Orca:**
   Read `~/.gemini/config/skills/orca-linear/SKILL.md`
4. **Per-Workspace Environment Isolation (Ports, DBs, Compose, .env):**
   Read `~/.gemini/config/skills/orca-per-workspace-env/SKILL.md`
5. **Mobile Emulator Control (iOS / Android):**
   Read `~/.gemini/config/skills/orca-emulator/SKILL.md` and `~/.gemini/config/skills/orca-emulator-android/SKILL.md`
6. **Desktop GUI / App Window Control (`orca computer`):**
   Read `~/.gemini/config/skills/computer-use/SKILL.md`

## Antigravity Specific Notes for Orca

- In Orca, Google's Antigravity agent ID is `--agent antigravity` (`agy` CLI). Do not pass `--model` when spawning `--agent antigravity`.
- First start of `--agent antigravity` in a cold worktree may fail with `agent_not_in_foreground` at 60s; release with `orca orchestration worker-release --dispatch <failed>` and retry with `--retry-of <failed> --timeout-ms 180000`.
- When acting as an Orca worker, run `orca orchestration check --terminal <handle> --json` at the start and between heavy steps, and never use bare `cd` in persistent shells.
