---
name: git-dual-branch-workflow
description: Standard operating procedure for dual-branch Git workflows requiring synchronized feature branch and main branch updates with pre-commit build verification.
---

# Git Dual-Branch Safe Synchronization Workflow

This skill standardizes the process of developing on a dedicated feature/dev branch (e.g. `DevOhm`) while keeping the `main` branch continuously updated and synchronized.

---

## 1. Operating Procedure

1. **Pre-Commit Verification**:
   - Always run frontend/backend typechecks and production builds before committing:
   ```bash
   npm run build
   ```

2. **Commit and Push to Dev Branch**:
   - Stage modified files explicitly.
   - Commit using conventional commit format with zero emojis:
   ```bash
   git add <files>
   git commit -m "type(scope): description without emoji"
   git push origin <dev-branch>
   ```

3. **Merge and Push to Main**:
   - Checkout `main`, merge the dev branch with `--no-edit`, push to `origin main`, and immediately switch back to the dev branch:
   ```bash
   git checkout main && git merge <dev-branch> --no-edit && git push origin main && git checkout <dev-branch>
   ```

---

## 2. Fast Command Pipeline

```bash
# Complete Single-Step Execution Chain
npm run build && \
git add <files> && \
git commit -m "type(scope): concise description" && \
git push origin DevOhm && \
git checkout main && \
git merge DevOhm --no-edit && \
git push origin main && \
git checkout DevOhm
```

---

## 3. Checklist for Git Operations

- [ ] Build and typecheck pass with code 0 before staging.
- [ ] Commit message strictly contains no emojis.
- [ ] Working branch returned to active feature branch after syncing `main`.
- [ ] Both `origin/<dev-branch>` and `origin/main` reflect identical commit hashes.
