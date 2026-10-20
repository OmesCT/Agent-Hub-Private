#!/bin/bash
# Keeps Claude from working on an old release: compares the current branch with origin/main.
# Notify/block only — never merges, rebases or fast-forwards anything.
#   main-sync.sh context  -> SessionStart / UserPromptSubmit: inject "main moved" context
#   main-sync.sh guard    -> PreToolUse(Bash): deny build/push/tag/MR commands while behind main
mode="${1:-context}"
input="$(cat)"
repo="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$repo" || exit 0
git rev-parse -q --verify refs/remotes/origin/main >/dev/null || exit 0

if [ "$mode" = guard ]; then
  cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
  printf '%s' "$cmd" | grep -Eq '(^|[;&|(]|&&|\|\|)[[:space:]]*(docker[[:space:]]+(buildx[[:space:]]+)?build|docker[[:space:]]+compose[^;&|]*--build|git[[:space:]]+push|git[[:space:]]+tag[[:space:]]+(-[asfd]|[^-[:space:]])|glab[[:space:]]+mr[[:space:]]+create)' || exit 0
fi

# Fetch at most once per 60s; 5s connect timeout so an offline VPN never stalls the prompt.
stamp="$repo/.git/.main-sync-fetch"
fetch_note=""
if [ ! -f "$stamp" ] || [ $(( $(date +%s) - $(stat -f %m "$stamp" 2>/dev/null || echo 0) )) -ge 60 ]; then
  if GIT_SSH_COMMAND="ssh -o ConnectTimeout=5 -o BatchMode=yes" git fetch -q origin main 2>/dev/null; then
    touch "$stamp"
  else
    fetch_note=" (fetch failed — VPN/GitLab unreachable; comparing with the last fetched origin/main)"
  fi
fi

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
behind="$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)"
ahead="$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)"
main_ver="$(git show origin/main:VERSION 2>/dev/null | tr -d '[:space:]')"
head_ver="$(git show HEAD:VERSION 2>/dev/null | tr -d '[:space:]')"
main_sha="$(git rev-parse --short origin/main)"

if [ "$mode" = guard ]; then
  [ "$behind" -gt 0 ] || exit 0
  reason="Blocked by main-sync hook: branch '$branch' (VERSION $head_ver) is $behind commit(s) behind origin/main ($main_ver, $main_sha)$fetch_note. Rebase onto origin/main first (ask the user before any force-push), then retry."
  jq -n --arg r "$reason" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
fi

event="$(printf '%s' "$input" | jq -r '.hook_event_name // "SessionStart"' 2>/dev/null)"
if [ "$behind" -gt 0 ]; then
  msg="[main-sync] origin/main is at $main_ver ($main_sha) but branch '$branch' is at $head_ver: $behind commit(s) behind, $ahead ahead$fetch_note. Do not analyse, fix, build or tag on this base — rebase onto origin/main first (in a separate worktree if background agents are reading the tree) and tell the user. Never force-push without asking."
elif [ "$event" = SessionStart ]; then
  msg="[main-sync] branch '$branch' is up to date with origin/main ($main_ver, $main_sha); $ahead commit(s) ahead$fetch_note."
else
  exit 0
fi
jq -n --arg e "$event" --arg m "$msg" '{hookSpecificOutput:{hookEventName:$e,additionalContext:$m}}'
