# Pull Request Workflow for Protected Main Branch

Quick reference guide for working with branch protection rules that require PRs before merging to main.

---

## When You Need This Workflow

GitHub will reject your push with this error:
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
```

This is **GOOD** - it means your branch protection is working correctly.

---

## The 6-Step Workflow (Simple Version)

### Step 1: Create Feature Branch
```bash
git checkout -b feature-branch-name
```

**Naming Convention**:
- `docs/` - Documentation changes (e.g., `docs/security-documentation`)
- `feat/` - New features (e.g., `feat/add-new-skill`)
- `fix/` - Bug fixes (e.g., `fix/security-check-pattern`)
- `chore/` - Maintenance (e.g., `chore/update-dependencies`)

### Step 2: Push Feature Branch
```bash
git push -u origin feature-branch-name
```

**What This Does**:
- Sends your branch to GitHub
- GitHub provides a URL for creating the PR
- Look for: `https://github.com/mbcoalson/skills/pull/new/feature-branch-name`

### Step 3: Create Pull Request

**Option A - Website (Recommended)**:
1. Copy the URL from the terminal output
2. Paste it into your browser
3. Fill in the PR title and description
4. Click "Create pull request"

**Option B - GitHub CLI** (if installed):
```bash
gh pr create --title "your title" --body "your description"
```

### Step 4: Review and Merge

**On GitHub Website**:
1. Review the changes in the PR
2. Click "Merge pull request"
3. Choose "Squash and merge" (recommended for clean history)
4. Confirm merge

### Step 5: Update Local Main
```bash
git checkout main
git pull origin main
```

**What This Does**:
- Switches back to main branch
- Pulls the merged changes from GitHub

### Step 6: Clean Up
```bash
git branch -d feature-branch-name
```

**Optional** - Delete remote branch:
```bash
git push origin --delete feature-branch-name
```

**Note**: GitHub usually auto-deletes the remote branch after merge.

---

## Quick Reference Card (Memorize This)

```bash
# 1. Branch
git checkout -b docs/my-change

# 2. Push
git push -u origin docs/my-change

# 3. Create PR (copy URL from terminal, open in browser)

# 4. Merge (on GitHub website)

# 5. Update local
git checkout main
git pull origin main

# 6. Clean up
git branch -d docs/my-change
```

---

## Common Scenarios

### Scenario 1: Already Committed to Main (Oops!)

If you already committed to main locally but can't push:

```bash
# Don't panic! Your commit is safe.

# 1. Create branch FROM your current position
git checkout -b docs/my-fix

# 2. Push the new branch
git push -u origin docs/my-fix

# 3. Reset main to match remote
git checkout main
git reset --hard origin/main

# 4. Continue with Step 3 (Create PR)
```

### Scenario 2: Multiple Commits Before Pushing

This workflow works fine with multiple commits:

```bash
git checkout -b feat/big-feature
git add file1.js
git commit -m "feat: add part 1"
git add file2.js
git commit -m "feat: add part 2"
git add file3.js
git commit -m "feat: add part 3"

# Push all commits at once
git push -u origin feat/big-feature

# Create PR - all 3 commits will be in the PR
```

### Scenario 3: Need to Update PR After Review

If someone requests changes on your PR:

```bash
# Make sure you're on the feature branch
git checkout feature-branch-name

# Make your changes
# ... edit files ...

# Commit and push
git add .
git commit -m "fix: address review comments"
git push

# PR automatically updates - no need to create a new one!
```

---

## Why Squash and Merge?

When merging the PR, use "Squash and merge" because:

1. **Clean History**: All commits in the PR become one commit on main
2. **Easy Rollback**: If needed, you can revert one commit instead of many
3. **Readable Log**: `git log` on main shows one entry per feature/fix

**Example**:
- PR has 5 commits: "wip", "fix typo", "another fix", "final fix", "really final"
- Squash merges as: "feat: add new security documentation"

---

## Current PR Waiting for You

You have a PR ready to complete:

**Branch**: docs/security-documentation
**URL**: https://github.com/mbcoalson/skills/pull/new/docs/security-documentation

**Next Steps**:
1. Open that URL in your browser
2. Title: "docs: add comprehensive security documentation"
3. Body: "Documents all security layers including local checks, GitHub rulesets, and future enhancements"
4. Create PR
5. Merge it
6. Come back to terminal for cleanup

---

## Troubleshooting

### "gh: The term 'gh' is not recognized"
- GitHub CLI not installed
- Use the website workflow instead (Option A in Step 3)

### "fatal: A branch named 'X' already exists"
- You already created this branch
- Use `git checkout X` instead of `git checkout -b X`

### "Your branch is ahead of 'origin/main' by N commits"
- You committed to main locally
- Follow "Scenario 1: Already Committed to Main" above

### PR merge button is grayed out
- Check for merge conflicts
- Click "Resolve conflicts" button if present
- Or update your branch: `git pull origin main` then push

---

## Remember

✅ **DO**: Create feature branches for all work
✅ **DO**: Use descriptive branch names
✅ **DO**: Squash and merge for clean history
✅ **DO**: Delete branches after merging

❌ **DON'T**: Try to force push to main (`git push --force`)
❌ **DON'T**: Try to bypass rulesets (they're protecting you!)
❌ **DON'T**: Work directly on main branch

---

**Built with [Claude Code](https://claude.com/claude-code)**
