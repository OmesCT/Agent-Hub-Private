---
name: feedback-always-rebase-on-latest-main
description: "Always fetch and rebase working branches (dev-ohm, fix/*) onto the latest origin/main before analysing, fixing, building or tagging"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c7c76821-7c8d-4205-b2e9-1f632abb53bd
  modified: 2026-10-07T03:48:33.180Z
---

Before any step that reads or changes code — bug hunting, re-verification, fixing, building images, tagging — run `git fetch origin` and bring the working branch onto the latest `origin/main` (fast-forward if possible, otherwise rebase). Re-check after long-running background work too, and re-verify findings if main moved.

**Why:** the team ships releases fast (0.14 → 0.17 in about a day, 2026-10-02/03). A frontend bug hunt was done on 0.14.0 while main reached 0.17.0, which forced a full 172-item re-verification. The user said (2026-10-03): "อยากให้ rebase ไว้ตลอด… เผื่อเขาทำ version ใหม่มาแล้วเรายัง process version เก่าอยู่".

**How to apply:**
- Start of every work block: `git fetch origin && git rev-list --left-right --count origin/main...HEAD`. If behind, rebase/ff first, then continue.
- Long background runs (workflows, agents) read the working tree: rebase in a separate git worktree while they run, swap afterwards.
- Pushing a rewritten branch still needs the user's go-ahead (`--force-with-lease`); never move existing tags ([[feedback-dev-ohm-issue-first-no-mr]]).
- Always state which release (VERSION on main) an analysis or build is based on.
- 2026-10-06: a fast-forward of dev-ohm is always safe; once dev-ohm carries the user's own pushed commit (0267a93 role-flow report, dev-ohm intentionally 1 ahead of main and equal to origin/dev-ohm) do NOT rebase it: that rewrites a pushed commit while another session works in the primary checkout. Say so and ask. For a long analysis use a pinned worktree and re-validate quotes/lines (qcheck) on the newest main right before filing; main moved 4 times in about 6 hours (0.19.1 -> 0.20.0).
- 2026-10-07 (later): when dev-ohm carries its own pushed commit and falls behind main again, the user preferred NOT to force-push ("แล้วเราต้อง force-push อะไร") and chose an MR dev-ohm -> main left open (!176). The project merges with a merge commit, so the SHA survives and dev-ohm fast-forwards afterwards. The project deletes the source branch after merge by default: create that MR with remove_source_branch=false (API) and merge it without `--remove-source-branch`. Offer this route before proposing rebase + force-push.
- Outcome 2026-10-07: I asked once ("rebase would need a force-push, say the word"), the user answered "update หน่อยตอนนี้ และ push ไป branch dev-ohm เลย". Then: `git rebase origin/main` in the primary checkout (dev-ohm), resolve the one `docs/AGENTS.md` reviews-row conflict by keeping both lists, `git push --force-with-lease=dev-ohm:<old tip>` (the lease protects against a push made meanwhile). Ask once, then do it exactly; never a bare `--force`.
